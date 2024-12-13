class Elevator:
    def __init__(self, floor):
        self.floor = floor
        self.lastCommand = "CloseDoor"
        self.door = False
        self.end = 0
        self.steps = 0
        
    def MoveUp(self):
        self.floor += 1
        self.steps += 1
        self.lastCommand = "MoveUp"
        print("MoveUp", end = ' ')
    
    def MoveDown(self):
        self.floor -= 1
        self.steps += 1
        self.lastCommand = "MoveDown"
        print("MoveDown", end = ' ')

    def OpenDoor(self):
        self.door = True
        self.UpEnd()
        self.lastCommand = "OpenDoor"
        print("OpenDoor", end = ' ')
    
    def UpEnd(self):
        self.end = 1

    def CloseDoor(self):
        self.door = False
        self.lastCommand = "CloseDoor"
        print("CloseDoor", end = ' ')

    def Analyze(self, command):
        try:
            self.Commands[(self.lastCommand, command)](self)
        except KeyError:
            raise Exception(f"Несуществующая комманда: {command}")

    def OpenOrNot(self):
        return self.door

    Commands = { 
        ("CloseDoor", "OpenDoor"): OpenDoor,
        ("MoveUp", "OpenDoor"): OpenDoor,
        ("MoveDown", "OpenDoor"): OpenDoor,
        ("OpenDoor", "OpenDoor"): UpEnd,

        ("OpenDoor", "MoveUp"): CloseDoor,
        ("CloseDoor","MoveUp"): MoveUp,
        ("MoveUp","MoveUp"): MoveUp, 

        ("OpenDoor","MoveDown"): CloseDoor,
        ("CloseDoor","MoveDown"): MoveDown,
        ("MoveDown","MoveDown"): MoveDown, 
    }

#создание списка действий и массива n*m 
# n растояние до 1 лифта
# m растояние до 2 лифта
# 0 - вызываем первый лифт, 1 - вызываем второй лифт
n = 4
distance = [[1] * n for _ in range(n)]

def generate_actions(n):
    actions = {} 
    for i in range(1, n+1): 
        for j in range(i, n+1): 
            actions[(i, j)] = "OpenDoor"
            actions[(j, i)] = "OpenDoor"

    for i in range(1, n+1):
        for j in range(i+1, n+1):
            distance[i-1][j-1] = 0
            actions[(i, j)] = "MoveUp"
            actions[(j, i)] = "MoveDown"
    return actions

actions = generate_actions(n)

calls = ((2, 4), (1, 2), (3, 1), (2, 2), (1, 3))
elevators = [Elevator(1), Elevator(1)]

for call in calls:
    n, m = abs(call[0] - elevators[0].floor), abs(call[0] - elevators[1].floor)
    ElNum = distance[n][m]

    elevators[ElNum].end = 0
    elevators[ElNum].steps = 0
    print("\n", f"({call[0]} --> {call[1]}) Лифт №{ElNum+1}", end='  ')

    while (elevators[ElNum].floor != call[1]) or (not elevators[ElNum].OpenOrNot()):

        print(f"_{elevators[ElNum].floor}_", end = ' ')

        a = actions.get((elevators[ElNum].floor, call[elevators[ElNum].end]))
        elevators[ElNum].Analyze(a)

    print(f" |Лифт №{ElNum+1} прошел {elevators[ElNum].steps} этажей|", end = ' ')
