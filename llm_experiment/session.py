from typing import Dict, Any, Optional, List, TYPE_CHECKING, Callable
import re
import ast

from .participant import Participant
from .model import Model
from .utils.parsers import get_parser
from .utils.generators import get_random_football_player, get_random_letter, get_random_symbol

if TYPE_CHECKING:
    from experiment import Experiment


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

        def _parse_call(expr: str):
            """Parse a call expression and return (func_name, args, kwargs).
            Returns None if expr is not a valid call."""
            try:
                tree = ast.parse(expr, mode='eval')
            except SyntaxError:
                return None
            if not isinstance(tree.body, ast.Call):
                return None
            call = tree.body
            # Only support simple Name or Attribute calls
            if isinstance(call.func, ast.Name):
                func_name = call.func.id
                obj_name = None
            elif isinstance(call.func, ast.Attribute):
                if not isinstance(call.func.value, ast.Name):
                    return None
                obj_name = call.func.value.id
                func_name = call.func.attr
            else:
                return None
            args = [ast.literal_eval(a) for a in call.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
            return obj_name, func_name, args, kwargs

        def replace(match):
            expr = match.group(1).strip()

            parsed = _parse_call(expr)
            if parsed is None:
                return match.group(0)

            obj_name, func_name, args, kwargs = parsed

            # participant.<method>(...)
            if obj_name == 'participant':
                method = getattr(self.participant, func_name, None)
                if callable(method):
                    return str(method(*args, **kwargs))
                return match.group(0)

            # top-level function call (no object prefix)
            if obj_name is None:
                func = _globals.get(func_name)
                if callable(func):
                    return str(func(*args, **kwargs))
                return match.group(0)

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
                    if measure.get('parser').get('params'):
                        parser = get_parser(measure.get('parser').get('name'), **measure.get('parser').get('params'))
                    else:
                        parser = get_parser(measure.get('parser').get('name'))
                
                try:
                    answer = await self.model.generate(prompt, parser)
                except Exception as e:
                    print(f'Error in Session.run(): {e}')
                    answer = None
                
                self.result[step.get('measure_id')] = answer
                
                prompt = ''

        return self.result
