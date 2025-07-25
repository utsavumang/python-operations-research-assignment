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

    def _subtract_row_minimums(self):
        for i in range(self.n_rows):
            min_val = np.min(self.cost_matrix[i, :])
            self.cost_matrix[i, :] -= min_val
        print("Row minimums subtracted.")

    def _subtract_column_minimums(self):
        for j in range(self.n_cols):
            min_val = np.min(self.cost_matrix[:, j])
            self.cost_matrix[:, j] -= min_val
        print("Column minimums subtracted.")

    def _find_and_cover_zeros(self):

        # Identify potential assignments, determine lines to be drawn.

        self.marked_zeros = []
        # To keep track of zeros that are part of an assignment
        assigned_mask = np.zeros_like(self.cost_matrix, dtype=bool)

        # Assign zeros in rows with only one zero
        for r in range(self.n_rows):
            zero_indices = np.where(self.cost_matrix[r, :] == 0)[0]
            # Filter out zeros in columns that are already part of an assignment
            unassigned_zeros = [c for c in zero_indices if not assigned_mask[:, c].any()]
            if len(unassigned_zeros) == 1:
                c = unassigned_zeros[0]
                self.marked_zeros.append((r, c))
                assigned_mask[r, c] = True

        # Assign zeros in columns with only one zero
        for c in range(self.n_cols):
            # Skip if column already has an assignment from the row scan
            if assigned_mask[:, c].any():
                continue
            zero_indices = np.where(self.cost_matrix[:, c] == 0)[0]
            # Filter out zeros in rows that are already part of an assignment
            unassigned_zeros = [r for r in zero_indices if not assigned_mask[r, :].any()]
            if len(unassigned_zeros) == 1:
                r = unassigned_zeros[0]
                self.marked_zeros.append((r, c))
                assigned_mask[r, c] = True
        
        print(f"Only Found {len(self.marked_zeros)} possible assignments.")

        self._cover_all_zeros()

    def _cover_all_zeros(self):
        # Line Drawing
        self.row_covered.fill(False)
        self.col_covered.fill(False)
        
        assigned_rows = {r for r, c in self.marked_zeros}
        
        # Mark rows that are not assigned
        for r in range(self.n_rows):
            if r not in assigned_rows:
                self.row_covered[r] = True
        
        marked_rows_updated = True
        marked_cols_updated = True
        
        while marked_rows_updated or marked_cols_updated:
            # Mark columns with zeros in newly marked rows
            marked_cols_updated = False
            for r in range(self.n_rows):
                if self.row_covered[r]:
                    for c in range(self.n_cols):
                        if self.cost_matrix[r, c] == 0 and not self.col_covered[c]:
                            self.col_covered[c] = True
                            marked_cols_updated = True
            
            # Mark rows that have assignments in newly marked columns
            marked_rows_updated = False
            for r, c in self.marked_zeros:
                if self.col_covered[c] and not self.row_covered[r]:
                    self.row_covered[r] = True
                    marked_rows_updated = True
        
        # Lines to be drawn through UNMARKED rows and MARKED columns.
        self.row_covered = ~self.row_covered
        
        num_lines = np.sum(self.row_covered) + np.sum(self.col_covered)
        print(f"Drew {num_lines} lines to cover all zeros.")


    