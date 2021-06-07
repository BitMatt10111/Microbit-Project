import random
import sys
import pygame
dim=20

CELL_SIZE = 20
BLACK = (0,0,0) #RGB
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,0,255)

class Cell():
    def __init__(self,id):
        self.id=id
        self.n=1
        self.s=1
        self.e=1
        self.w=1

def adjacencyDictionary(maze):
    aD={}
    for i in range(0,len(maze)): #y - row
        for k in range(0,len(maze[0])):  #x - column
            temp=[]
            if i != 0:
                temp.append(maze[i-1][k])
            if k != 0:
                temp.append(maze[i][k-1])
            if i != len(maze)-1:
                temp.append(maze[i+1][k])
            if k != len(maze[i])-1:
                temp.append(maze[i][k+1])
            aD[maze[i][k]]=temp
    return aD 

def allVisited(adjList,viewedCells):
    ret=True
    for cell in adjList:
        if not(cell in viewedCells):
            ret=False
    return ret

def createMaze():
    global dim
    maze=[]
    viewedCells=[]
    i=0
    for _ in range(dim):
        listRow=[]
        for _ in range(dim):
            cellObj=Cell(i)
            i+=1
            listRow.append(cellObj)
        maze.append(listRow)
    cell=maze[int(random.uniform(0,dim-1))][int(random.uniform(0,dim-1))]
    viewedCells.append(cell)
    adjDict=adjacencyDictionary(maze)
    while len(viewedCells)<dim*dim:
        adjList=adjDict[cell]
        if allVisited(adjList,viewedCells)!=True:
            while True:
                inc=1
                randomAdjCell=adjList[int(random.uniform(0,len(adjList)-1))]
                if not(randomAdjCell in viewedCells):
                    break
                else:
                    adjList.remove(randomAdjCell)
            if cell.id+dim==randomAdjCell.id:
                cell.s=0
                randomAdjCell.n=0
            if cell.id-dim==randomAdjCell.id:
                cell.n=0
                randomAdjCell.s=0
            if cell.id+1==randomAdjCell.id:
                cell.e=0
                randomAdjCell.w=0
            if cell.id-1==randomAdjCell.id:
                cell.w=0
                randomAdjCell.e=0
            viewedCells.append(randomAdjCell)
            cell=randomAdjCell
        else:
            cell=viewedCells[-inc]
            inc+=1
    return maze

def drawMaze(maze):
    global screen
    pygame.init()
    i=0
    k=0
    dimension=(dim*dim,dim*dim)
    screen = pygame.display.set_mode(dimension)
    screen.fill(BLACK)
    for y in range(0,dimension[0],dim):
        for x in range(0,dimension[0],dim):
            cell=maze[i][k]
            if cell.s==1:
                pygame.draw.line(screen, WHITE, (x,y+dim), (x+dim,y+dim),2)
            if cell.n==1:
                pygame.draw.line(screen, WHITE, (x,y), (x+dim,y),2)
            if cell.w==1:
                pygame.draw.line(screen, WHITE, (x,y), (x,y+dim),2)
            if cell.e==1:
                pygame.draw.line(screen, WHITE, (x+dim,y), (x+dim,y+dim),2)
            k+=1
        k=0
        i+=1

def main():
    maze=createMaze()
    while True:
        drawMaze(maze)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__=="__main__":
    main()