import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def manhattan(point, target_point):
    return abs(point[0] - target_point[0]) + abs(point[1] - target_point[1])

def initialize_matrix(goal_cells,maze,maze_acc):
    for cell in goal_cells:
        maze[cell[0]][cell[1]]=0
        maze_acc[cell[0]][cell[1]]=True
def print_matrix(maze,rows,cols):
    for i in range(rows):
        print(maze[i])


def main():
    log("Running...")
    log("Ghassan_Qandeel_1212397")
    x,y =0,0
    API.setText(7,7,"GOAL")
    API.setText(7, 8, "GOAL")
    API.setText(8, 7, "GOAL")
    API.setText(8, 8, "GOAL")

    API.setColor(7, 7, "R")
    API.setColor(7, 8, "R")
    API.setColor(8, 7, "R")
    API.setColor(8, 8, "R")
    API.setColor(x, y, "G")
    API.setText(x, y, "abc")
    ###############################################


    goal_cells=[[7,7],[7,8],[8,7],[8,8]]

    rows, cols = 16, 16  # Typical Micro mouse maze size
    maze_Values = [[float('inf')] * cols for _ in range(rows)]
    maze_Acc_1 = [[False] * cols for _ in range(rows)]
    initialize_matrix(goal_cells,maze_Values,maze_Acc_1)
    print(")))))))))))))))))))))))))))))))))")
    print_matrix(maze_Values,rows,cols)
    print(")))))))))))))))))))))))))))))))))")
    print_matrix(maze_Acc_1,rows,cols)
    queue=[]
    queue.append([7,7])
    queue.append([7,8])
    queue.append([8,7])
    queue.append([8,8])

    for q in queue:
        x,y = q[0],q[1]
        if maze_Acc_1[x][y] == True:
            #Check for border
            if x != 0:
                x0 = x-1
            else:
                x0 = x
            if x != 15:
                x1 =x+1
            else:
                x1=x

            if y != 0:
                y0 = y-1
            else:
                y0 = y
            if y != 15:
                y1 = y+1
            else:
                y1 = y

            if maze_Acc_1[x0][y]==False:
                maze_Values[x0][y]=manhattan([x0,y],[x,y])
                maze_Acc_1[x0][y] =True
                queue.append([x0,y])
            if maze_Acc_1[x1][y]==False:
                maze_Values[x1][y] = manhattan([x1, y], [x,y])
                maze_Acc_1[x1][y] = True
                queue.append([x1,y])
            if maze_Acc_1[x][y0]==False:
                maze_Values[x][y0] = manhattan([x, y0], [x,y])
                maze_Acc_1[x][y0] = True
                queue.append([x,y0])
            if maze_Acc_1[x][y1]==False:
                maze_Values[x][y1] = manhattan([x, y1], [x, y])
                maze_Acc_1[x][y1] = True
                queue.append([x,y1])


if __name__ == "__main__":
    main()
