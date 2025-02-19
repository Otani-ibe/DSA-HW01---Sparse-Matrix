class SparseMatrix:
    def __init__(self, rows=None, cols=None, file_path=None):
        self.rows = 0
        self.cols = 0
        self.data = {}  # {(row, col): value}

        if file_path:
            self.load_from_file(file_path)
        elif rows is not None and cols is not None:
            self.rows = rows
            self.cols = cols
        else:
            raise ValueError("Provide either a file path or matrix dimensions.")

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f]
                self.rows = int(lines[0].split('=')[1])
                self.cols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    if line:
                        line = line.replace(" ", "")
                        if not (line.startswith('(') and line.endswith(')')):
                            raise ValueError("Invalid file format.")
                        row, col, value = map(int, line[1:-1].split(','))
                        self.set_element(row, col, value)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except ValueError as e:
            raise ValueError(f"Invalid file format: {e}")

    def set_element(self, row, col, value):
        self.data[(row, col)] = value

    def get_element(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data.get((row, col), 0)
        raise IndexError("Index out of bounds.")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")
        result = SparseMatrix(self.rows, self.cols)
        for (row, col), value in self.data.items():
            result.set_element(row, col, value + other.get_element(row, col))
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")
        result = SparseMatrix(self.rows, self.cols)
        for (row, col), value in self.data.items():
            result.set_element(row, col, value - other.get_element(row, col))
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix multiplication requires first matrix's columns to match second matrix's rows.")
        result = SparseMatrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                sum_val = sum(self.get_element(i, k) * other.get_element(k, j) for k in range(self.cols))
                if sum_val:
                    result.set_element(i, j, sum_val)
        return result

    def print_readable(self, max_rows=10, max_cols=10):
        print(f"Matrix ({self.rows}x{self.cols})")
        for i in range(min(self.rows, max_rows)):
            print(" ".join(str(self.get_element(i, j)).rjust(5) for j in range(min(self.cols, max_cols))))
        if self.rows > max_rows or self.cols > max_cols:
            print("...")


def main():
    operation = input("Enter operation (Add, Subtract, Multiply): ").strip().lower()
    matrix1 = SparseMatrix(file_path='../sample_input/matrixfile1.txt')
    matrix2 = SparseMatrix(file_path='../sample_input/matrixfile3.txt')
    
    operations = {"add": matrix1.add, "subtract": matrix1.subtract, "multiply": matrix1.multiply}
    
    if operation in operations:
        result = operations[operation](matrix2)
        print("Result:")
        result.print_readable()
    else:
        print("Invalid operation. Please enter Add, Subtract, or Multiply.")

if __name__ == "__main__":
    main()
