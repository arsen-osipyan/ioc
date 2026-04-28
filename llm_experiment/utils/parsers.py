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


if __name__ == '__main__':
    integer_parser = IntegerParser()
    boolean_parser = BooleanParser()
    float_parser = FloatParser()

    print(integer_parser.parse('It would be 10$'))
    print(integer_parser.parse('It would be 10.0$'))
    print(integer_parser.parse('10'))
    print(integer_parser.parse('-1'))
    print(integer_parser.parse('0'))

    print(boolean_parser.parse('yes'))
    print(boolean_parser.parse('yeah'))
    print(boolean_parser.parse('hmmm yeah'))
    print(boolean_parser.parse('hmmm yes'))
    print(boolean_parser.parse('hmmm no'))
    print(boolean_parser.parse('hmmm nope'))
    print(boolean_parser.parse('1'))
    print(boolean_parser.parse('true'))
    print(boolean_parser.parse('0'))
    print(boolean_parser.parse('false'))
    print(boolean_parser.parse('yoo noo'))

    print(float_parser.parse('0'))
    print(float_parser.parse('0.0'))
    print(float_parser.parse('0.34'))
    print(float_parser.parse('0.34342342'))
    print(float_parser.parse('3333.34342342'))
    print(float_parser.parse('333,2323'))
    print(float_parser.parse('-333.2323'))
    print(float_parser.parse('-333,2323'))
    print(float_parser.parse('+333.2323'))

