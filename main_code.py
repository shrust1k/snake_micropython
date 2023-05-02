from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time 
import random
from default_parameters import *

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(id=1, scl=Pin(7), sda = Pin(6))
display = SSD1306_I2C(128, 64, i2c)

while (button.value()==1):
            
            display.fill(0)
            display.text("PRESS BUTTON TO", 5, 0, 1)
            display.text("START THE GAME!", 5, 8, 1)
            display.show()
            

while True:
    while (button.value()==1):
            
            display.fill(0)
            display.text("PRESS BUTTON!", 20, 0, 1)
            display.text("TO START THE GAME!", 20, 0, 1)
            display.show()
            time.sleep(1)
            
    #here
    score = 0
    body = 1
    heads_coordinates = [defaultX, defaultY]
    body_coordinates = [heads_coordinates]
    last_part = heads_coordinates
    gameOver = False
    start = False
    fruitX = 32
    fruitY = 32

    adcX = ADC(0)
    adcY = ADC(1)
    

    OldMin = 0 
    OldMax = 65536
    NewMin = 0 
    NewMax = 100

    minCord = 30
    maxCord = 70

    

    SPACE_SIZE = 8

    def direction(x,y,direction):
        if(x>minCord and x<maxCord and y<minCord):
            direction = "down"
        elif(x>minCord and x<maxCord and y>maxCord):
            direction = "up"
        elif(y>minCord and y<maxCord and x>maxCord):
            direction = "left"
        elif(y>minCord and y<maxCord and x<minCord):
            direction = "right"
        else:
            direction = direction
        """   
        if(x>maxCord):
            if(x>minCord and x<maxCord and y>maxCord):
                direction = "up"
            elif():
                
                
        elif(x<minCord):
            if(x>minCord and x<maxCord and y<minCord):
                direction = "down"
            
        elif(y>maxCord):
            if(y>minCord and y<maxCord and x<minCord):
                direction = "right"
            
        elif(y<minCord):
            if(y>minCord and y<maxCord and x>maxCord):
                direction = "left"
        """               
        return direction


    
            
        

    def coordinates(direction):
        occasion()
      
        global heads_coordinates, body_coordinates, last_part

        x_rect = heads_coordinates[0]
        y_rect = heads_coordinates[1]
        
        if (direction == "up"):
            y_rect+=SPACE_SIZE
        elif (direction == "down"):
            y_rect-=SPACE_SIZE
        elif (direction == "left"):
            x_rect+=SPACE_SIZE
        elif (direction == "right"):
            x_rect-=SPACE_SIZE
            
        if (x_rect<0):
            x_rect = GAME_WIDTH + x_rect
        elif(x_rect>GAME_WIDTH):
            x_rect = 0
            
        elif (y_rect<16):
            y_rect = GAME_HEIGHT + y_rect
        elif (y_rect>GAME_HEIGHT+SPACE_SIZE):
            y_rect = 0 + 16
            
        
        heads_coordinates = [x_rect, y_rect] 
        body_coordinates.insert(0,heads_coordinates)
        last_part = body_coordinates[-1]
        body_coordinates.pop()   
       
       


    def fruit():
        global fruitX, fruitY
        fruitX = random.randint(0,GAME_WIDTH//SPACE_SIZE)*SPACE_SIZE
        fruitY = random.randint(0,(GAME_HEIGHT-16)//SPACE_SIZE)*SPACE_SIZE+16

    def occasion():
        s = False
        global fruitX, fruitY, heads_coordinates, score, body, gameOver
        
        if (fruitX == heads_coordinates[0] and fruitY == heads_coordinates[1]):      
            score += 1
            body += 1
            body_coordinates.append(body_coordinates[-1])
            fruit()
            
                    
            
        for coordinate in body_coordinates[1:-1]:
            if coordinate == body_coordinates[0]:
                gameOver = True
            
        
            
    def draw(body_coordinates,fruitX,fruitY, score, body):
        x = body_coordinates[0][0]
        y = body_coordinates[0][1]
        display.fill(0)
        
        for i in body_coordinates:
            display.fill_rect(i[0], i[1], SPACE_SIZE,SPACE_SIZE, 1)
            
        display.text('SCORE:{score}'.format(score=score), 30, 0, 1)
        display.rect(fruitX, fruitY,SPACE_SIZE,SPACE_SIZE, 1)
        display.show()
        


    last_direction = default_direction


    
    while (gameOver==False):
        
        
        joystickX = round((((adcX.read_u16() - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
        joystickY = round((((adcY.read_u16() - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
        current_direction = direction(joystickX,joystickY,last_direction)
        
        print("Last direction: {last_dir}, current direction: {cur_dir}".format(last_dir = last_direction, cur_dir = current_direction))
        
        if (current_direction == "up" and last_direction == "down" or current_direction=="down" and last_direction=="up"):
            current_direction = last_direction
  
        elif (current_direction == "right" and last_direction == "left" or current_direction=="left" and last_direction=="right"):
            current_direction = last_direction

        
        last_time = time.ticks_ms()
        
        
        draw(body_coordinates, fruitX, fruitY, score, body)
               
        #print("{direction} Rects cords:{listx}".format( direction =current_direction, listx = body_coordinates ))
        coordinates(current_direction)
        last_direction = current_direction
        while (time.ticks_ms()-last_time<SPEED):
            pass    
            
       
            
            
    else:
        while (button.value()==1):   
            display.fill(0)
            display.text("PRESS BUTTON", 5, 0, 1)
            display.text("TO TRY AGAIN!", 5, 8, 1)
            display.show()

        else:
            gameOver = False
        
 



