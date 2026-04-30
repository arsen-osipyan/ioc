import random
import string


def get_random_football_player() -> str:
    FOOTBALL_PLAYER_LIST = [
        'Lionel Messi', 'Cristiano Ronaldo', 'Pelé', 'Diego Maradona', 'Zinedine Zidane', 'Ronaldinho', 'Ronaldo Nazário',
        'Franz Beckenbauer', 'Johan Cruyff', 'Michel Platini', 'Alfredo Di Stéfano', 'Ferenc Puskás', 'George Best',
        'Bobby Charlton', 'Paolo Maldini', 'Franco Baresi', 'Roberto Baggio', 'Marco van Basten', 'Ruud Gullit', 'Gerd Müller',
        'Karl-Heinz Rummenigge', 'Lothar Matthäus', 'Oliver Kahn', 'Philipp Lahm', 'Andrés Iniesta', 'Xavi Hernandez',
        'Carles Puyol', 'Iker Casillas', 'Raúl González', 'David Beckham', 'Steven Gerrard', 'Frank Lampard', 'Wayne Rooney',
        'Ryan Giggs', 'Thierry Henry', 'Patrick Vieira', 'Zlatko Ibrahimović', 'Kylian Mbappé', 'Erling Haaland',
        'Robert Lewandowski', 'Luis Suárez', 'Neymar Jr', 'Kevin De Bruyne', 'Luka Modrić', 'Sergio Ramos', 'Giorgio Chiellini',
        'Gianluigi Buffon', 'Peter Schmeichel', 'Lev Yashin', 'Paolo Rossi'
    ]
    return random.choice(FOOTBALL_PLAYER_LIST)

def get_random_8_letters() -> str:
    return '#' + ''.join(random.choices(string.ascii_uppercase, k=8))

def get_random_8_symbols():
    SYMBOL_LIST = [
        "§", "¶", "†", "‡", "•", "◘", "○", "◙", "♂", "♀", "♪", "♫", "☼",
        "►", "◄", "↕", "‼", "↨", "↑", "↓", "→", "←", "∟", "↔", "▲", "▼",
        "⌂", "⌐", "⌠", "⌡", "─", "│", "┌", "┐", "└", "┘", "├", "┤", "┬", "┴",
        "┼", "╞", "╟", "╚", "╔", "╩", "╦", "╠", "═", "╬", "╧", "╨", "╤", "╥",
        "╙", "╘", "╒", "╓", "╫", "╪", "┘", "┌", "█", "▄", "▌", "▐", "▀", "■",
        "☺", "☻", "♥", "♦", "♣", "♠", "◘", "○", "◙", "♂", "♀", "♪", "♫",
        "☼", "►", "◄", "↕", "‼", "↨", "↑", "↓", "→", "←", "∟", "↔", "▲", "▼",
        "⌀", "⌂", "⌅", "⌆", "⌘", "⌚", "⌨", "⎋", "⎌", "⏏", "␣", "␤",
        "☠", "☢", "☣", "⚡", "❄", "☯", "⚛", "♾", "⚧", "☭", "⚔", "⛧", "⛤",
        "⛥", "⛦", "⛨", "🜁", "🜂", "🜃", "🜄", "🜅", "🜆", "🜇", "🜈", "🜉", "🜊",
        "🜋", "🜌", "⚒", "⚓", "⚔", "⚕", "⚖", "⚗", "⚘", "⚙", "⚚", "⚛", "⚜",
        "⚠", "⚡", "⚧", "⚨", "⚩", "⚰", "⚱", "⚲", "⚳", "⚴", "⚵", "⚶", "⚷"
    ]
    return '#' + ''.join(random.choices(SYMBOL_LIST, k=8))

def get_random_name():
    NAME_LIST = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
        'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
        'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
        'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
        'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
        'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
        'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
        'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
        'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez'
    ]
    return random.choice(NAME_LIST)

def get_random_list(type: str, n: int) -> list:
    TYPE_MAP = {
        'football_player': get_random_football_player,
        '8_letters': get_random_8_letters,
        '8_symbols': get_random_8_symbols,
        'name': get_random_name,
    }
    generator = TYPE_MAP.get(type)
    if generator is None:
        raise ValueError(f"Unknown type '{type}'. Available types: {list(TYPE_MAP.keys())}")
    return [generator() for _ in range(n)]


if __name__ == '__main__':
    print(get_random_football_player())
    print(get_random_football_player())
    print(get_random_football_player())
    print(get_random_football_player())
    print(get_random_football_player())
    
    print(get_random_8_letters())
    print(get_random_8_letters())
    print(get_random_8_letters())
    print(get_random_8_letters())
    print(get_random_8_letters())

    print(get_random_8_symbols())
    print(get_random_8_symbols())
    print(get_random_8_symbols())
    print(get_random_8_symbols())
    print(get_random_8_symbols())

    print(get_random_name())
    print(get_random_name())
    print(get_random_name())
    print(get_random_name())
    print(get_random_name())
