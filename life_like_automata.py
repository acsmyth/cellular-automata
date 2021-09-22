import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time

rows, cols = 300, 300

grid = [['X' if random.random() < 0.5 else '-' for q in range(cols)] for q in range(rows)]

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

rule = 'B4678/S35678'

birth_rule = [int(e) for e in list(rule[1:rule.index('/')])]
survival_rule  = [int(e) for e in list(rule[rule.index('/')+2:])]

print('Rule:')
print(rule)

def gen_possible_rules(n):
    max_digits = len(int_to_bin_str(2**n - 1))
    ret = []
    for q in range(2**n - 1, -1, -1):
        ret.append(int_to_bin_str(q, max_digits))
    return ret

def get_neighbors(r, c):
    ret = [[r, c-1], [r, c+1], [r+1, c], [r+1, c-1], [r+1, c+1], [r-1, c], [r-1, c-1], [r-1, c+1]]
    for i in range(len(ret)):
        nei = ret[i]
        ret[i] = [nei[0] % rows, nei[1] % cols]
    return ret


w, h = 700, 700
pygame.init()
pygame.display.set_caption('Automata')
screen = pygame.display.set_mode([w, h])


def display_grid(grid):
    cellW = w / cols
    cellH = h / rows
    pygame.draw.rect(screen, (255,255,255), (0, 0, cols * cellW, rows * cellH))
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'X':
                col = (0,0,0)
                pygame.draw.rect(screen, col, (c * cellW, r * cellH, cellW+1, cellH+1))

display_grid(grid)
gens = 999999999999
for q in range(gens):
    new_grid = [[0 for z in range(cols)] for z in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(r,c)
            cur_alive = grid[r][c] == 'X'
            nei_alive = 0
            for i in range(len(neighbors)):
                nei = neighbors[i]
                nei_alive += 1 if grid[nei[0]][nei[1]] == 'X' else 0
            if not cur_alive and nei_alive in birth_rule:
                new_grid[r][c] = 'X'
            elif cur_alive and nei_alive not in survival_rule:
                new_grid[r][c] = '-'
            else:
                new_grid[r][c] = grid[r][c]
            # else it stays in the same state
    grid = new_grid

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    display_grid(grid)
    pygame.display.flip()

pygame.quit()


