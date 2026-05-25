import pygame
import random
import cv2
import mediapipe as mp
import math
import numpy as np

width=1600 
height=900

pygame.init()
screen=pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Frutas da fruteira")
clock=pygame.time.Clock()

cap=cv2.VideoCapture(0)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)


#class particulas
class Particles:
    def __init__ (self,x,y):
        self.x=x
        self.y=y
        self.size=random.randint(1,6)
        self.speed_x=random.randint(-9,0)
        self.speed_y=random.randint(-9,0)
        self.life=12
    def move(self):
        self.x+=self.speed_x
        self.y+=self.speed_y
        self.life-=1
    def draw(self):
        pygame.draw.circle(screen,(255,255,255),(int(self.x),int(self.y)),self.size)

# variaveis

particles=[]
trail_points=[]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
    success, frame=cap.read()
    if success:
        window_width=screen.get_width()
        window_height=screen.get_height()
        frame=cv2.resize(frame,(window_width, window_height))
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(rgb)
        frame=np.rot90(rgb)
        frame_surface=pygame.surfarray.make_surface(frame)
        screen.blit(frame_surface,(0,0))

        #indicador
        if results.multi_hand_landmarks:
            hand_landmarks=results.multi_hand_landmarks[0]
            tip=hand_landmarks.landmark[8]
            raw_x=screen.get_width()-int(tip.x*screen.get_width())
            raw_y=int(tip.y*screen.get_height())
            if len(trail_points)>0:
                last_x,last_y=trail_points[-1]
                smooth_x=int(last_x+(raw_x-last_x)*0.35)
                smooth_y=int(last_y+(raw_y-last_y)*0.35)
            else:
                smooth_x=raw_x
                smooth_y=raw_y
            trail_points.append((smooth_x,smooth_y))
    # rastro
    if len(trail_points)>12:
        trail_points.pop(0)
    # rastro
    for i in range(1,len(trail_points)):
        start=trail_points[i-1]
        end=trail_points[i]
        pygame.draw.line(screen,(120,120,120),start,end,20)
        pygame.draw.line(screen,(220,220,220),start,end,12)
        pygame.draw.line(screen,(255,255,255),start,end,5)
    pygame.display.update()
    clock.tick(60)
cap.release()
pygame.quit()