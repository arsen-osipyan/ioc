from typing import List, Optional, Dict, Any, Tuple

from .utils.generators import get_random_name


class Participant:
    
    def __init__(self, participant_config: dict):
        self.name: Optional[str] = participant_config.get('name', get_random_name())
        self.gender: Optional[str] = participant_config.get('gender')
        self.experiment_id: str = participant_config.get('experiment_id')
        self.condition_id: str = participant_config.get('condition_id')
    
    def is_assigned_to_experiment(self, experiment_id: str) -> bool:
       return self.experiment_id == experiment_id
    
    def get_condition_for_experiment(self, experiment_id: str) -> Optional[str]:
        if self.experiment_id == experiment_id:
            return self.condition_id
        return None
    
    def get_title(self) -> str:
        if self.gender == 'male':
            return 'Mr.'
        elif self.gender == 'female':
            return 'Ms.'
        else:
            return 'Mx.'
    
    def get_title_and_name(self) -> str:
        return self.get_title() + ' ' + self.name
    
    def get_pronoun_subject(self, title: bool = False) -> str:
        pronoun_subject = 'they'
        if self.gender == 'male':
            pronoun_subject = 'he'
        elif self.gender == 'female':
            pronoun_subject = 'she'
        return pronoun_subject if not title else pronoun_subject.title()
    
    def get_pronoun_object(self, title: bool = False) -> str:
        pronoun_object = 'them'
        if self.gender == 'male':
            pronoun_object = 'him'
        elif self.gender == 'female':
            pronoun_object = 'her'
        return pronoun_object if not title else pronoun_object.title()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'gender': self.gender
        }
    
    def __str__(self) -> str:
        return self.get_title_and_name()

    def __repr__(self) -> str:
        return self.get_title_and_name()
