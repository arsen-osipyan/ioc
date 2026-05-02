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


class BooleanParser(Parser):
    
    TRUE_VALUES = {'true', '1', 'yes', 'yep', 'yeah', 'y', 'ok', 'okay'}
    FALSE_VALUES = {'false', '0', 'no', 'nah', 'nope', 'n'}
    
    def __init__(self, default: Optional[bool] = None):
        super().__init__()
        self.default = default
    
    def parse(self, s: str) -> Optional[bool]:
        if not isinstance(s, str):
            return self.default
        
        normalized = s.strip().lower()
        if not normalized:
            return self.default
        
        if normalized in self.TRUE_VALUES:
            return True
        
        if normalized in self.FALSE_VALUES:
            return False
        
        tokens = re.findall(r'[a-zA-Z0-9]+', normalized)
        for token in tokens:
            if token in self.TRUE_VALUES:
                return True
            if token in self.FALSE_VALUES:
                return False
        
        return self.default


class FloatParser(Parser):
    
    def __init__(
        self,
        default: Optional[float] = None,
        range_min: Optional[float] = None,
        range_max: Optional[float] = None
    ):
        super().__init__()
        self.default = default
        self.range_min = range_min
        self.range_max = range_max
    
    def parse(self, s: str) -> Optional[float]:
        if not isinstance(s, str):
            return self.default
        
        text = s.strip()
        if not text:
            return self.default
        
        match = re.search(r'[-+]?\d+(?:[.,]\d+)?', text)
        if not match:
            return self.default
        
        number_str = match.group().replace(',', '.')
        
        try:
            number = float(number_str)
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
    if name == 'BooleanParser':
        return BooleanParser(**params)
    if name == 'FloatParser':
        return FloatParser(**params)
    return None
