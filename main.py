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

WHITE=(255,255,255)
fruits_images={
    "apple":{
        "whole": pygame.image.load("assets/blueberry.png").convert_alpha(),
        "cut": pygame.image.load("assets/sliced_buleberry.png").convert_alpha(),
    },
}

#class fruta
class Fruit:
    def __init__ (self):
        self.type=random.choice(list(fruits_images.keys()))
        self.x=random.randint(100, width-100)
        self.y=height+50
        self.size=random.randint(100,140)
        self.speed_x=random.randint(-5,5)
        self.speed_y=random.randint(-25,-15)
        self.gravity=0.5
        self.sliced=False
        self.slice_time=15
        self.radius=self.size//2
    def move (self):
        self.x+=self.speed_x
        self.y+=self.speed_y
        self.speed_y+=self.gravity
        if self.sliced:
            self.slice_time-=1
    def draw (self):
        if not self.sliced:
            image=fruits_images[self.type]["whole"]
        else: 
            image=fruits_images[self.type]["cut"]
        image=pygame.transform.scale(image,(self.size,self.size))
        rect=image.get_rect(center=(self.x,self.y))
        screen.blit(image,rect)
    def off_screen(self):
        return self.y>screen.get_height()+100


#lass particulas
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
fruits=[]
particles=[]
trail_points=[]
spawn_timer=0
running=True
score=0
font = pygame.font.SysFont("Arial", 40)
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
    
    #frutas 
    spawn_timer+=1
    if spawn_timer>20:
        fruits.append(Fruit())
        spawn_timer=0
    for fruit in fruits[:]:
        fruit.move()
        fruit.draw()
        if not fruit.sliced:
            for point in trail_points:
                distance=math.hypot(fruit.x-point[0], fruit.y-point[1])
                if distance<fruit.radius:
                    fruit.sliced=True
                    for _ in range(25):
                        particles.append(Particles(fruit.x,fruit.y))
                    score+=1
                    break
        if fruit.sliced and fruit.slice_time<=0:
            fruits.remove(fruit)
        elif fruit.off_screen():
            fruits.remove(fruit)
    #particulas
    for particle in particles [:]:
        particle.move()
        particle.draw()
        if particle.life<=0:
            particles.remove(particle)
    
    #score
    score_text= font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(15,15))

    pygame.display.update()
    clock.tick(60)
cap.release()
pygame.quit()