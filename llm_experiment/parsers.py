import re
from typing import List, Any, Dict, Optional


class Parser:

    def __init__(self):
        pass
    
    def parse(s: str) -> Optional[str]:
        raise NotImplementedError


class IntegerParser(Parser):

    def __init__(self, range_min: int = None, range_max: int = None, default: Optional[str] = None):
        super().__init__()

        self.range_min = range_min
        self.range_max = range_max
        self.default = default
    
    def parse(s: str) -> Optional[str]:
        if not isinstance(s, str):
            return self.default
        
        match = re.match(r'^[-+]?\d+', s.strip())
        if not match:
            return self.default
        
        try:
            number = int(match.group())
        except ValueError:
            return self.default
        
        if self.range_min is not None and number < self.range_min:
            return self.default
            
        if self.range_max is not None and number > self.range_max:
            return self.default
        
        return number


class YesNoParser(Parser):

    def __init__(self, default: Optional[str] = None):
        super().__init__()

        self.yes_patterns = ['yes']
        self.no_patterns = ['no']

        self.default = default
    
    def parse(s: str) -> Optional[str]:
        if not s or not isinstance(s, str):
            return self.default
        
        s_lower = s.strip().lower()
        
        if s_lower in self.yes_patterns:
            return 'yes'
        elif s_lower in self.no_patterns:
            return 'no'
        
        return self.default


def get_parser(parser_name, **kwargs):
    if parser_name == 'IntegerParser':
        return IntegerParser(**kwargs)
    
    if parser_name == 'YesNoParser':
        return YesNoParser(**kwargs)
    
    raise RuntimeError(f'Parser {parser_name} is not implemented')
