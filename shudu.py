import random
import tkinter as tk
from tkinter import messagebox


class SudokuGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("数独游戏")
		self.entries = [[None for _ in range(9)] for _ in range(9)]

		# # 生成一个随机预填充的数独网格
		self.initial_grid = self.generate_sudoku()
		self.difficulty = tk.StringVar()
		self.difficulty.set("简单")

		self.create_widgets()

	def create_widgets(self):
		# 创建9x9的数独网格
		grid_frame = tk.Frame(self.root, bg='#F0F0F0', bd=2, relief='ridge')
		grid_frame.pack(pady=20, padx=20)

		for row in range(9):
			for col in range(9):
				entry = tk.Entry(grid_frame, width=2, font=('Arial', 18), justify='center', bg='#FFFFFF')
				entry.grid(row=row, column=col, padx=1, pady=1, ipady=5, sticky='nsew')
				self.entries[row][col] = entry
				if self.initial_grid[row][col] != 0:
					entry.insert(0, str(self.initial_grid[row][col]))
					entry.config(state='readonly', disabledbackground='#E0E0E0', disabledforeground='#000000')

		# 创建一排数字按钮
		number_frame = tk.Frame(self.root, bg='#F0F0F0')
		number_frame.pack(pady=10)
		self.selected_number = tk.IntVar(value=0)
		for i in range(1, 10):
			button = tk.Radiobutton(number_frame, text=str(i), variable=self.selected_number, value=i,
									indicatoron=False,
									width=4, height=2, font=('Arial', 12), bg='#E0E0E0', selectcolor='#D0D0D0',
									relief='raised', bd=2)
			button.pack(side='left', padx=5)

		# 创建按钮框
		button_frame = tk.Frame(self.root, bg='#F0F0F0')
		button_frame.pack(pady=10)

		# 创建确定按钮
		submit_button = tk.Button(button_frame, text="确定", command=self.submit, font=('Arial', 12), width=10,
								  bg='#A0A0A0', relief='raised', bd=2)
		submit_button.pack(side='left', padx=5)

		# 创建检查按钮
		check_button = tk.Button(button_frame, text="检查", command=self.check_solution, font=('Arial', 12), width=10,
								 bg='#A0A0A0', relief='raised', bd=2)
		check_button.pack(side='left', padx=5)

		# 创建提示按钮
		hint_button = tk.Button(button_frame, text="提示", command=self.show_hint, font=('Arial', 12), width=10,
								bg='#A0A0A0', relief='raised', bd=2)
		hint_button.pack(side='left', padx=5)

		# 创建新游戏按钮
		new_game_button = tk.Button(button_frame, text="新游戏", command=self.new_game, font=('Arial', 12), width=10,
									bg='#A0A0A0', relief='raised', bd=2)
		new_game_button.pack(side='left', padx=5)

	def submit(self):
		number = self.selected_number.get()
		if number != 0:
			# 查找当前焦点的输入框，并插入数字
			widget = self.root.focus_get()
			if isinstance(widget, tk.Entry) and widget.cget('state') != 'readonly':
				widget.delete(0, tk.END)
				widget.insert(0, str(number))
		else:
			messagebox.showwarning("无效输入", "请选择一个数字")

	def check_solution(self):
		grid = []
		for row in range(9):
			current_row = []
			for col in range(9):
				value = self.entries[row][col].get()
				if value == '':
					messagebox.showwarning("不完整", "请完成所有的空格")
					return
				current_row.append(int(value))
			grid.append(current_row)

		if self.is_valid_sudoku(grid):
			messagebox.showinfo("成功", "恭喜！解正确")
		else:
			messagebox.showerror("错误", "数独解不正确，请再试一次")

	def show_hint(self):
		widget = self.root.focus_get()
		if isinstance(widget, tk.Entry) and widget.cget('state') != 'readonly':
			row = int(widget.grid_info()['row'])
			col = int(widget.grid_info()['column'])
			possible_values = self.get_possible_values(row, col)
			if possible_values:
				hint_value = possible_values[0]
				messagebox.showinfo("提示", f"可能的值：{hint_value}")
			else:
				messagebox.showinfo("提示", "无法确定唯一值")
		else:
			messagebox.showwarning("无效输入", "请选择一个空格")

	def get_possible_values(self, row, col):
		values = list(range(1, 10))
		for i in range(9):
			if self.entries[row][i].get() != '' and int(self.entries[row][i].get()) in values:
				values.remove(int(self.entries[row][i].get()))
			if self.entries[i][col].get() != '' and int(self.entries[i][col].get()) in values:
				values.remove(int(self.entries[i][col].get()))
		for i in range(3):
			for j in range(3):
				r = (row // 3) * 3 + i
				c = (col // 3) * 3 + j
				if self.entries[r][c].get() != '' and int(self.entries[r][c].get()) in values:
					values.remove(int(self.entries[r][c].get()))
		return values

	def is_valid_sudoku(self, board):
		for i in range(9):
			if not self.is_valid_block([board[i][j] for j in range(9)]):  # 检查行
				return False
			if not self.is_valid_block([board[j][i] for j in range(9)]):  # 检查列
				return False
			if not self.is_valid_block([
				board[m][n]
				for m in range(i // 3 * 3, i // 3 * 3 + 3)
				for n in range(i % 3 * 3, i % 3 * 3 + 3)
			]):  # 检查3x3子网格
				return False
		return True

	def is_valid_block(self, block):
		block = [num for num in block if num != 0]
		return len(block) == len(set(block))

	def generate_sudoku(self):
		base = 3
		side = base * base

		def pattern(r, c): return (base * (r % base) + r // base + c) % side

		def shuffle(s): return random.sample(s, len(s))

		r_base = range(base)
		rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
		cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
		nums = shuffle(range(1, base * base + 1))

		board = [[nums[pattern(r, c)] for c in cols] for r in rows]

		squares = side * side
		no_of_hints = squares * 3 // 4
		for p in random.sample(range(squares), squares - no_of_hints):
			board[p // side][p % side] = 0

		return board

	def new_game(self):
		self.root.destroy()
		root = tk.Tk()
		sudoku_gui = SudokuGUI(root)
		root.mainloop()


# if __name__ == "__main__":
root = tk.Tk()
sudoku_gui = SudokuGUI(root)
root.mainloop()
