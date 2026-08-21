import pygame
import random

# ১. Pygame শুরু করা
pygame.init()

# ২. স্ক্রিনের সাইজ ও শিরোনাম
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")

# ৩. রঙের কোড (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PINK = (255, 105, 180)

# ৪. পজিশন ও সাইজ
basket_width = 90
basket_height = 20
basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - 30 # ঝুড়ি একদম নিচে সামান্য উপরে সেট করা হয়েছে

# লাল বলের সেটিংস (স্পিড একটু বেশি)
ball_size = 20
ball_x = random.randint(0, WIDTH - ball_size)
ball_y = -50
ball_speed = 7

# অনেকগুলো ফুলের তালিকা তৈরি (ফুলগুলো সাধারণ বস্তু হিসেবে নিচে পড়বে)
flower_colors = [YELLOW, ORANGE, PINK]
flowers = []
for i in range(5): # একসাথে ৫টি ফুল পড়বে
    flowers.append({
        'x': random.randint(0, WIDTH - 20),
        'y': random.randint(-400, 0),
        'speed': random.randint(4, 6),
        'color': random.choice(flower_colors)
    })

score = 0
lives = 3
game_over = False

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# ৫. গেম লুপ
running = True
while running:
    clock.tick(30) # ৩০ FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # স্ক্রিন টাচ করে ঝুড়ি সরানো
        if pygame.mouse.get_pressed()[0]:
            touch_x = pygame.mouse.get_pos()[0]
            basket_x = touch_x - basket_width // 2

        # ঝুড়ি যাতে স্ক্রিনের বাইরে না যায়
        if basket_x < 0:
            basket_x = 0
        if basket_x > WIDTH - basket_width:
            basket_x = WIDTH - basket_width

        # লাল বল নিচে পড়া
        ball_y += ball_speed

        # ফুলগুলো নিচে পড়া
        for f in flowers:
            f['y'] += f['speed']
            if f['y'] > HEIGHT:
                f['y'] = random.randint(-100, 0)
                f['x'] = random.randint(0, WIDTH - 20)

        # লাল বল ধরার লজিক
        if (basket_y < ball_y + ball_size < basket_y + basket_height) and (basket_x < ball_x < basket_x + basket_width):
            score += 1
            ball_y = random.randint(-150, -50)
            ball_x = random.randint(0, WIDTH - ball_size)

        # লাল বল মিস করলে লাইফ কমানো (৩ বার মিস হলে গেম ওভার)
        if ball_y > HEIGHT:
            lives -= 1
            ball_y = random.randint(-150, -50)
            ball_x = random.randint(0, WIDTH - ball_size)
            if lives <= 0:
                game_over = True

    # স্ক্রিন রিফ্রেশ ও ড্রয়িং
    screen.fill((200, 230, 255))
    
    # ঝুড়ি আঁকা (একদম নিচে)
    pygame.draw.rect(screen, BROWN, (basket_x, basket_y, basket_width, basket_height))

    # ফুল আঁকা
    for f in flowers:
        pygame.draw.circle(screen, f['color'], (f['x'], f['y']), 12)

    # লাল বল আঁকা (যেটি ধরতে হবে)
    pygame.draw.circle(screen, RED, (ball_x + ball_size//2, ball_y + ball_size//2), ball_size//2)

    # স্কোর ও লাইফ দেখানো
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    lives_text = font.render("Lives: " + str(lives), True, (255, 0, 0))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # গেম ওভার মেসেজ
    if game_over:
        over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.update()

pygame.quit()