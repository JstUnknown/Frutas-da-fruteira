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

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

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


cap.release()
#pygame.quit()