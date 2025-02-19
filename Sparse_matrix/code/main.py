from sparse_matrix import SparseMatrix

def main():
    """
    This program performs basic matrix operations (Addition, Subtraction, Multiplication)
    on sparse matrices loaded from text files.
    """
    
    operation = input("Enter operation (Add, Subtract, Multiply): ").strip().lower()
    
    matrix_1_path = '../sample_input/matrixfile1.txt'
    matrix_2_path = '../sample_input/matrixfile3.txt'
    
    matrix1 = SparseMatrix(matrix_file_path=matrix_1_path)
    matrix2 = SparseMatrix(matrix_file_path=matrix_2_path)
    
    operations = {
        "add": matrix1.add,
        "subtract": matrix1.subtract,
        "multiply": matrix1.multiply
    }
    
    if operation in operations:
        result = operations[operation](matrix2)
        print("Result:")
        result.print_readable()
    else:
        print("Invalid operation. Please enter Add, Subtract, or Multiply.")

if __name__ == "__main__":
    main()
