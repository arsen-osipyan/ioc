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
