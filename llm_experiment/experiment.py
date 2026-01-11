import os
import time
from typing import List, Any, Dict
from tqdm import tqdm
import pandas as pd

from .llm import LLMAgent
from .parsers import get_parser_by_name



class Participant:

    def __init__(self, participant_config: dict):
        self.id = participant_config['id']
        self.name = participant_config.get('name')
        self.gender = participant_config.get('gender')

        self.experiments_conditions: List[tuple] = [
            (ec.get('experiment_id'), ec.get('condition_id'))
            for ec in participant_config.get('experiments_conditions')
            if 'experiment_id' in ec and 'condition_id' in ec
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            # 'participant_id': self.id,
            # 'participant_name': self.name,
            'participant_gender': self.gender
        }
    
    def __repr__(self):
        return '{} {}'.format('Mr.' if self.gender == 'male' else 'Ms.', self.name)

    def __str__(self):
        return '{} {}'.format('Mr.' if self.gender == 'male' else 'Ms.', self.name)


class Experiment:

    def __init__(self, experiment_config: dict):
        self.id = experiment_config['id']
        self.title = experiment_config.get('title')
        self.description = experiment_config.get('description')

        self.scenario: List[dict] = experiment_config.get('scenario')

        self.conditions: List[Condition] = [
            Condition(self, c_config)
            for c_config in experiment_config.get('conditions')
        ]

        self.results: pd.DataFrame = pd.DataFrame()
    
    def run(self, model: LLMAgent, participants: List[Participant]) -> pd.DataFrame:
        print(f'Running {self}...')
        
        run_time = int(time.time() * 1000)
        run_df = pd.DataFrame()
        
        participants_filtered = [
            p for p in participants
            if hasattr(p, 'experiments_conditions')
            and any(isinstance(pec, (list, tuple)) and len(pec) >= 1 and pec[0] == self.id for pec in p.experiments_conditions)
        ]

        for i in range(len(self.conditions)):
            condition_results = self.conditions[i].run(model, participants_filtered)

            if run_df.empty:
                run_df = condition_results
            else:
                run_df = pd.concat([run_df, condition_results], ignore_index=True)
        
        run_df = run_df.assign(**self.to_dict())
        # run_df['experiment_run_ts'] = run_time

        if self.results.empty:
            self.results = run_df
        else:
            self.results = pd.concat([self.results, run_df], ignore_index=True)

        return run_df

    def to_dict(self) -> Dict[str, Any]:
        return {
            'experiment_id': self.id,
            'experiment_title': self.title,
            # 'experiment_scenario_hash': hash(str(self.scenario))
        }
    
    def get_result(self) -> pd.DataFrame:
        return self.results.copy()
    
    def clear_results(self) -> None:
        self.results = pd.DataFrame()
    
    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Condition:

    def __init__(self, experiment: Experiment, condition_config: dict):
        self.id = condition_config['id']
        self.title = condition_config.get('title')
        self.description = condition_config.get('description')

        self.experiment = experiment
        
        base_scenario = getattr(self.experiment, 'scenario', []) or []
        self.scenario: List[dict] = []
        for item in base_scenario:
            if isinstance(item, dict):
                if 'condition' not in item:
                    self.scenario.append(item)
                elif item.get('condition') == self.id:
                    new_item = item.copy()
                    new_item.pop('condition')
                    self.scenario.append(new_item)

        self.results: pd.DataFrame = pd.DataFrame()

    def run(self, model: LLMAgent, participants: List[Participant]) -> pd.DataFrame:
        print(f'Running {self}...')

        run_time = int(time.time() * 1000)
        run_rows = []
        
        participants_filtered = [
            p for p in participants
            if hasattr(p, 'experiments_conditions')
            and any(isinstance(pec, (list, tuple)) and len(pec) >= 2 and pec[1] == self.id for pec in p.experiments_conditions)
        ]

        for p in tqdm(participants_filtered):
            model_copy = model
            if hasattr(model, 'copy'):
                try:
                    model_copy = model.copy()
                except Exception:
                    model_copy = model

            session = Session(self.scenario, model_copy, p)
            session_result = session.run()

            if isinstance(session_result, dict):
                run_rows.append(session_result)
        
        run_df = pd.DataFrame(run_rows).assign(**self.to_dict())
        # run_df['condition_run_ts'] = run_time
        
        if self.results.empty:
            self.results = run_df
        else:
            self.results = pd.concat([self.results, run_df], ignore_index=True)

        return run_df
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'condition_id': self.id,
            'condition_title': self.title,
            # 'condition_scenario_hash': hash(str(self.scenario))
        }
    
    def get_result(self) -> pd.DataFrame:
        return self.results.copy()
    
    def clear_results(self) -> None:
        self.results = pd.DataFrame()
    
    def __str__(self):
        return f'{self.experiment.title}: {self.title}'
    
    def __repr__(self):
        return f'{self.experiment.title}: {self.title}'


class Session:
    def __init__(self, scenario: List[dict], model: LLMAgent, participant: Participant):
        if not isinstance(scenario, list):
            raise TypeError('scenario must be a list of dicts')

        self.scenario = scenario
        self.model = model
        self.participant = participant

        self.result: Dict[str, Any] = {}
        self._init_result()

    def _init_result(self) -> None:
        base = dict()
        
        if hasattr(self.model, 'to_dict'):
            base.update(self.model.to_dict())
        if hasattr(self.participant, 'to_dict'):
            base.update(self.participant.to_dict())

        self.result = base

    def _safe_str_participant(self) -> str:
        try:
            return str(self.participant)
        except Exception:
            return repr(self.participant)

    def run(self) -> Dict[str, Any]:
        prompt = ''
        subject_str = self._safe_str_participant()

        for idx, item in enumerate(self.scenario):
            if not isinstance(item, dict):
                continue

            content = item.get('content')
            role = item.get('role')
            measure = item.get('measure')
            parser_cfg = item.get('parser')

            if role:
                prompt += str(role) + ': '

            if content:
                prompt += str(content)
            
            prompt += '\n'
            
            if measure:
                prompt = prompt.replace('{{subject}}', subject_str)

                try:
                    answer = self.model.generate(prompt)
                except Exception:
                    answer = None

                self.result[measure + '_raw'] = answer

                parsed_value = answer
                if parser_cfg and isinstance(parser_cfg, dict):
                    parser_name = parser_cfg.get('name')
                    if parser_name:
                        try:
                            parser = get_parser_by_name(parser_name)
                            if parser_cfg.get('params'):
                                parsed_value = parser(
                                    answer, **parser_cfg['params']
                                )
                            else:
                                parsed_value = parser(answer)
                        except Exception:
                            parsed_value = None

                self.result[measure] = parsed_value
                
                prompt = ''

        return self.result

    def get_result(self) -> Dict[str, Any]:
        return self.result

    def clear_result(self) -> None:
        self._init_result()
