from typing import List, Optional, Dict, Any, Tuple


class Participant:
    
    def __init__(self, participant_config: dict):
        self.name: Optional[str] = participant_config.get('name')
        self.gender: Optional[str] = participant_config.get('gender')
        self.participant_template_id: Optional[str] = participant_config.get('participant_template_id')
        
        self._set_pronouns()
        
        self.experiments_conditions: List[Tuple[str, str]] = []
        
        if 'experiments_conditions' in participant_config:
            self.experiments_conditions = list(map(
                lambda ec: list(ec.split(',')),
                participant_config.get('experiments_conditions').split(';')
            ))
    
    def _set_pronouns(self) -> None:
        if self.gender == 'male':
            self.pronoun_subject = 'he'
            self.pronoun_object = 'him'
            self.pronoun_possessive = 'his'
            self.pronoun_possessive_absolute = 'his'
            self.pronoun_reflexive = 'himself'
        elif self.gender == 'female':
            self.pronoun_subject = 'she'
            self.pronoun_object = 'her'
            self.pronoun_possessive = 'her'
            self.pronoun_possessive_absolute = 'hers'
            self.pronoun_reflexive = 'herself'
        else:
            self.pronoun_subject = 'they'
            self.pronoun_object = 'them'
            self.pronoun_possessive = 'their'
            self.pronoun_possessive_absolute = 'theirs'
            self.pronoun_reflexive = 'themselves'
    
    def is_assigned_to_experiment(self, experiment_id: str) -> bool:
       return any(exp_id == experiment_id for exp_id, _ in self.experiments_conditions)
    
    def get_condition_for_experiment(self, experiment_id: str) -> Optional[str]:
        for exp_id, cond_id in self.experiments_conditions:
            if exp_id == experiment_id:
                return cond_id
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'gender': self.gender
        }
    
    def __str__(self) -> str:
        return self.get_title_and_name()

    def __repr__(self) -> str:
        return self.get_title_and_name()
