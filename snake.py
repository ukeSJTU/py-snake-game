class Snake:
    def __init__(self, length, direction, colors, width_px, height_px):
        self.length = length
        self.direction = direction
        self.colors = colors
        self.width_px = width_px
        self.height_px = height_px
        self.snake_pos = [[width_px // 2, height_px // 2]]
        self.snake_direction = direction

    def draw_snake(self):
        return [(self.snake_pos[i], self.colors[i]) for i in range(self.length)]
