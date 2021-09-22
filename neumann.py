import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import sys

rows, cols = 100, 100
grid = [['X' if random.random() < 0.05 else '-' for q in range(cols)] for q in range(rows)]

def int_to_bin_str(n, ln=0):
    ret = '{0:b}'.format(n)
    ret = ret.replace('1', 'X').replace('0', '-')
    if len(ret) < ln:
        ret = ('-' * (ln-len(ret))) + ret
    return ret

def ran_bin_str(ln):
    ret = ''
    for q in range(ln):
        ret += 'X' if random.random() < 0.5 else '-'
    return ret

rng = 1
num_neighbors = (rng+1) ** 2 + rng ** 2 - 1
rule = ran_bin_str(2 ** num_neighbors)

def gen_possible_rules(n):
    max_digits = len(int_to_bin_str(2**n - 1))
    ret = []
    for q in range(2**n - 1, -1, -1):
        ret.append(int_to_bin_str(q, max_digits))
    return ret

def get_neighbors(r, c, rng):
    ret = []
    row_n = 0
    for row in range(r - rng, r + rng + 1):
        for col in range(c + abs(row_n - rng) - rng, c + rng - abs(row_n - rng) + 1):
            if r == row and c == col: continue
            r0 = row % rows
            c0 = col % cols
            ret.append([r0, c0])
        row_n += 1
    return ret

def random_grid(per):
    return [['X' if random.random() < per else '-' for c in range(cols)] for r in range(rows)]

w, h = 700, 700
pygame.init()
pygame.display.set_caption('Automata')
screen = pygame.display.set_mode([w, h])


def display_grid(grid):
    cellW = w / cols
    cellH = h / rows
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            col = (0,0,0) if grid[r][c] == 'X' else (255,255,255)
            pygame.draw.rect(screen, col, (c * cellW, r * cellH, cellW, cellH))

perms_dict = {}
perms = gen_possible_rules(num_neighbors)
for i in range(len(perms)):
    perms_dict[perms[i]] = i


cool_rules = ['XXXXXX-XX--X----', 'XX-X--XXXX---XX-', '-X--X-X-X--XX-X-', 'X---X---X-X-XX-X', 'X-----XX--X----X', 'XXXXX----X-XXXX-',
              '--X-XXXXX--XXX-X', 'XXXXXXXX-XX-----', '--X-XXX-----XX--', 'XXX-X---X---XXX-']
rule = cool_rules[0]
ticks_per_rule = 40
print('Rule: ' + rule)

grid = random_grid(0.30)
display_grid(grid)
gens = 999999999999
for q in range(gens):
    if q % ticks_per_rule == ticks_per_rule-1:
        if cool_rules.index(rule)+1  >= len(cool_rules):
            cool_rules.append(ran_bin_str(2 ** num_neighbors))
            grid = random_grid(0.5)
        rule = cool_rules[cool_rules.index(rule)+1]
        print('Rule: ' + rule)
    new_grid = [[0 for z in range(cols)] for z in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(r,c,rng)
            on_off_bin_str = ''
            for i in range(len(neighbors)):
                nei = neighbors[i]
                on_off_bin_str += str(grid[nei[0]][nei[1]])
            idx = perms_dict[on_off_bin_str]
            new_grid[r][c] = rule[idx]
    grid = new_grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    display_grid(grid)
    pygame.display.flip()

pygame.quit()


