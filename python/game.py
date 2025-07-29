import pygame
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 100
GRID_PADDING = 10
GRID_COUNT = 4

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# 字体设置
font = pygame.font.Font(None, 50)

# 生成初始棋盘
def generate_board():
    board = [[0] * GRID_COUNT for _ in range(GRID_COUNT)]
    add_new_tile(board)
    add_new_tile(board)
    return board

# 在棋盘上添加一个新的随机数字
def add_new_tile(board):
    empty_tiles = [(i, j) for i in range(GRID_COUNT) for j in range(GRID_COUNT) if board[i][j] == 0]
    if empty_tiles:
        x, y = random.choice(empty_tiles)
        board[x][y] = random.choice([2, 4])

# 绘制棋盘
def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_COUNT):
        for j in range(GRID_COUNT):
            value = board[i][j]
            color = EMPTY_TILE_COLOR if value == 0 else TILE_COLORS.get(value, BLACK)
            pygame.draw.rect(screen, color, (j * (GRID_SIZE + GRID_PADDING), i * (GRID_SIZE + GRID_PADDING), GRID_SIZE, GRID_SIZE))
            if value != 0:
                text = font.render(str(value), True, BLACK if value < 16 else WHITE)
                text_rect = text.get_rect(center=(j * (GRID_SIZE + GRID_PADDING) + GRID_SIZE // 2, i * (GRID_SIZE + GRID_PADDING) + GRID_SIZE // 2))
                screen.blit(text, text_rect)

# 合并行或列
def merge(line):
    non_zero = [x for x in line if x != 0]
    merged = []
    skip = False
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged.append(2 * non_zero[i])
            skip = True
        else:
            merged.append(non_zero[i])
    return merged + [0] * (GRID_COUNT - len(merged))

# 移动棋盘
def move(board, direction):
    new_board = [row[:] for row in board]
    if direction == 'up':
        for j in range(GRID_COUNT):
            column = [board[i][j] for i in range(GRID_COUNT)]
            new_column = merge(column)
            for i in range(GRID_COUNT):
                new_board[i][j] = new_column[i]
    elif direction == 'down':
        for j in range(GRID_COUNT):
            column = [board[i][j] for i in range(GRID_COUNT)][::-1]
            new_column = merge(column)[::-1]
            for i in range(GRID_COUNT):
                new_board[i][j] = new_column[i]
    elif direction == 'left':
        for i in range(GRID_COUNT):
            new_row = merge(board[i])
            new_board[i] = new_row
    elif direction == 'right':
        for i in range(GRID_COUNT):
            new_row = merge(board[i][::-1])[::-1]
            new_board[i] = new_row
    return new_board

# 检查游戏是否结束
def is_game_over(board):
    for i in range(GRID_COUNT):
        for j in range(GRID_COUNT):
            if board[i][j] == 0:
                return False
            if i > 0 and board[i][j] == board[i - 1][j]:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]:
                return False
            if i < GRID_COUNT - 1 and board[i][j] == board[i + 1][j]:
                return False
            if j < GRID_COUNT - 1 and board[i][j] == board[i][j + 1]:
                return False
    return True

# 主循环
def main():
    board = generate_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_board = move(board, 'up')
                elif event.key == pygame.K_DOWN:
                    new_board = move(board, 'down')
                elif event.key == pygame.K_LEFT:
                    new_board = move(board, 'left')
                elif event.key == pygame.K_RIGHT:
                    new_board = move(board, 'right')
                else:
                    continue

                if new_board != board:
                    board = new_board
                    add_new_tile(board)

                if is_game_over(board):
                    print("Game Over!")
                    running = False

        draw_board(board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()