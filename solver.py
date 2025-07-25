import numpy as np

class AssignmentSolver:


    def __init__(self, cost_matrix):
        self.original_matrix = np.array(cost_matrix, dtype=float)
        self.cost_matrix = np.array(cost_matrix, dtype=float)
        self.n_rows, self.n_cols = self.cost_matrix.shape
        self.assignments = {}  # Store final assignments as {row: col}
        self.marked_zeros = [] # Stores (row, col) of assigned zeros
        self.row_covered = np.zeros(self.n_rows, dtype=bool)
        self.col_covered = np.zeros(self.n_cols, dtype=bool)

    def solve(self):
        
        self._add_dummy_rc()
        
        self._subtract_row_minimums()
        
        self._subtract_column_minimums()

        while not self._is_optimal():
            self._find_and_cover_zeros()
            self._adjust_matrix()
        self._find_final_assignments()


        total_cost = self._calculate_total_cost()
        

        final_assignments = list(self.assignments.items())

        print("Completed.")
        return final_assignments, total_cost

    def _add_dummy_rc(self):
        n, m = self.cost_matrix.shape
        if n == m:
            return
            
        size = max(n, m)
        padded_matrix = np.zeros((size, size), dtype=float)
        padded_matrix[:n, :m] = self.cost_matrix
        self.cost_matrix = padded_matrix
        self.n_rows, self.n_cols = self.cost_matrix.shape
        
        self.row_covered = np.zeros(self.n_rows, dtype=bool)
        self.col_covered = np.zeros(self.n_cols, dtype=bool)
        
        print(f"Dummy Rows/Columns added, matrix size now {size}x{size}.")

    

