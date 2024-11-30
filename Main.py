import API
import sys

direction_map = {
    "N": (0, -1),  # Move up (decrease y by 1)
    "S": (0, 1),  # Move down (increase y by 1)
    "W": (-1, 0),  # Move left (decrease x by 1)
    "E": (1, 0)  # Move right (increase x by 1)
}
direction_map_maze = {
    "N": (0, 1),  # Move up (decrease y by 1)
    "S": (0, -1),  # Move down (increase y by 1)
    "W": (-1, 0),  # Move left (decrease x by 1)
    "E": (1, 0)  # Move right (increase x by 1)
}

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def setValuesInMaze(maze):
    for i in range(0,len(maze)):
        for j in range(0,len(maze[0])):
            API.setText(i,j,maze[i][j])

def initialize_matrix(goal_cells, maze, visited):
    for cell in goal_cells:
        maze[cell[0]][cell[1]] = 0  # Goal cells have distance 0
        visited[cell[0]][cell[1]] = True

def bfs_propagation(goal_cells, maze, visited, rows, cols):
    queue = goal_cells[:]  # Initialize BFS queue with all goal cells

    while queue:
        x, y = queue.pop(0)

        # Check all neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # Ensure the neighbor is within bounds and not visited
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny]:
                # Update distance and mark as visited
                maze[nx][ny] = maze[x][y] + 1
                visited[nx][ny] = True
                queue.append([nx, ny])


def isWall(direction):
    if direction == "N":
        return API.wallFront()
    elif direction == "S":
        return API.wallBack()
    elif direction == "W":
        return API.wallLeft()
    elif direction == "E":
        return API.wallRight()
    return False


def move(direction):
    if direction == "N":
        API.moveForward()
    elif direction == "S":
        API.turnRight()
        API.turnRight()
        API.moveForward()
    elif direction == "W":
        API.turnLeft()
        API.moveForward()
    elif direction == "E":
        API.turnRight()
        API.moveForward()


def checkWalls():
    direction_names = ["N", "S", "W", "E"]
    possible_moves = []
    for d in direction_names:
        if not isWall(d):
            possible_moves.append(d)
    return possible_moves


def Check_move(maze, x, y, x_matrix, y_matrix, visited):
    stuck = False
    possible_moves = checkWalls()
    # log("Debug")
    # log(" ")
    # log(" ")
    # log(f"{} ")
    # log(f"{} ")
    # log(" ")
    # log(" ")
    # log("Debug")


    # here we will check what the possible to do if not return false


    for pm in possible_moves:
        if 0 <= x < 16 and 0 <= y < 16 and 0 <= x_matrix < 16 and 0 <= y_matrix < 16:

            next_move_distance_value_x = x_matrix + direction_map[pm][0]
            next_move_distance_value_y = y_matrix + direction_map[pm][1]
            log("Debug")
            log(" ")
            log(f"the next move {pm} ")
            log(f"value of current {maze[x_matrix][y_matrix]} ")
            log(f"nx {next_move_distance_value_x} ")
            log(f"yx {next_move_distance_value_y} ")
            log(f"next move value{maze[next_move_distance_value_x][next_move_distance_value_y]} ")
            log(" ")
            log("Debug")
            if 0 <= next_move_distance_value_x < 16 and 0 <= next_move_distance_value_y < 16 and 0 <= x_matrix < 16 and 0 <= y_matrix < 16:
                if not (maze[x_matrix][y_matrix] > maze[next_move_distance_value_x][next_move_distance_value_y]):
                    possible_moves.remove(pm)


    direction = []
    if len(possible_moves) == 0:
        stuck = True
    else:
        for d in possible_moves:
            direction.append(d)
        if "S" in direction:
            direction.remove("S")
        move(direction[0])
    return stuck, direction;


def findGoal(maze, goal_cells, visited):
    # Initialize the starting position
    x, y = 0,0
    x_matrix,y_matrix = 0,15

    rows, cols = len(maze), len(maze[0])

    while [x, y] not in goal_cells:
        log("Lets begin bro")
        log(f"({x},{y}) in the maze")
        log(f"There wall Right {isWall("E")}")
        log(f"There wall Left {isWall("W")}")
        log(f"There wall North {isWall("N")}")
        log(f"There wall South {isWall("S")}")
        log(f"manhatin distance for ({x},{y}) is {maze[x][y]}")
        log(f"matrix cordinate ({x_matrix},{y_matrix})")

        stuck,direction = Check_move(maze, x, y, x_matrix, y_matrix, visited)
        if len(direction) != 0:
            direction = direction[0]

        if stuck==True:
            log("Stuck")
        else:
            x=x+direction_map_maze[direction][0]
            y=y+direction_map_maze[direction][1]
            x_matrix=x_matrix+direction_map[direction][0]
            y_matrix=y_matrix+direction_map[direction][1]











def main():
    log("Running...")
    log("Ghassan_Qandeel_1212397")
    x, y = 0, 0
    API.setText(7, 7, "GOAL")
    API.setText(7, 8, "GOAL")
    API.setText(8, 7, "GOAL")
    API.setText(8, 8, "GOAL")

    API.setColor(7, 7, "R")
    API.setColor(7, 8, "R")
    API.setColor(8, 7, "R")
    API.setColor(8, 8, "R")
    API.setColor(x, y, "G")
    API.setText(x, y, "abc")
    goal_cells = [[7, 7], [7, 8], [8, 7], [8, 8]]

    rows, cols = 16, 16  # Typical Micro mouse maze size
    maze_Values = [[float('inf')] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    initialize_matrix(goal_cells, maze_Values, visited)
    #Here to find the manhaten distance fo all values before see walls for all
    bfs_propagation(goal_cells, maze_Values, visited, rows, cols)
    setValuesInMaze(maze_Values)



    findGoal(maze_Values,goal_cells,visited)


if __name__ == "__main__":
    main()
