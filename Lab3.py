class Elevator:
    def __init__(self, floor):
        self.floor = floor
        self.steps = 0
        self.doorState = False
        self.lastCommand = "close_the_door"

    def default(self):
        self.end = 0
        self.steps = 0
        
    def go_up(self):
        self.floor += 1
        self.steps += 1
        self.lastCommand = "go_up"
        return "Go up"
    
    def go_down(self):
        self.floor -= 1
        self.steps += 1
        self.lastCommand = "go_down"
        return "Go down"

    def open_the_door(self):
        self.doorState = True
        self.lastCommand = "open_the_door"
        return "Open the door"

    def close_the_door(self):
        self.doorState = False
        self.lastCommand = "close_the_door"
        return "Close the door"

    def analyze(self, command):
        try:
            return self.Commands[(self.lastCommand, command)](self)
        except KeyError:
            raise Exception(f"Команда не существует: {command}")

    def open_or_not(self):
        return self.doorState

    Commands = { 
        ("close_the_door", "open_the_door"): open_the_door,
        ("go_up", "open_the_door"): open_the_door,
        ("go_down", "open_the_door"): open_the_door,

        ("open_the_door", "go_up"): close_the_door,
        ("close_the_door","go_up"): go_up,
        ("go_up","go_up"): go_up, 

        ("open_the_door","go_down"): close_the_door,
        ("close_the_door","go_down"): go_down,
        ("go_down","go_down"): go_down, 
    }

def create_space(floors = 4, FloorForFirstEl = 1, FloorForSecondEl = 3):
    first_or_second = [[1] * floors for _ in range(floors)]

    actions = {} 
    for i in range(1, floors+1): 
        actions[(i, i)] = "open_the_door"

    for i in range(1, floors+1):
        for j in range(i+1, floors+1):
            first_or_second[i-1][j-1] = 0
            actions[(i, j)] = "go_up"
            actions[(j, i)] = "go_down"

    elevators = [Elevator(FloorForFirstEl), Elevator(FloorForSecondEl)]
    return actions, first_or_second, elevators

def move_elevator_to_floor(elevator, target_floor, actions):
    while (elevator.floor != target_floor) or (not elevator.open_or_not()):
        print(f"|{elevator.floor}|", end=' ')
        action = actions.get((elevator.floor, target_floor)) 
        result = elevator.analyze(action) 
        print(result, end=' ')

calls = (
    (2, 4), (1, 2), (3, 1), (2, 2), (1, 3), 
    (4, 1), (3, 2), (1, 4), (2, 1), (3, 3)
)
actions, first_or_second, elevators = create_space()

for call in calls:
    n, m = abs(call[0] - elevators[0].floor), abs(call[0] - elevators[1].floor)
    num = first_or_second[n][m]
    elevators[num].default()

    print(f'Лифт #{num+1} С этажа №{call[0]} на этаж №{call[1]}', end = '\n\t')

    move_elevator_to_floor(elevators[num], call[0], actions)
    move_elevator_to_floor(elevators[num], call[1], actions)

    print(f'\n\tЭтажей пройдено -- {elevators[num].steps} --')
