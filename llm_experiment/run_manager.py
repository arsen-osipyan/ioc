import os
import time
from typing import List, Any, Dict
import pandas as pd

from .experiment import Experiment, Participant
from .llm import LLMAgent



class RunManager:

    def __init__(self):
        self.experiments: dict = dict()
        self.models: dict = dict()
        self.participants: dict = dict()

        self.results: pd.DataFrame = pd.DataFrame()

    def load_experiments(self, experiments_config: List[dict]) -> None:
        for e_config in experiments_config.get('experiments'):
            if 'id' in e_config:
                e_id = e_config.get('id')
                self.experiments[e_id] = Experiment(e_config)

    def load_models(self, models_config: List[dict]) -> None:
        for m_config in models_config.get('models'):
            if 'id' in m_config:
                m_id = m_config.get('id')
                self.models[m_id] = LLMAgent(m_config)
    
    def load_participants(self, participants_config: List[dict]) -> None:
        for p_config in participants_config.get('participants'):
            if 'id' in p_config:
                p_id = p_config.get('id')
                self.participants[p_id] = Participant(p_config)
    
    def load(self, experiments_config: List[dict], models_config: List[dict], participants_config: List[dict]) -> None:
        self._load_experiments(experiments_config)
        self._load_models(models_config)
        self._load_participants(participants_config)

    def run(self, run_config: dict) -> None:
        print(40 * '=', run_config.get('title'), 40 * '=')

        run_dir_name = os.environ.get('RESULTS_FOLDER') + run_config.get('id')
        os.makedirs(run_dir_name, exist_ok=True)

        for e in run_config.get('experiments'):
            if not e.get('experiment_id') in self.experiments.keys():
                print('Experiment {experiment_id} not found.'.format(experiment_id=e.get('experiment_id')))
                continue
            
            experiment = self.experiments[e.get('experiment_id')]

            experiment_dir_name = run_dir_name + '/' + e.get('experiment_id')
            os.makedirs(experiment_dir_name, exist_ok=True)

            for m in e.get('models'):
                if not m.get('model_id') in self.models.keys():
                    print('Model {model_id} not found.'.format(model_id=m.get('model_id')))
                    continue
                
                model = self.models[m.get('model_id')]

                model_dir_name = experiment_dir_name + '/' + m.get('model_id')
                os.makedirs(model_dir_name, exist_ok=True)
                
                for i in range(m.get('n_iterations', 0)):
                    print(f'{experiment} -> {model} -> Iteration {i + 1}')

                    experiment_results = experiment.run(model, self.participants.values())

                    filename = 'results_' + str(int(time.time())) + '.csv'

                    experiment_results.to_csv(model_dir_name + '/' + filename)
