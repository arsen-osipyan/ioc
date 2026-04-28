from typing import Dict, Any, Optional, List, TYPE_CHECKING, Callable
import re

from .participant import Participant
from .model import Model
from .utils.parsers import get_parser
from .utils.generators import get_random_football_player, get_random_8_letters

if TYPE_CHECKING:
    from .experiment import Experiment


class Session:
    
    def __init__(
        self,
        scenario: List[dict],
        measures: List[dict],
        participant: Participant,
        model: Model
    ):
        self.scenario: List[dict] = scenario
        self.measures: List[dict] = measures
        self.participant: Participant = participant
        self.model: LLMAgent = model
        
        self.result: Dict[str, Any] = {}
        self._init_result()
    
    def _init_result(self) -> None:
        self.result = {}
        self.result.update(self.participant.to_dict())
        self.result.update(self.model.to_dict())        
    
    def _format_text(self, text: str) -> str:
        _globals = globals()

        def replace(match):
            expr = match.group(1).strip()
            if expr.startswith('participant.'):
                name = expr[len('participant.'):]
                is_call = name.endswith('()')
                attr = getattr(self.participant, name[:-2] if is_call else name, None)
                return str(attr() if is_call else attr) if attr is not None else match.group(0)
            if expr.endswith('()'):
                func = _globals.get(expr[:-2])
                return str(func()) if callable(func) else match.group(0)
            return match.group(0)

        return re.sub(r'\{\{(.+?)\}\}', replace, text)
    
    async def run(self) -> Dict[str, Any]:
        prompt = ''

        for step in self.scenario:
            text = self._format_text(step.get('text'))
            if text and text != '':
                prompt += text

            if step.get('measure_id'):
                if not filter(lambda m: m['id'] == step.get('measure_id'), self.measures):
                    continue
                
                measure = list(filter(lambda m: m['id'] == step.get('measure_id'), self.measures))[0]

                parser = None
                if measure.get('parser'):
                    parser = get_parser(measure.get('parser').get('name'), **measure.get('parser').get('params'))
                
                try:
                    answer = await self.model.generate(prompt, parser)
                except Exception as e:
                    print(f'Error in Session.run(): {e}')
                    answer = None
                
                self.result[step.get('measure_id')] = answer
                
                prompt = ''
        
        return self.result
