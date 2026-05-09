import os
import glob
import asyncio
from typing import List, Dict, Any, Optional
import pandas as pd

from .experiment import Experiment
from .participant import Participant
from .model import Model
from .utils.read_yaml import read_yaml


class RunManager:

    def __init__(self, config_dir: str):
        self.config_dir: str = config_dir

        self.experiments: Dict[str, Experiment] = {}
        self.models: Dict[str, Any] = {}
        self.participants: List[Participant] = []

        self.results: pd.DataFrame = pd.DataFrame()

    def _load_yaml(self, filename: str) -> dict:
        return read_yaml(self.config_dir + filename)

    def load_experiments(self) -> None:
        experiments_yaml = self._load_yaml('experiments.yaml')
        scenarios_yaml = self._load_yaml('scenarios.yaml')

        for e_config in experiments_yaml.get('experiments'):
            if not e_config.get('scenario'):
                scenario = list(filter(
                    lambda s: s.get('experiment_id') == e_config.get('id'),
                    scenarios_yaml.get('scenarios')
                ))
                if scenario:
                    e_config['scenario'] = scenario[0].get('steps')

            self.experiments[e_config.get('id')] = Experiment(e_config)

        print(f'Loaded {len(self.experiments)} experiment(s)')

    def load_participants(self) -> None:
        participants_yaml = self._load_yaml('participants.yaml')

        for p_config in participants_yaml.get('participants'):
            for p_ec in list(p_config.get('experiments_conditions', '').split(';')):
                experiment_id = p_ec.split(',')[0]
                condition_id = p_ec.split(',')[1]
                n = 1 if len(p_ec.split(',')) == 2 else int(p_ec.split(',')[2])
                for i in range(n):
                    p_config.update({'experiment_id': experiment_id, 'condition_id': condition_id})
                    self.participants.append(Participant(p_config))

        print(f'Loaded {len(self.participants)} participant(s)')

    def load_models(self) -> None:
        models_yaml = self._load_yaml('models.yaml')

        model_templates = {mt['id']: mt for mt in models_yaml.get('model_templates')}

        for m_config in models_yaml.get('models'):
            model_template_id = m_config.get('model_template_id')
            if model_template_id and model_template_id in model_templates.keys():
                m_config.update(model_templates[model_template_id]['default'])

            self.models[m_config.get('id')] = Model(m_config)

        print(f'Loaded {len(self.models)} model(s)')

    def load_all(self) -> None:
        self.load_experiments()
        self.load_participants()
        self.load_models()

    def _print_run_title(self, run_title) -> None:
        n = len(run_title)
        print('=' * (n + 8))
        print('=== ' + run_title + ' ===')
        print('=' * (n + 8))

    def _load_existing_iterations(self, model_dir: str) -> Dict[int, pd.DataFrame]:
        existing: Dict[int, pd.DataFrame] = {}
        for filepath in glob.glob(os.path.join(model_dir, 'iteration_*.csv')):
            basename = os.path.basename(filepath)
            try:
                num = int(basename.replace('iteration_', '').replace('.csv', ''))
                existing[num - 1] = pd.read_csv(filepath)
            except Exception:
                pass
        return existing

    def _collect_experiment_results(self, experiment_dir: str) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for filepath in glob.glob(
            os.path.join(experiment_dir, '**', 'iteration_*.csv'), recursive=True
        ):
            try:
                frames.append(pd.read_csv(filepath))
            except Exception:
                pass
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def run(self, run_config: dict) -> None:
        run_id = run_config.get('id')
        run_title = run_config.get('title', run_id)

        self._print_run_title(run_title)

        results_folder = os.environ.get('RESULTS_FOLDER', 'results/')
        run_dir_name = os.path.join(results_folder, run_id)
        os.makedirs(run_dir_name, exist_ok=True)

        touched_experiment_dirs: Dict[str, str] = {}

        for exp_config in run_config.get('experiments', []):
            experiment_id = exp_config.get('experiment_id')
            variation_id = exp_config.get('variation_id', 'default')

            if experiment_id not in self.experiments:
                print(f'Experiment {experiment_id} not found.')
                continue

            experiment = self.experiments[experiment_id]
            variation_ids = list(map(lambda v: v['id'], experiment.variations))

            if variation_id != 'default' and variation_id not in variation_ids:
                print(f'Variation {variation_id} for experiment {experiment_id} not found.')
                continue

            experiment_dir_name = os.path.join(run_dir_name, experiment_id)
            os.makedirs(experiment_dir_name, exist_ok=True)
            touched_experiment_dirs[experiment_id] = experiment_dir_name

            variation_dir_name = os.path.join(experiment_dir_name, variation_id)
            os.makedirs(variation_dir_name, exist_ok=True)

            for model_config in exp_config.get('models', []):
                model_id = model_config.get('model_id')

                if model_id not in self.models:
                    print(f'Model {model_id} not found.')
                    continue

                model = self.models[model_id]

                model_dir_name = os.path.join(variation_dir_name, model_id)
                os.makedirs(model_dir_name, exist_ok=True)

                n_iterations = model_config.get('n_iterations', 1)

                existing_iterations = self._load_existing_iterations(model_dir_name)
                done_count = len(existing_iterations)

                experiment_variation_title = experiment.get_title(variation_id)

                if done_count >= n_iterations:
                    print(f'{experiment_variation_title} -> {model.name} -> All {n_iterations} iteration(s) already done, skipping')
                    continue

                for iteration in range(n_iterations):
                    if iteration in existing_iterations:
                        print(f'{experiment_variation_title} -> {model.name} -> Iteration {iteration + 1}/{n_iterations} already done, skipping')
                        continue

                    print(f'{experiment_variation_title} -> {model.name} -> Iteration {iteration + 1}/{n_iterations}')

                    experiment_results = asyncio.run(experiment.run(
                        self.participants, model, variation_id
                    ))

                    if not experiment_results.empty:
                        experiment_results['iteration_id'] = iteration
                        filename = f'iteration_{iteration + 1}.csv'
                        filepath = os.path.join(model_dir_name, filename)
                        experiment_results.to_csv(filepath, index=False)
                        print(f'Saved results to {filepath}')

        all_run_frames: List[pd.DataFrame] = []
        if os.path.isdir(run_dir_name):
            for entry in sorted(os.scandir(run_dir_name), key=lambda e: e.name):
                if not entry.is_dir():
                    continue
                experiment_dir = entry.path
                exp_results = self._collect_experiment_results(experiment_dir)
                if not exp_results.empty:
                    filepath = os.path.join(experiment_dir, 'results.csv')
                    exp_results.to_csv(filepath, index=False)
                    print(f'Rebuilt results for {entry.name} -> {filepath}')
                    all_run_frames.append(exp_results)

        if all_run_frames:
            self.results = pd.concat(all_run_frames, ignore_index=True)

    def get_results(self) -> pd.DataFrame:
        return self.results.copy()

    def clear_results(self) -> None:
        self.results = pd.DataFrame()
        for experiment in self.experiments.values():
            experiment.clear_results()
