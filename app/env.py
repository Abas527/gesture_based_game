import pygame
import random
import sys


pygame.init()

size = width, height = 800,600
player_width=40
player_height=40
ground=0
player_x,player_y=400,height-player_height-20
player_speed=10
player_vel_x,player_vel_y=0,0
jump=-10


obstacle_width=70
obstacle_height=70
obstacle_speed=10
obstacles=[]
obstacle_timer=0

jump_obstacle_width=50
jump_obstacle_height=20
jump_obstacle_speed=10
jump_obstacles=[]
jump_obstacle_timer=0

gravity=0.3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Runner Game")

clock=pygame.time.Clock()

running=True
isjumping=False

score=0
font = pygame.font.SysFont(None, 40)

player_img=pygame.image.load("assets/pokemon_ball.png")
player_image=pygame.transform.scale(player_img,(player_width,player_height))
obstacle_image=pygame.image.load("assets/big_obstacle.png")
obstacle_image=pygame.transform.scale(obstacle_image,(obstacle_width,obstacle_height))

while(running):

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        
    screen.fill(WHITE)

    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_vel_x=-player_speed
    elif(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player_vel_x=player_speed
    else:
        player_vel_x=0
    

    if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not isjumping:
        isjumping=True
        player_vel_y=jump
    
    player_vel_y+=gravity
    player_y+=player_vel_y

    player_x+=player_vel_x

    if player_x<0:
        player_x=0
    
    if player_x > width-player_width:
        player_x=width-player_width
    
    if player_y >= height-player_height:
        player_y=height-player_height
        isjumping=False
        player_vel_y=0
    
    
    is_collide=False

    obstacle_timer+=1
    if obstacle_timer > random.randint(10,200):
        new_obstacle={
            "x":width,
            "y":height-obstacle_height,
            "width":obstacle_width,
            "height":obstacle_height
        }

        if len(jump_obstacles)!=0:
            obstacle_rect=pygame.Rect(new_obstacle['x'],new_obstacle['y'],new_obstacle['width'],new_obstacle['height'])
            for obstacle in jump_obstacles:
                jump_rect=pygame.Rect(obstacle['x'],obstacle['y'],obstacle['width'],obstacle['height'])

                if jump_rect.colliderect(obstacle_rect):
                    is_collide=True
                    break
        if not is_collide:
            obstacles.append(new_obstacle)
            obstacle_timer=0
    
    for obstacle in obstacles[:]:
        obstacle['x'] -= obstacle_speed
        
        if obstacle['x'] + obstacle['width'] < 0:
            obstacles.remove(obstacle)
            score+=1
    
    player_rect=pygame.Rect(player_x,player_y,player_width,player_height)

    for obstacle in obstacles:
        obstacle_rect=pygame.Rect(obstacle['x'],obstacle['y'],obstacle['width'],obstacle['height'])

        if player_rect.colliderect(obstacle_rect):
            print("Game over!!")
            print(f"SCRORE:{score}")
            running=False
    
    jump_obstacle_timer+=1
    
    if jump_obstacle_timer > random.randint(200,1000):
        new_obstacle={
            "x":width,
            "y":height-jump_obstacle_height-20,
            "width":jump_obstacle_width,
            "height":jump_obstacle_height
        }
        jump_rect=pygame.Rect(new_obstacle['x'],new_obstacle['y'],new_obstacle['width'],new_obstacle['height'])
        for obstacle in obstacles:
            obstacle_rect=pygame.Rect(obstacle['x'],obstacle['y'],obstacle['width'],obstacle['height'])

            if jump_rect.colliderect(obstacle_rect):
                is_collide=True
                break
        
        if not is_collide:

            jump_obstacles.append(new_obstacle)
            jump_obstacle_timer=0
    
    for obstacle in jump_obstacles[:]:
        obstacle['x'] -= jump_obstacle_speed
        
        if obstacle['x'] + obstacle['width'] < 0:
            jump_obstacles.remove(obstacle)
    
    player_rect=pygame.Rect(player_x,player_y,player_width,player_height)

    for obstacle in jump_obstacles:
        obstacle_rect=pygame.Rect(obstacle['x'],obstacle['y'],obstacle['width'],obstacle['height'])

        if player_rect.colliderect(obstacle_rect):
            isjumping=True
            score=score+100
            player_vel_y=jump-5
    
    pygame.draw.rect(screen,BROWN,(0,ground,width,height-ground))
    screen.blit(player_image,(player_x,player_y,player_width,player_height))
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
    
    for obstacle in jump_obstacles:
        pygame.draw.rect(screen, RED, (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
    
    
    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


    pygame.display.flip()
    clock.tick(30)

pygame.quit()