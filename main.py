from abc import ABC, abstractmethod
from reprint import output
import time

class Matrix:
    def __init__(self, width_in, height_in):
        self.width = width_in
        self.height = height_in
        self.rows = self._create_empty_matrix()

    def _create_empty_matrix(self):
        _matrix = []
        for r in range(self.width):
            row = []
            for h in range(self.height):
                row.append((False if ((h + r) % 6 == 0) else True)) # FOR TEST ONLY
                # row.append(False)
            _matrix.append(row)
        return _matrix
    
    def next_step(self):
        for x in range(len(self.rows)):
            row = self.rows[x]
            for y in range(len(row)):
                # iterate on this decision
                self.rows[x][y] = not self.rows[x][y]

class MatrixRenderer(ABC):
    # Eventually we will have one for CLI output, and one for Raspberry Pi output
    @abstractmethod
    def generate_output(self, matrix, output_obj):
        pass

class CLIMatrixRenderer(MatrixRenderer):
    def generate_output(self, matrix, output_obj, i):
        header = "--" + ("---" * (matrix.width))
        for pos in range(len(output_obj)-1, 0, -1):
            output_obj.remove(output_obj[pos])
        for row in matrix.rows:
            
            output_obj.append((f"HELLO  -  {i}"))

        # print(header)
        # for row in matrix.rows:
        #     row_str = "|"
        #     for item in row:
        #         row_str += (("   " if item else " X "))
        #     row_str += "|"
        #     print(row_str)
        # print(header)

class GOL:
    def __init__(self, dimension_in=20, total_steps_in=10):
        self.matrix = Matrix(width_in=dimension_in, height_in=dimension_in)
        self.total_steps = total_steps_in

        renderer = CLIMatrixRenderer()  # eventually will change for rasp pi

        with output(output_type="list", initial_len=dimension_in) as output_list:
            for i in range(self.total_steps):
                time.sleep(1)
                # self.matrix.next_step()
                renderer.generate_output(self.matrix, output_list, i)
                # print(i)

def main():
    print("starting game")
    gol = GOL()
    print("Game Complete :)")

main()