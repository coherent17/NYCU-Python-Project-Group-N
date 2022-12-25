import pygame
import random
from tkinter import *
from tkinter import messagebox
from utils import *
from pygame import mixer

# data.append(cur_data)
filename = r"C:\Users\Davon\Desktop\University\Semester 3\Lab on Python for Data Science and Machine Learning\Final Project\audio\Major_2.wav"
mixer.init()
mixer.music.load(filename)

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Figure:
    figures = [ 
        [[1, 5, 9,13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6,10]],
        [[1, 2, 6,10], [5, 6, 7, 9], [2, 6,10,11], [3, 5, 6, 7]],  
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

game_w = 10
game_h = 25

class Game:
    def __init__(self, x, y):  
        self.x = x
        self.y = y
        self.block_size = 30
        self.state = "start"
        self.figure = None
        self.score = 0
        self.level = 1.25
        self.key_guess = -1
        self.field = [[0 for j in range(game_w)] for i in range(game_h)]

    def new_figure(self, x = 3, y = 0):
        self.figure = Figure(x, y)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > game_h - 1 or \
                            j + self.figure.x > game_w - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, game_h):
            zeros = 0
            for j in range(game_w):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(game_w):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

# Music part

song_names_path = 'link.csv'
val_data_path = 'val_data.csv'

val_data = pd.read_csv(val_data_path)
val_data.set_index('Index')
song_names = pd.read_csv(song_names_path)
song_names.set_index('Index')



p1 = Game(225, 50)
p2 = Game(975, 50)

counter = 0
fps = 60
zoom = 28
done = False
music_played = False

mixer.init()
mixer.music.set_volume(0.2)
pygame.init()
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 800))
row, name, scale = get_song(val_data, song_names)

while not done:
    if p1.state == 'start' and p2.state == 'start':
        if p1.figure is None:
            p1.new_figure(3, 0)

        if p2.figure is None:
            p2.new_figure(3, 0)

        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // p1.level // 2) == 0:
            if p1.state == "start":
                p1.go_down()

            if p2.state == "start":
                p2.go_down()

        if not music_played:
            mixer.music.load("audio\\"+name)
            mixer.music.play()
            music_played = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_w:
                #     p1.rotate()
                if event.key == pygame.K_s:
                    p1.go_space()
                if event.key == pygame.K_a:
                    p1.go_side(-1)
                if event.key == pygame.K_d:
                    p1.go_side(1)
                if event.key == pygame.K_e:
                    p1.key_guess = 1
                if event.key == pygame.K_q:
                    p1.key_guess = 0

                # if event.key == pygame.K_UP:
                #     p2.rotate()
                if event.key == pygame.K_k:
                    p2.go_space()
                if event.key == pygame.K_j:
                    p2.go_side(-1)
                if event.key == pygame.K_l:
                    p2.go_side(1)
                if event.key == pygame.K_u:
                    p2.key_guess = 1
                if event.key == pygame.K_o:
                    p2.key_guess = 0

                if p1.key_guess == scale:
                    p1.rotate()
                    row, name, scale = get_song(val_data, song_names)
                    p1.key_guess = -1
                    p2.key_guess = -1
                    music_played = False
                elif p2.key_guess == scale:
                    p2.rotate()
                    row, name, scale = get_song(val_data, song_names)
                    p1.key_guess = -1
                    p2.key_guess = -1
                    music_played = False
        
    
            
    screen.fill(WHITE)

    for i in range(game_h):
        for j in range(game_w):
            pygame.draw.rect(screen, GRAY, [p1.x + zoom * j, p1.y + zoom * i, zoom, zoom], 1)
            pygame.draw.rect(screen, GRAY, [p2.x + zoom * j, p2.y + zoom * i, zoom, zoom], 1)
            if p1.field[i][j] > 0:
                pygame.draw.rect(screen, colors[p1.field[i][j]],
                                [p1.x + zoom * j + 1, p1.y + zoom * i + 1, zoom - 2, zoom - 1])
            if p2.field[i][j] > 0:
                pygame.draw.rect(screen, colors[p2.field[i][j]],
                                [p2.x + zoom * j + 1, p2.y + zoom * i + 1, zoom - 2, zoom - 1])

    if p1.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in p1.figure.image():
                    pygame.draw.rect(screen, colors[p1.figure.color],
                                    [p1.x + zoom * (j + p1.figure.x) + 1,
                                    p1.y + zoom * (i + p1.figure.y) + 1,
                                    zoom - 2, zoom - 2])
    
    if p2.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in p2.figure.image():
                    pygame.draw.rect(screen, colors[p2.figure.color],
                                    [p2.x + zoom * (j + p2.figure.x) + 1,
                                    p2.y + zoom * (i + p2.figure.y) + 1,
                                    zoom - 2, zoom - 2])


    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(p1.score), True, BLACK)
    text2 = font.render("Score: " + str(p2.score), True, BLACK)
    

    screen.blit(text, [p1.x-100, p1.y-50])
    screen.blit(text2, [p2.x-100, p2.y-50])
    if p1.state == "gameover" or p2.state == "gameover":
        if p1.score == p2.score:
            text_winner = font1.render("Draw!", True, (180, 34, 22))
        else:
            if p1.score > p2.score:
                winner = "Player 1"
            else:
                winner = "Player 2"
            text_winner = font1.render(winner + " win!", True, (180, 34, 22))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        p1.state = "gameover"
        p2.state = "gameover"
        screen.blit(text_winner, [670, 200])
        pygame.display.flip()
        clock.tick(fps)
    pygame.display.flip()
    clock.tick(fps)