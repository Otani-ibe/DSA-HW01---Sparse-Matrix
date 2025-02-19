import os

class MatrixDimensionError(Exception):
    """Custom exception for matrix dimension mismatches."""
    pass

class MatrixIndexError(Exception):
    """Custom exception for invalid matrix indices."""
    pass

class SparseMatrix:
    """
    A memory-efficient sparse matrix implementation using a dictionary of dictionaries.
    
    Storage format: {row: {col: value}} storing only non-zero elements.
    
    Time Complexity:
    - Get/Set Element: O(1)
    - Addition/Subtraction: O(n)
    - Multiplication: O(n*m) (where n, m are non-zero elements in matrices)
    - CSR Conversion: O(n)
    """
    
    def __init__(self, source=None, rows=0, cols=0):
        self.data = {}  # {row: {col: value}}
        self.rows, self.cols = rows, cols
        self.nnz = 0
        
        if isinstance(source, str):
            self._load_from_file(source)
    
    def _load_from_file(self, file_path):
        """Load matrix from file with strict dimension checking."""
        try:
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
                
                try:
                    self.rows = int(lines[0].split('=')[1])
                    self.cols = int(lines[1].split('=')[1])
                except (IndexError, ValueError):
                    raise ValueError("Invalid dimension format in file.")
                
                for line in lines[2:]:
                    if not line.strip():
                        continue
                    try:
                        row, col, value = map(int, line.strip('()').split(','))
                        self.set_element(row, col, value)
                    except ValueError:
                        raise ValueError(f"Invalid numeric values in line: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Matrix file not found: {file_path}")
    
    def to_csr(self):
        """Convert matrix to Compressed Sparse Row (CSR) format."""
        values, col_indices, row_ptr = [], [], [0]
        count = 0
        
        for row in range(self.rows):
            if row in self.data:
                for col in sorted(self.data[row]):
                    values.append(self.data[row][col])
                    col_indices.append(col)
                    count += 1
            row_ptr.append(count)
        
        return values, col_indices, row_ptr
    
    def _elementwise_operation(self, other, operation):
        """Generic method for addition and subtraction."""
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise MatrixDimensionError("Matrix dimensions must match.")
        
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        
        for row, cols in self.data.items():
            for col, value in cols.items():
                result.set_element(row, col, value)
        
        for row, cols in other.data.items():
            for col, value in cols.items():
                result.set_element(row, col, operation(result.get_element(row, col), value))
        
        return result
    
    def add(self, other):
        """Add two sparse matrices."""
        return self._elementwise_operation(other, lambda x, y: x + y)
    
    def subtract(self, other):
        """Subtract two sparse matrices."""
        return self._elementwise_operation(other, lambda x, y: x - y)
    
    def multiply(self, other):
        """Multiply two sparse matrices using a dictionary-based approach."""
        if self.cols != other.rows:
            raise MatrixDimensionError("Matrix dimensions must be compatible for multiplication.")
        
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        
        for row, cols in self.data.items():
            row_data = {}
            for k, v1 in cols.items():
                if k in other.data:
                    for col, v2 in other.data[k].items():
                        row_data[col] = row_data.get(col, 0) + v1 * v2
            
            for col, value in row_data.items():
                result.set_element(row, col, value)
        
        return result
    
    def get_element(self, row, col):
        """Retrieve an element at the specified position."""
        return self.data.get(row, {}).get(col, 0)
    
    def set_element(self, row, col, value):
        """Set an element at the specified position."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise MatrixIndexError("Index out of bounds.")
        
        if value:
            self.data.setdefault(row, {})[col] = value
            self.nnz += 1
        elif row in self.data and col in self.data[row]:
            del self.data[row][col]
            if not self.data[row]:
                del self.data[row]
            self.nnz -= 1
    
    def transpose(self):
        """Transpose the matrix."""
        result = SparseMatrix(rows=self.cols, cols=self.rows)
        
        for row, cols in self.data.items():
            for col, value in cols.items():
                result.set_element(col, row, value)
        
        return result
    
    def save_to_file(self, file_path):
        """Save matrix to file in specified format."""
        try:
            with open(file_path, 'w') as f:
                f.write(f"rows={self.rows}\ncols={self.cols}\n")
                for row in sorted(self.data):
                    for col in sorted(self.data[row]):
                        f.write(f"({row}, {col}, {self.data[row][col]})\n")
        except IOError:
            raise IOError(f"Error writing to file: {file_path}")
    
    @staticmethod
    def ensure_results_directory():
        """Ensure results directory exists."""
        results_dir = "../../results"
        os.makedirs(results_dir, exist_ok=True)
