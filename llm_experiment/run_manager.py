import os
import time
from typing import List, Dict, Any, Optional
import pandas as pd

from .experiment import Experiment
from .participant import Participant
from .llm import LLMAgent, create_agent
from .utils.read_yaml import read_yaml


class RunManager:
    
    def __init__(self, config_dir: str):
        self.config_dir: str = config_dir

        self.experiments: Dict[str, Experiment] = {}
        self.models: Dict[str, LLMAgent] = {}
        self.participants: List[Participant] = []

        self.results: pd.DataFrame = pd.DataFrame()
    
    def _load_yaml(self, filename: str) -> dict:
        return read_yaml(self.config_dir + filename)
    
    def load_experiments(self) -> None:
        experiments_yaml = self._load_yaml('experiments.yaml')
        scenarios_yaml = self._load_yaml('scenarios.yaml')

        for e_config in experiments_yaml.get('experiments'):
            if not e_config.get('scenario'):
                scenario = list(filter(lambda s: s.get('experiment_id') == e_config.get('id'), scenarios_yaml.get('scenarios')))
                if scenario:
                    e_config['scenario'] = scenario[0].get('steps')

            self.experiments[e_config.get('id')] = Experiment(e_config)
        
        print(f'Loaded {len(self.experiments)} experiment(s)')
    
    def load_participants(self) -> None:
        participants_yaml = self._load_yaml('participants.yaml')

        participant_templates = {pt['id']: pt for pt in participants_yaml.get('participant_templates')}

        for p_config in participants_yaml.get('participants'):
            participant_template_id = p_config.get('participant_template_id')
            if participant_template_id and participant_template_id in participant_templates.keys():
                p_config.update(participant_templates[participant_template_id]['default'])
            
            self.participants.append(Participant(p_config))

        print(f'Loaded {len(self.participants)} participant(s)')
    
    def load_models(self) -> None:
        models_yaml = self._load_yaml('models.yaml')

        for m_config in models_yaml.get('models'):
            self.models[m_config.get('id')] = create_agent(m_config)

        print(f'Loaded {len(self.models)} model(s)')
    
    def load_all(self) -> None:
        self.load_experiments()
        self.load_participants()
        self.load_models()
    
    def run(self, run_config: dict) -> None:
        run_id = run_config.get('id')
        run_title = run_config.get('title', run_id)
        
        print('=' * 40, run_title, '=' * 40)
        
        # Create run directory
        results_folder = os.environ.get('RESULTS_FOLDER', 'results/')
        run_dir_name = os.path.join(results_folder, run_id)
        os.makedirs(run_dir_name, exist_ok=True)
        
        # Process each experiment in the run
        for exp_config in run_config.get('experiments', []):
            experiment_id = exp_config.get('experiment_id')
            
            if experiment_id not in self.experiments:
                print(f'Experiment {experiment_id} not found.')
                continue
            
            experiment = self.experiments[experiment_id]
            
            # Create experiment directory
            experiment_dir_name = os.path.join(run_dir_name, experiment_id)
            os.makedirs(experiment_dir_name, exist_ok=True)
            
            # Get variation if specified
            variation_id = exp_config.get('variation_id')
            
            # Process each model for this experiment
            for model_config in exp_config.get('models', []):
                model_id = model_config.get('model_id')
                
                if model_id not in self.models:
                    print(f'Model {model_id} not found.')
                    continue
                
                model = self.models[model_id]
                
                # Create model directory
                model_dir_name = os.path.join(experiment_dir_name, model_id)
                os.makedirs(model_dir_name, exist_ok=True)
                
                # Run multiple iterations
                n_iterations = model_config.get('n_iterations', 1)
                
                for iteration in range(n_iterations):
                    print(f'{experiment.id} -> {model_id} -> Iteration {iteration + 1}/{n_iterations}')
                    
                    # Run experiment
                    experiment_results = experiment.run(
                        self.participants,
                        model,
                        variation_id
                    )
                    
                    # Save results
                    if not experiment_results.empty:
                        timestamp = int(time.time())
                        filename = f'results_{timestamp}_iter{iteration + 1}.csv'
                        filepath = os.path.join(model_dir_name, filename)
                        experiment_results.to_csv(filepath, index=False)
                        print(f'Saved results to {filepath}')
                    
                    # Store in manager results
                    if self.results.empty:
                        self.results = experiment_results
                    else:
                        self.results = pd.concat(
                            [self.results, experiment_results],
                            ignore_index=True
                        )
        
        print('=' * 80)
        print(f'Run {run_id} completed!')
    
    def get_results(self) -> pd.DataFrame:
        """
        Get all accumulated results.
        
        Returns:
            DataFrame with all results
        """
        return self.results.copy()
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results = pd.DataFrame()
        for experiment in self.experiments.values():
            experiment.clear_results()
    
    def __repr__(self) -> str:
        return (
            f"RunManager(experiments={len(self.experiments)}, "
            f"models={len(self.models)}, "
            f"participants={len(self.participants)})"
        )
