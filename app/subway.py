import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import random
from opencv.conn import shared


def get_commands():
    
    cmd= shared.get_command()

    if cmd is None:
        return False,"None"
    else:
        return True,cmd



def run_game():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Subway Style Runner")
    player_img=pygame.image.load("assets/pokemon_ball.png")
    obstacle_img=pygame.image.load("assets/obstacle.png")
    big_obstacle_img=pygame.image.load("assets/big_obstacle.png")

    clock = pygame.time.Clock()

    player_width = 50
    player_height = 50
    player_y = HEIGHT - player_height - 20

    lanes = [200, 400, 600]
    player_lane = 1
    player_x = lanes[player_lane]


    is_jumping = False
    player_vel_y = 0
    jump_force = -10
    gravity = 0.5
    clear_jump=HEIGHT-player_height-50

    obstacle_width = 100
    obstacle_height = 60
    obstacle_speed = 6
    obstacles = []
    obstacle_timer = 0


    big_obstacle_width = 200
    big_obstacle_height = 120
    big_obstacle_speed = 6
    big_obstacles = []
    big_obstacle_timer = 0

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (50, 50, 255)
    RED = (255, 0, 0)


    player_img=pygame.transform.scale(player_img,(player_width,player_height))
    obstacle_img=pygame.transform.scale(obstacle_img,(obstacle_width,obstacle_height))
    big_obstacle_img=pygame.transform.scale(big_obstacle_img,(big_obstacle_width,big_obstacle_height))


    score = 0
    font = pygame.font.SysFont(None, 40)

    running = True
    while running:

        clock.tick(60)
        screen.fill(BLUE)

        is_command,cmd=get_commands()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key==pygame.K_a) and player_lane > 0:
                    player_lane -= 1
                if (event.key == pygame.K_RIGHT or event.key==pygame.K_d) and player_lane < 2:
                    player_lane += 1
                if (event.key == pygame.K_UP or event.key==pygame.K_SPACE) and not is_jumping:
                    is_jumping = True
                    player_vel_y = jump_force
        if is_command:
            if cmd=="JUMP":
                is_jumping = True
                player_vel_y = jump_force
            if cmd=="LEFT" and player_lane < 2:
                player_lane += 1
            if cmd=="RIGHT" and player_lane > 0:
                player_lane -= 1
                

        player_x = lanes[player_lane]

        if is_jumping:
            player_y += player_vel_y
            player_vel_y += gravity
        

            if player_y >= HEIGHT - player_height - 20:
                player_y = HEIGHT - player_height - 20
                is_jumping = False
                player_vel_y = 0


        obstacle_timer += 1
        if obstacle_timer > random.randint(200, 400):
            lane = random.randint(0, 100)%3
            obstacles.append({
            "x": lanes[lane],
            "y": -60
            })
            obstacle_timer = 0


        for obs in obstacles:
            obs["y"] += obstacle_speed

        for obs in obstacles[:]:
            if obs["y"] > HEIGHT:
                obstacles.remove(obs)
                score += 1
    
        big_obstacle_timer += 1
        if big_obstacle_timer > random.randint(500, 1000):
            lane = random.randint(0, 20)%3
            big_obstacles.append({
                "x": lanes[lane],
                "y": -60
            })
            big_obstacle_timer = 0


        for obs in big_obstacles:
            obs["y"] += big_obstacle_speed

        for obs in big_obstacles[:]:
            if obs["y"] > HEIGHT:
                big_obstacles.remove(obs)
                score += 1

        player_rect = pygame.Rect(
            player_x - player_width // 2,
            player_y,
            player_width,
            player_height
        )

        for obs in obstacles:
            obs_rect = pygame.Rect(
                obs["x"] - obstacle_width // 2,
                obs["y"],
                obstacle_width,
                obstacle_height
            )
            if player_y > clear_jump:
                player_rect.height=player_height//2

                if player_rect.colliderect(obs_rect):
                    print("Game Over!")
                    print("Score:", score)
                    running = False
    
        obstacle_speed+=0.001

        for obs in big_obstacles:
            obs_rect = pygame.Rect(
                obs["x"] - big_obstacle_width // 2,
                obs["y"],
                big_obstacle_width,
                big_obstacle_height
            )
        
            if player_rect.colliderect(obs_rect):
                    print("Game Over!")
                    print("Score:", score)
                    running = False
        big_obstacle_speed+=0.001

        pygame.draw.line(screen, BLACK, (300, 0), (300, HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (500, 0), (500, HEIGHT), 2)


        screen.blit(player_img,(player_x - player_width // 2, player_y, player_width, player_height))

        for obs in obstacles:
            screen.blit(obstacle_img,(obs["x"] - obstacle_width // 2, obs["y"], obstacle_width, obstacle_height) )
    
        for obs in big_obstacles:
            screen.blit(big_obstacle_img,(obs["x"] - big_obstacle_width // 2, obs["y"], big_obstacle_width, big_obstacle_height) )

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
    
    pygame.quit()
    sys.exit()



