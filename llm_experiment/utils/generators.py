import random
import string


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

LETTER_LIST = string.ascii_uppercase

SYMBOL_LIST = [
    'ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ', 'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ',
    'հ', 'ձ', 'ղ', 'ճ', 'մ', 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ', 'ռ', 'ս', 'վ',
    'տ', 'ր', 'ց', 'ւ', 'փ', 'ք', 'օ', 'ֆ',
]

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



def get_random_name():
    return random.choice(NAME_LIST)


def get_random_football_player(n: int = 1) -> str:
    if n == 1:
        return random.choice(FOOTBALL_PLAYER_LIST)

    random_list = random.sample(FOOTBALL_PLAYER_LIST, k=n)

    return '[' + ', '.join(list(map(lambda s: '"' + s + '"', random_list))) + ']'

def get_random_letter(n: int = 1) -> str:
    if n == 1:
        return random.choice(LETTER_LIST)

    random_list = random.sample(LETTER_LIST, k=n)

    return '[' + ', '.join(list(map(lambda s: '"' + s + '"', random_list))) + ']'

def get_random_symbol(n: int = 1) -> str:
    if n == 1:
        return random.choice(SYMBOL_LIST)

    random_list = random.sample(SYMBOL_LIST, k=n)

    return '[' + ', '.join(list(map(lambda s: '"' + s + '"', random_list))) + ']'
