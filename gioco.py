import pygame
import keyboard
import threading, queue
import serial, time
import time

pygame.init()



screen = pygame.display.set_mode((1920, 1080))
close=False
background_image = pygame.image.load("sfondo.jpg").convert()



class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True


rm = Read_Microbit()
rm.start()
pygame.init()
speed = [0, 0] 
q = queue.Queue()       

while not close:
    acc = q.get()
    screen.blit(background_image, [0, 0])
    pygame.display.update()

    if keyboard.is_pressed('q'):
        close=True

