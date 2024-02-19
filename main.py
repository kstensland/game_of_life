from abc import ABC, abstractmethod
from reprint import output
import time
import copy


class Matrix:
    def __init__(self, width_in, height_in, starting_grid=None):
        self.width = width_in
        self.height = height_in
        self.rows = self._create_starting_matrix(starting_grid=(starting_grid or []))

    def _create_starting_matrix(self, starting_grid):
        _matrix = []
        for r in range(self.width):
            row = []
            for h in range(self.height):
                row.append(False)
            _matrix.append(row)

        for coords in starting_grid:
            x = coords[0]
            y = coords[1]
            _matrix[x][y] = True

        return _matrix

    def _get_neighbors(self, x, y):
        RELATIVE_POSITIONS = [-1, 0, 1]
        neighbor_cells = []

        for relative_x in RELATIVE_POSITIONS:
            relative_row = x + relative_x
            if relative_row < 0 or relative_row >= self.width:
                continue
            for relative_y in RELATIVE_POSITIONS:
                relative_col = y + relative_y
                if relative_row == x and relative_col == y:
                    # we don't want to count the actual cell
                    continue
                if relative_col < 0 or relative_col >= self.height:
                    continue
                neighbor_cells.append((relative_row, relative_col))
        return neighbor_cells
    
    def _get_active_neighbors_count(self, neighbors):
        count = 0
        for coords in neighbors:
            x = coords[0]
            y = coords[1]
            if self.rows[x][y]:
                count += 1
        return count

    def next_step(self):
        new_grid = copy.deepcopy(self.rows)
        for x in range(len(self.rows)):
            row = self.rows[x]
            for y in range(len(row)):
                # iterate on this decision
                neighbors = self._get_neighbors(x, y)
                active_neighbors_count = self._get_active_neighbors_count(neighbors)
                is_cell_active = self.rows[x][y]

                if is_cell_active:
                    # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
                    if active_neighbors_count < 2:
                        new_grid[x][y] = False
                
                    # Any live cell with more than three live neighbors dies, as if by overpopulation.
                    if active_neighbors_count > 3:
                        new_grid[x][y] = False

                    # Any live cell with two or three live neighbors lives on to the next generation.
                else:
                    #Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
                    if active_neighbors_count in [2, 3]:
                        new_grid[x][y] = True
        self.rows = new_grid


class MatrixRenderer(ABC):
    # Eventually we will have one for CLI output, and one for Raspberry Pi output
    @abstractmethod
    def generate_output(self, matrix, output_obj):
        pass


class CLIMatrixRenderer(MatrixRenderer):
    def generate_output(self, matrix, output_obj):
        # empty out the output object
        for pos in range(len(output_obj)-1, 0, -1):
            output_obj.remove(output_obj[pos])

        vertical_border = "--" + ("---" * (matrix.width))
        output_obj.append(vertical_border)

        for row in matrix.rows:
            row_str = "|"
            for item in row:
                row_str += ((" X " if item else "   "))
            row_str += "|"
            output_obj.append(row_str)

        # bottom border
        output_obj.append(vertical_border)


class GOL:
    def __init__(self, dimension_in=20, total_steps_in=0, starting_grid=None):
        self.matrix = Matrix(width_in=dimension_in, height_in=dimension_in, starting_grid=starting_grid)
        self.total_steps = total_steps_in

        renderer = CLIMatrixRenderer()  # eventually will change for rasp pi

        with output(output_type="list", initial_len=dimension_in) as output_list:
            # Show starting setup
            renderer.generate_output(self.matrix, output_list)
            time.sleep(1)

            # Iterate through game
            for i in range(self.total_steps):
                time.sleep(0.5)
                self.matrix.next_step()
                renderer.generate_output(self.matrix, output_list)


def main():
    print("starting game")
    start=[(4, 3), (5, 4), (6, 2), (6, 3), (6, 4)]
    gol = GOL(starting_grid=start)
    print("Game Complete :)")

main()