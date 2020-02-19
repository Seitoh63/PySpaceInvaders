import time

import pygame
pygame.init()

s1=pygame.mixer.Sound("sound/fastinvader1.wav")
s2=pygame.mixer.Sound("sound/fastinvader2.wav")
s3=pygame.mixer.Sound("sound/fastinvader3.wav")
s4=pygame.mixer.Sound("sound/fastinvader4.wav")

pygame.display.set_mode()

delay =0.5
ch = pygame.mixer.Channel(1)
while True:

    ch.play(s1)
    time.sleep(delay)
    ch.play(s2)
    time.sleep(delay)
    ch.play(s3)
    time.sleep(delay)
    ch.play(s4)
    time.sleep(delay)