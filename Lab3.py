class Elevator:
    def __init__(self, floor):
        self.floor = floor
        self.lastCommand = "close_the_door"
        self.door = False
        self.end = 0
        self.steps = 0
        
    def move_up(self):
        self.floor += 1
        self.steps += 1
        self.lastCommand = "move_up"
        return "Move up"
    
    def move_down(self):
        self.floor -= 1
        self.steps += 1
        self.lastCommand = "move_down"
        return "Move down"

    def open_the_door(self):
        self.door = True
        self.end = 1
        self.lastCommand = "open_the_door"
        return "Open the door"

    def close_the_door(self):
        self.door = False
        self.lastCommand = "close_the_door"
        return "Close the door"
    
    def close_the_door_and_go(self):
        self.door = False
        self.end = 1
        self.lastCommand = "close_the_door"
        return "Close the door"

    def analyze(self, command):
        try:
            return self.Commands[(self.lastCommand, command)](self)
        except KeyError:
            raise Exception(f"Несуществующая комманда: {command}")

    def open_or_not(self):
        return self.door

    Commands = { 
        ("close_the_door", "open_the_door"): open_the_door,
        ("move_up", "open_the_door"): open_the_door,
        ("move_down", "open_the_door"): open_the_door,

        ("open_the_door", "open_the_door"): close_the_door_and_go,

        ("open_the_door", "move_up"): close_the_door,
        ("close_the_door","move_up"): move_up,
        ("move_up","move_up"): move_up, 

        ("open_the_door","move_down"): close_the_door,
        ("close_the_door","move_down"): move_down,
        ("move_down","move_down"): move_down, 
    }

def CreateSpace(floors = 4, FirstFl = 1, SecondFl = 1):
    first_or_second = [[1] * floors for _ in range(floors)]

    actions = {} 
    for i in range(1, floors+1): 
        actions[(i, i)] = "open_the_door"

    for i in range(1, floors+1):
        for j in range(i+1, floors+1):
            first_or_second[i-1][j-1] = 0
            actions[(i, j)] = "move_up"
            actions[(j, i)] = "move_down"

    elevators = [Elevator(FirstFl), Elevator(SecondFl)]
    return actions, first_or_second, elevators

calls = ((2, 4), (1, 2), (3, 1), (2, 2), (1, 3))
actions, first_or_second, elevators = CreateSpace()

for call in calls:
    n, m = abs(call[0] - elevators[0].floor), abs(call[0] - elevators[1].floor)
    ElNum = first_or_second[n][m]

    elevators[ElNum].end = 0
    elevators[ElNum].steps = 0
    print("\n", f"({call[0]} --> {call[1]}) Лифт №{ElNum+1}", end='  ')

    while (elevators[ElNum].floor != call[1]) or (not elevators[ElNum].open_or_not()):
        print(f"|{elevators[ElNum].floor}|", end = ' ')

        action = actions.get((elevators[ElNum].floor, call[elevators[ElNum].end]))
        result = elevators[ElNum].analyze(action)
        print(result, end = ' ')

    print(f'\n Этажей пройдено -- {elevators[ElNum].steps} --', end = ' ')