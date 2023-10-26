import socket
import pygame

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_sock.connect(('192.168.91.65', 1234))

def find(s):
    s = s[1:len(s) - 1]
    mas = s.split(';')
    return mas

pygame.init()
all_sprites = pygame.sprite.Group()
Ball_sprites = pygame.sprite.Group()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

running = True
clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, color):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color(color),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.add(Ball_sprites)

while running:

    otvet = ''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            otvet += str(x) + ' ' + str(y)

    screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    all_sprites.update()
    all_sprites.remove(i for i in all_sprites)
    Ball_sprites.remove(i for i in Ball_sprites)

    pygame.display.flip()

    try:
        client_sock.send(otvet.encode())
    except:
        pass

    try:
        data = client_sock.recv(1024**2).decode()
        data = find(data)
        count = 0
        for i in data:
            count += 1
            ball_data = i.split()
            ball_data[3] = ball_data[3][1:len(ball_data[3]) - 1]
            ball_data[4] = ball_data[4][0:len(ball_data[4]) - 1]
            ball_data[5] = ball_data[5][0:len(ball_data[5]) - 1]
            Ball(int(ball_data[0]), (int(ball_data[1])), (int(ball_data[2])), ((int(ball_data[3])), (int(ball_data[4])), (int(ball_data[5]))))
    except:
        pass

pygame.quit()