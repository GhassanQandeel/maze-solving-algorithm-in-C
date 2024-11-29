import API
import sys

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

def findGoal(maze, goal_cells, visited):
    # Initialize the starting position
    x, y = 15,0
    rows, cols = len(maze), len(maze[0])
#   16 , 16
    # Directions for moving: (dx, dy) -> up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#   to move the maze we should implement our maze so x,y is our current position for maze
#   if i need to move maze to up i will sub x by 1
#   if i need to move maze to down i will add x by 1
#   if i need to move maze to right i will add y by 1
#   if i need to move maze to left i will sub y by 1

    direction_names = ["N", "S", "W", "E"]



    while [x, y] not in goal_cells:
        log("Lets begin bro")

        nx, ny = x - 1, y
        sx, sy = x + 1 , y
        wx, wy = x , y - 1
        ex, ey = x , y + 1


        if isWall("S") and isWall("E") and isWall("W") and (maze[nx][ny] == maze[x][y] + 1):
            move("N")
            log("move(N)")
            x, y = nx, ny
            break
        elif isWall("S") and isWall("W") and (maze[nx][ny] == maze[x][y] + 1):
            pass

        break
        if [x, y] in goal_cells:
            log(f"Goal reached at ({x}, {y})!")
        else:
            log("Failed to reach the goal.")




def isWall(direction):
    if direction == "N":
        return API.wallFront()
    elif direction == "S":
        API.turnRight()
        API.turnRight()
        result = API.wallFront()
        API.turnRight()
        API.turnRight()
        return result
    elif direction == "W":
        API.turnLeft()
        result = API.wallFront()
        API.turnRight()
        return result
    elif direction == "E":
        API.turnRight()
        result = API.wallFront()
        API.turnLeft()
        return result
    return False

def move(direction):
    if direction == "N":
        API.moveForward()
    elif direction == "S":
        API.turnRight()
        API.turnRight()
        API.moveForward()
        API.turnRight()
        API.turnRight()
    elif direction == "W":
        API.turnLeft()
        API.moveForward()
        API.turnRight()
    elif direction == "E":
        API.turnRight()
        API.moveForward()
        API.turnLeft()

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
