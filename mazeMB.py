import sys
import serial, time
import threading, queue
import time
import random
import sys
import pygame

dim=28
dimension=(dim*dim,dim*dim)
screen = pygame.display.set_mode(dimension)
clock = pygame.time.Clock()
background_image = pygame.image.load("sfondo.jpg").convert()

BLACK = (0,0,0) #RGB
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
dt = 1
gamma = 0.05
q = queue.Queue()

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM5"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            acc = [float(x) for x in data[1:-3].split(",")]
            q.put(acc)
            time.sleep(0.01)

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
    cell=maze[int(random.uniform(0,dim))][int(random.uniform(0,dim))]
    start=maze[int(random.uniform(0,dim))][0]
    end=maze[int(random.uniform(0,dim))][dim-1]
    viewedCells.append(cell)
    adjDict=adjacencyDictionary(maze)
    while len(viewedCells)<dim*dim:
        adjList=adjDict[cell]
        if allVisited(adjList,viewedCells)!=True:
            while True:
                inc=1
                randomAdjCell=adjList[int(random.uniform(0,len(adjList)))]
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
    return maze,[start,end]

def drawMaze(maze,specialCells):
    global screen
    pygame.init()
    i=0
    k=0
    screen.blit(background_image, [0, 0])
    for y in range(0,dimension[0],dim):
        for x in range(0,dimension[0],dim):
            cell=maze[i][k]
            if cell.id==specialCells[0].id:
                tile = pygame.Rect(x,y,dim,dim)
                pygame.draw.rect(screen,GREEN,tile)
                specialCells[0].x=x
                specialCells[0].y=y
            if cell.id==specialCells[1].id:
                tile = pygame.Rect(x,y,dim,dim)
                pygame.draw.rect(screen,RED,tile)
                specialCells[1].x=x
                specialCells[1].y=y
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

def ballF(specialCells):
    start=specialCells[0]
    end=specialCells[1]
    pygame.draw.circle(screen,RED,[start.x+dim/2,],dim/4,False)
    pygame.draw.circle(screen,GREEN,[end.x+dim/2,end.y+dim/2],dim/4,False)

def main():
    rm = Read_Microbit()
    rm.start()
    speed = [0, 0]

    specialCells=[]
    maze,specialCells=createMaze()

    ball = pygame.image.load("intro_ball.gif")
    ball = pygame.transform.scale(ball, (15, 15))
    ballrect = ball.get_rect()
    ballrect.centerx = 100
    ballrect.centery = 100
    while True:
        drawMaze(maze,specialCells)

        acc = q.get()
        speed[0] = (1.-gamma)*speed[0] + dt*acc[0]/1024.
        speed[1] = (1.-gamma)*speed[1] + dt*acc[1]/1024.
        q.task_done()
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > dimension[0]:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > dimension[1]:
            speed[1] = -speed[1]
        
        screen.blit(ball, ballrect)
        pygame.display.flip()
        clock.tick(10)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    rm.terminate()
                    rm.join()
                    pygame.quit()
                    sys.exit()

if __name__=="__main__":
    main()