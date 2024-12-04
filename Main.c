#include <stdio.h>
#include <stdlib.h>
#include "API.h"

// Define directions
#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

// Maze dimensions
#define MAZE_SIZE 16

// Define Goal
#define goalX MAZE_SIZE/2-1 // Set the goal X-coordinate
#define goalY MAZE_SIZE/2-1 // Set the goal Y-coordinate

// Cell structure
typedef struct {
    int distance;
    unsigned char walls; // bits: [0]=North, [1]=East, [2]=South, [3]=West
} Cell;

// Maze array
Cell maze[MAZE_SIZE][MAZE_SIZE];

// Current state of the robot
int x = 0, y = 0;           // Current position
int direction = NORTH;      // Current direction

// Log helper
void log(char* text) {
    fprintf(stderr, "%s\n", text);
    fflush(stderr);
}

// Initialize the maze distances
void initMaze() {
    for (int i = 0; i < MAZE_SIZE; i++) {
        for (int j = 0; j < MAZE_SIZE; j++) {
            maze[i][j].walls = 0;
            maze[i][j].distance = abs(i - goalX) + abs(j - goalY);
        }
    }
}

// Check if the current cell is the goal
int isGoal(int x, int y) {
    return (x == goalX && y == goalY);
}

// Update position based on direction
void updatePosition() {
    switch (direction) {
        case NORTH: y++; break;
        case EAST:  x++; break;
        case SOUTH: y--; break;
        case WEST:  x--; break;
    }
}

// Turn the robot to the left
void turnLeft() {
    API_turnLeft();
    direction = (direction + 3) % 4; // Counter-clockwise
}

// Turn the robot to the right
void turnRight() {
    API_turnRight();
    direction = (direction + 1) % 4; // Clockwise
}

// Turn the robot around
void turnAround() {
    turnRight();
    turnRight();
}

// Update walls based on sensor readings
void updateWalls() {
    if (API_wallFront()) {
        int dir = direction;
        maze[x][y].walls |= (1 << dir);
        int nx = x, ny = y;
        switch (dir) {
            case NORTH: ny++; if (ny < MAZE_SIZE) maze[nx][ny].walls |= (1 << SOUTH); break;
            case EAST: nx++; if (nx < MAZE_SIZE) maze[nx][ny].walls |= (1 << WEST); break;
            case SOUTH: ny--; if (ny >= 0) maze[nx][ny].walls |= (1 << NORTH); break;
            case WEST: nx--; if (nx >= 0) maze[nx][ny].walls |= (1 << EAST); break;
        }
    }
    if (API_wallLeft()) {
        int dir = (direction + 3) % 4;
        maze[x][y].walls |= (1 << dir);
        int nx = x, ny = y;
        switch (dir) {
            case NORTH: ny++; if (ny < MAZE_SIZE) maze[nx][ny].walls |= (1 << SOUTH); break;
            case EAST: nx++; if (nx < MAZE_SIZE) maze[nx][ny].walls |= (1 << WEST); break;
            case SOUTH: ny--; if (ny >= 0) maze[nx][ny].walls |= (1 << NORTH); break;
            case WEST: nx--; if (nx >= 0) maze[nx][ny].walls |= (1 << EAST); break;
        }
    }
    if (API_wallRight()) {
        int dir = (direction + 1) % 4;
        maze[x][y].walls |= (1 << dir);
        int nx = x, ny = y;
        switch (dir) {
            case NORTH: ny++; if (ny < MAZE_SIZE) maze[nx][ny].walls |= (1 << SOUTH); break;
            case EAST: nx++; if (nx < MAZE_SIZE) maze[nx][ny].walls |= (1 << WEST); break;
            case SOUTH: ny--; if (ny >= 0) maze[nx][ny].walls |= (1 << NORTH); break;
            case WEST: nx--; if (nx >= 0) maze[nx][ny].walls |= (1 << EAST); break;
        }
    }
}

