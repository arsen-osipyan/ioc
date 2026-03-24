import os
import asyncio
from typing import List, Optional, Dict, Any
from tqdm import tqdm
import pandas as pd

from .model import Model
from .participant import Participant


class Experiment:
    
    def __init__(self, experiment_config: dict):
        self.id: str = experiment_config['id']
        self.title: Optional[str] = experiment_config.get('title')
        
        self.conditions: List[dict] = experiment_config.get('conditions', [])
        self.measures: List[dict] = experiment_config.get('measures', [])
        self.variations: List[dict] = experiment_config.get('variations', [])
        
        self.scenario: List[dict] = experiment_config.get('scenario', [])
        
        self.results: pd.DataFrame = pd.DataFrame()

    def adapt_scenario(
        self,
        condition_id: str,
        variation_id: Optional[str] = None
    ) -> List[dict]:
        adapted_scenario = []

        for step in self.scenario:
            if step.get('condition_id') and step.get('condition_id') != condition_id:
                continue
            
            text = step.get('text')

            if variation_id:
                for step_variation in step.get('variations', []):
                    if step_variation.get('variation_id') == variation_id and step_variation.get('text'):
                        text = step_variation.get('text')
            
            adapted_step = dict(text=text)

            if step.get('measure_id'):
                adapted_step['measure_id'] = step.get('measure_id')
            
            adapted_scenario.append(adapted_step)

        return adapted_scenario

    def split_participants_by_conditions(
        self,
        participants: List[Participant]
    ) -> Dict[str, List[Participant]]:
        participants_split = {condition['id']: [] for condition in self.conditions}
        
        for participant in participants:
            if participant.is_assigned_to_experiment(self.id):
                participant_condition_id = participant.get_condition_for_experiment(self.id)

                if participant_condition_id in participants_split.keys():
                    participants_split[participant_condition_id].append(participant)
        
        return participants_split

    async def run(
        self,
        participants: List[Participant],
        model: Model,
        variation_id: Optional[str] = None
    ) -> pd.DataFrame:
        all_results = []

        participants_split = self.split_participants_by_conditions(participants)
        
        for condition in self.conditions:
            condition_id = condition.get('id')
            condition_title = condition.get('title')
            
            adapted_scenario = self.adapt_scenario(condition_id, variation_id)
            
            tasks = []
            condition_participants = participants_split[condition_id]
            
            print(f'  - {condition_title}: Starting {len(condition_participants)} sessions in parallel...')
            
            for participant in condition_participants:
                model_copy = model.copy()

                from .session import Session

                session = Session(
                    scenario=adapted_scenario,
                    measures=self.measures,
                    participant=participant,
                    model=model_copy
                )
                
                tasks.append(session.run())
            
            condition_results = await asyncio.gather(*tasks)
            
            for result in condition_results:
                result['experiment_id'] = self.id
                result['variation_id'] = variation_id
                result['condition_id'] = condition_id
                all_results.append(result)
            
            print(f'  - {condition_title}: Completed {len(condition_results)} sessions')
        
        run_df = pd.DataFrame(all_results)
        
        if self.results.empty:
            self.results = run_df
        else:
            self.results = pd.concat([self.results, run_df], ignore_index=True)
        
        return run_df
    
    def get_result(self) -> pd.DataFrame:
        return self.results.copy()
    
    def clear_result(self) -> None:
        self.results = pd.DataFrame()
    
    def get_title(self, variation_id: Optional[str] = None) -> str:
        if not self.variations:
            return self.title
        
        if not variation_id or variation_id == 'default':
            return self.title + ' (Default)'
        
        variation_ids = list(map(lambda v: v['id'], self.variations))

        if variation_id in variation_ids:
            variation_title = list(filter(lambda v: v['id'] == variation_id, self.variations))[0]['title']
            return self.title + ' (' + variation_title + ')'
        
        return self.title + ' (' + variation_id + ')'
