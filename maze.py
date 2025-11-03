from constants import MAZE_LAYOUT, MAZE_LAYOUT_ORIGINAL, MAZE_WIDTH, MAZE_HEIGHT

class Maze:    
    def __init__(self, layout=None):
        if layout is None:
            layout = MAZE_LAYOUT
        
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.cells = []
        
        for row in layout:
            row_str = row.rstrip('\n')
            row_cells = []
            for i in range(self.width):
                if i < len(row_str):
                    row_cells.append(row_str[i])
                else:
                    row_cells.append(' ')
            self.cells.append(row_cells)
        
        while len(self.cells) < self.height:
            self.cells.append([' '] * self.width)
        
        if len(self.cells) > self.height:
            self.cells = self.cells[:self.height]
    
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return ' '
    
    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = value
    
    def is_wall(self, x, y):
        return self.get_cell(x, y) == '#'
    
    def is_dot(self, x, y):
        return self.get_cell(x, y) == '.'
    
    def is_power_pellet(self, x, y):
        return self.get_cell(x, y) == 'o'
    
    def is_walkable(self, x, y):
        cell = self.get_cell(x, y)
        return cell != '#'
    
    def can_move(self, x, y, direction):
        dx, dy = direction.value
        cell_x = int(x)
        cell_y = int(y)
        new_x = cell_x + dx
        new_y = cell_y + dy
        return self.is_walkable(new_x, new_y)
    
    def eat_dot(self, x, y):
        cell = self.get_cell(x, y)
        if cell == '.' or cell == 'o':
            self.set_cell(x, y, ' ')
            return cell
        return None
    
    def count_dots(self):
        count = 0
        for row in self.cells:
            count += row.count('.') + row.count('o')
        return count
    
    def reset(self, layout=None):
        if layout is None:
            layout = MAZE_LAYOUT_ORIGINAL
        self.__init__(layout)
    
    def get_layout(self):
        return [row[:] for row in self.cells]