// Floodfill algorithm to update distances
void floodFill() {
    int changed = 1;
    // Keep looping untill no change on the distance happened
    while (changed) {
        changed = 0;
        for (int i = 0; i < MAZE_SIZE; i++) {
            for (int j = 0; j < MAZE_SIZE; j++) {
                if (isGoal(i, j)) {
                    if (maze[i][j].distance != 0) {
                        maze[i][j].distance = 0;
                        changed = 1;
                    }
                } else {
                    int minNeighbor = 255; // Max possible distance
                    // Check all neighbors
                    if (!(maze[i][j].walls & (1 << NORTH)) && j < MAZE_SIZE - 1) {
                        if (maze[i][j + 1].distance + 1 < minNeighbor)
                            minNeighbor = maze[i][j + 1].distance + 1;
                    }
                    if (!(maze[i][j].walls & (1 << EAST)) && i < MAZE_SIZE - 1) {
                        if (maze[i + 1][j].distance + 1 < minNeighbor)
                            minNeighbor = maze[i + 1][j].distance + 1;
                    }
                    if (!(maze[i][j].walls & (1 << SOUTH)) && j > 0) {
                        if (maze[i][j - 1].distance + 1 < minNeighbor)
                            minNeighbor = maze[i][j - 1].distance + 1;
                    }
                    if (!(maze[i][j].walls & (1 << WEST)) && i > 0) {
                        if (maze[i - 1][j].distance + 1 < minNeighbor)
                            minNeighbor = maze[i - 1][j].distance + 1;
                    }
                    if (maze[i][j].distance != minNeighbor) {
                        maze[i][j].distance = minNeighbor;
                        changed = 1;
                    }
                }
            }
        }
    }
}

// Get the direction with the minimum distance
int getMinDirection() {
    int minDist = 255;
    int dir = -1;
    // Check all possible directions
    if (!(maze[x][y].walls & (1 << NORTH)) && y < MAZE_SIZE - 1) {
        if (maze[x][y + 1].distance < minDist) {
            minDist = maze[x][y + 1].distance;
            dir = NORTH;
        }
    }
    if (!(maze[x][y].walls & (1 << EAST)) && x < MAZE_SIZE - 1) {
        if (maze[x + 1][y].distance < minDist) {
            minDist = maze[x + 1][y].distance;
            dir = EAST;
        }
    }
    if (!(maze[x][y].walls & (1 << SOUTH)) && y > 0) {
        if (maze[x][y - 1].distance < minDist) {
            minDist = maze[x][y - 1].distance;
            dir = SOUTH;
        }
    }
    if (!(maze[x][y].walls & (1 << WEST)) && x > 0) {
        if (maze[x - 1][y].distance < minDist) {
            minDist = maze[x - 1][y].distance;
            dir = WEST;
        }
    }
    return dir;
}

// Move the robot to the next cell in the given direction
void moveTo(int nextDir) {
    int turn = (nextDir - direction + 4) % 4;
    if (turn == 0) {
    // Do nothing
    } else if (turn == 1) {
        turnRight();
    } else if (turn == 2) {
        turnAround();
    } else if (turn == 3) {
        turnLeft();
    }
    API_moveForward();
    updatePosition();
    direction = nextDir;
}

// Main logic
int main(int argc, char* argv[]) {
     log("Running...");
    initMaze();
    API_setColor(0, 0, 'G');
    API_setText(0, 0, "Start");
    
    while (1) {
        // Update walls
        updateWalls();
        // Recalculate distances
        floodFill();
        // Check if goal
        if (isGoal(x, y)) {
            log("Goal reached!");
            API_setColor(x, y, 'G');
            API_setText(x, y, "Goal");
            break;
        }
        // Decide next move
        int nextDir = getMinDirection();
        if (nextDir == -1) {
            log("No path found!");
            break;
        }
        // Move to next cell
        moveTo(nextDir);
        // Update the color
        API_setColor(x, y, 'Y');
    }
    return 0;
}

