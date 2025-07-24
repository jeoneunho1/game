import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚽ 미니 축구 게임")

clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)

# 플레이어와 공 클래스
player = pygame.Rect(100, HEIGHT//2 - 25, 50, 50)
ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
goal = pygame.Rect(WIDTH - 30, HEIGHT//2 - 60, 20, 120)

ball_speed = [5, 3]

def reset():
    player.x = 100
    player.y = HEIGHT//2 - 25
    ball.x = WIDTH//2 - 15
    ball.y = HEIGHT//2 - 15
    ball_speed[0] = 5 * random.choice([-1, 1])
    ball_speed[1] = 3 * random.choice([-1, 1])

# 게임 루프
running = True
score = 0

while running:
    clock.tick(60)
    screen.fill(GREEN)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.y < HEIGHT - 50:
        player.y += 5

    # 공 이동
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 공 튕김
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1

    # 충돌 판정
    if player.colliderect(ball):
        ball_speed[0] *= -1

    # 골 판정
    if ball.colliderect(goal):
        score += 1
        reset()

    # 화면 그리기
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, RED, goal)
    pygame.display.flip()

pygame.quit()
