import customtkinter as ctk
import numpy as np
import random
from solver import AssignmentSolver

class AssignmentApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Assignment Solver")
        self.geometry("950x700") 
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.active_entry = None

        # Main window layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        self.create_matrix_grid()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Assignment Problem Solver", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(expand=True, pady=10)

        self.theme_switch = ctk.CTkSwitch(header_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.place(relx=0.98, rely=0.5, anchor="e")
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Light Mode")

    def _create_main_content(self):
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        config_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) # Adjusted for new layout
        config_frame.grid_columnconfigure(4, weight=0) # Button column

        # C0
        rows_label = ctk.CTkLabel(config_frame, text="Rows:")
        rows_label.grid(row=0, column=0, padx=(10,5), pady=5, sticky="e")
        self.rows_entry = ctk.CTkEntry(config_frame, width=60)
        self.rows_entry.grid(row=0, column=1, pady=5, sticky="w")
        self.rows_entry.insert(0, "4")

        cols_label = ctk.CTkLabel(config_frame, text="Columns:")
        cols_label.grid(row=1, column=0, padx=(10,5), pady=5, sticky="e")
        self.cols_entry = ctk.CTkEntry(config_frame, width=60)
        self.cols_entry.grid(row=1, column=1, pady=5, sticky="w")
        self.cols_entry.insert(0, "4")

        # C2
        row_name_label = ctk.CTkLabel(config_frame, text="Row Name:")
        row_name_label.grid(row=0, column=2, padx=(10,5), pady=5, sticky="e")
        self.row_name_entry = ctk.CTkEntry(config_frame)
        self.row_name_entry.grid(row=0, column=3, pady=5, sticky="w")
        self.row_name_entry.insert(0, "Agent")

        col_name_label = ctk.CTkLabel(config_frame, text="Column Name:")
        col_name_label.grid(row=1, column=2, padx=(10,5), pady=5, sticky="e")
        self.col_name_entry = ctk.CTkEntry(config_frame)
        self.col_name_entry.grid(row=1, column=3, pady=5, sticky="w")
        self.col_name_entry.insert(0, "Task")
        
        problem_type_label = ctk.CTkLabel(config_frame, text="Problem Type:")
        problem_type_label.grid(row=2, column=0, padx=(10,5), pady=5, sticky="e")
        self.problem_type_var = ctk.StringVar(value="Minimize Cost")
        self.problem_type_selector = ctk.CTkSegmentedButton(config_frame, values=["Minimize Cost", "Maximize Profit"], variable=self.problem_type_var)
        self.problem_type_selector.grid(row=2, column=1, columnspan=3, pady=5, sticky="w")


        # C4
        button_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        button_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=5)

        self.create_grid_button = ctk.CTkButton(button_frame, text="Create Matrix", command=self.create_matrix_grid)
        self.create_grid_button.pack(pady=5, fill="x")
        
        self.reset_button = ctk.CTkButton(button_frame, text="Reset Matrix", command=self.reset_matrix_grid)
        self.reset_button.pack(pady=5, fill="x")

        self.infinity_button = ctk.CTkButton(button_frame, text="Set Constraint (∞)", command=self.set_infinity_cost, fg_color="transparent", border_width=2)
        self.infinity_button.pack(pady=5, fill="x")

        # Main Layout Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left Pane
        left_pane = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_pane.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")
        left_pane.grid_rowconfigure(0, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)
        
        self.matrix_frame = ctk.CTkScrollableFrame(left_pane, label_text="Cost / Profit Matrix")
        self.matrix_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.matrix_entries = []
        
        self.solve_button = ctk.CTkButton(left_pane, text="Solve Assignment Problem", command=self.solve_matrix)
        self.solve_button.grid(row=1, column=0, pady=10, padx=0)
        
        # Right Pane
        self.result_textbox = ctk.CTkTextbox(main_frame, wrap="word", font=("Arial", 12))
        self.result_textbox.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="nsew")
        self.result_textbox.insert("0.0", "Results will be displayed here.")
        self.result_textbox.configure(state="disabled")

    def _create_footer(self):
        footer_frame = ctk.CTkFrame(self, corner_radius=0)
        footer_frame.grid(row=3, column=0, sticky="ew")
        
        footer_text = ("05 HSMC 03 | Operations Research | Dr. Ravinder Pal Singh | "
                       "Dept. of Electronics and Computer Engineering, NIAMT")
        footer_label = ctk.CTkLabel(footer_frame, text=footer_text, font=ctk.CTkFont(size=12))
        footer_label.pack(pady=5)

    def _clear_highlights(self):
        for row_entries in self.matrix_entries:
            for entry in row_entries:
                entry.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])

    def _set_active_entry(self, event):
        self.active_entry = event.widget

    def create_matrix_grid(self):
        self.create_grid_button.configure(text="Creating...", state="disabled")
        self.update_idletasks()
        try:
            self._clear_highlights()
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            self.matrix_entries = []
            rows, cols = int(self.rows_entry.get()), int(self.cols_entry.get())
            for r in range(rows):
                row_entries = []
                for c in range(cols):
                    entry = ctk.CTkEntry(self.matrix_frame, width=60, justify="center")
                    entry.bind("<FocusIn>", self._set_active_entry)
                    entry.insert(0, str(random.randint(1, 100)))
                    entry.grid(row=r, column=c, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
        except ValueError:
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "Error: Please enter valid integers for rows and columns.")
            self.result_textbox.configure(state="disabled")
        finally:
            self.create_grid_button.configure(text="Create Matrix", state="normal")
    
    def reset_matrix_grid(self):
        self._clear_highlights()
        for row_entries in self.matrix_entries:
            for entry in row_entries:
                entry.delete(0, "end")
                entry.insert(0, "0")

    def set_infinity_cost(self):
        if self.active_entry:
            self.active_entry.delete(0, "end")
            self.active_entry.insert(0, "inf")

    def solve_matrix(self):
        self.solve_button.configure(text="Solving...", state="disabled")
        self.update_idletasks()
        try:
            self._clear_highlights()
            
            def convert_value(val_str):
                cleaned_val = val_str.strip().lower()
                if cleaned_val in ('inf', 'infinity'):
                    return float('inf')
                return float(cleaned_val)

            profit_matrix_np = np.array([[convert_value(self.matrix_entries[r][c].get()) 
                                        for c in range(len(self.matrix_entries[r]))] 
                                        for r in range(len(self.matrix_entries))])
            
            problem_type = self.problem_type_var.get()
            

            if problem_type == "Maximize Profit":
                finite_max = profit_matrix_np[np.isfinite(profit_matrix_np)].max()
                cost_matrix = finite_max - profit_matrix_np
                cost_matrix[np.isneginf(cost_matrix)] = float('inf') 
            else:
                cost_matrix = profit_matrix_np.tolist()


            row_name = self.row_name_entry.get() or "Agent"
            col_name = self.col_name_entry.get() or "Task"
            
            solver = AssignmentSolver(cost_matrix)
            assignments, _ = solver.solve()
            
            original_rows, original_cols = profit_matrix_np.shape
            
            output_text = ""
            total_value = 0
            value_label = "Profit" if problem_type == "Maximize Profit" else "Cost"
            
            for row, col in assignments:
                if row < original_rows and col < original_cols:
                    value = profit_matrix_np[row, col]
                    if np.isfinite(value):
                        total_value += value
                    output_text += f"  - {row_name} {row + 1} assigned to {col_name} {col + 1} ({value_label}: {value})\n"
                    self.matrix_entries[row][col].configure(fg_color=("#A0E8A2", "#1E5631"))
            
            total_label = "Total Maximum Profit" if problem_type == "Maximize Profit" else "Total Minimum Cost"
            output_text += f"\n{total_label}: {total_value}"
            
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", output_text)
            self.result_textbox.configure(state="disabled")

        except (ValueError, IndexError):
            self.result_textbox.configure(state="normal")
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", "Error: Please ensure all matrix cells contain valid numbers.")
            self.result_textbox.configure(state="disabled")
        finally:
            self.solve_button.configure(text="Solve Assignment Problem", state="normal")

if __name__ == "__main__":
    app = AssignmentApp()
    app.mainloop()
