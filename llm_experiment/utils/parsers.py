import re
from typing import Optional, Any


class Parser:
    
    def __init__(self):
        pass
    
    def parse(self, s: str) -> Optional[Any]:
        raise NotImplementedError


class IntegerParser(Parser):
    
    def __init__(
        self,
        default: Optional[int] = None,
        range_min: Optional[int] = None,
        range_max: Optional[int] = None
    ):
        super().__init__()
        self.default = default
        self.range_min = range_min
        self.range_max = range_max
    
    def parse(self, s: str) -> Optional[int]:
        if not isinstance(s, str):
            return self.default
        
        match = re.search(r'[-+]?\d+', s.strip())
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


def get_parser(name, **params):
    if name == 'IntegerParser':
        return IntegerParser(**params)
    return None
