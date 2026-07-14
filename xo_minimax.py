import tkinter as tk
from tkinter import messagebox

class XOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Game XO Mở Rộng")
        self.root.geometry("600x680")
        self.root.configure(bg="#2c3e50")
        
        # Cấu hình mặc định ban đầu
        self.size = 6
        self.win_condition = 4
        self.current_player = "X"
        self.board = []
        self.buttons = []
        self.game_over = False

        # Giao diện menu chọn kích thước bàn cờ
        self.create_menu()

    def create_menu(self):
        """Tạo thanh chọn chế độ chơi ở phía trên ứng dụng"""
        menu_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        menu_frame.pack(fill=tk.X, side=tk.TOP)
        title_label = tk.Label(menu_frame, text="CHẾ ĐỘ CHƠI:", font=("Arial", 12, "bold"), fg="white", bg="#34495e")
        title_label.pack(side=tk.LEFT, padx=10)
        # Nút chọn 6x6
        btn_6x6 = tk.Button(menu_frame, text="Bàn cờ 6x6 (Thắng 4)", font=("Arial", 10, "bold"),
                            bg="#e67e22", fg="white", command=lambda: self.start_new_game(6, 4))
        btn_6x6.pack(side=tk.LEFT, padx=5)
        # Nút chọn 8x8
        btn_8x8 = tk.Button(menu_frame, text="Bàn cờ 8x8 (Thắng 5)", font=("Arial", 10, "bold"),
                            bg="#9b59b6", fg="white", command=lambda: self.start_new_game(8, 5))
        btn_8x8.pack(side=tk.LEFT, padx=5)
        # Nút chơi lại
        btn_reset = tk.Button(menu_frame, text="Chơi lại", font=("Arial", 10, "bold"),
                             bg="#2ecc71", fg="white", command=self.reset_game)
        btn_reset.pack(side=tk.RIGHT, padx=10)
        # Nhãn hiển thị lượt đi hiện tại
        self.status_label = tk.Label(self.root, text="Lượt đi: Người chơi X", font=("Arial", 14, "bold"), 
                                     fg="#f1c40f", bg="#2c3e50", pady=10)
        self.status_label.pack(side=tk.TOP)
        # Khung chứa bàn cờ chính
        self.board_frame = tk.Frame(self.root, bg="#2c3e50")
        self.board_frame.pack(expand=True)
        # Khởi tạo game 6x6 mặc định khi mở app
        self.start_new_game(6, 4)

    def start_new_game(self, size, win_condition):
        """Khởi tạo một ván đấu mới với kích thước được chọn"""
        self.size = size
        self.win_condition = win_condition
        self.reset_game()

    def reset_game(self):
        """Đặt lại trạng thái bàn cờ"""
        self.current_player = "X"
        self.game_over = False
        self.status_label.config(text="Lượt đi: Người chơi X", fg="#e74c3c")
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        
        # Xóa các nút cũ trên giao diện nếu có
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]

        # Tạo ma trận nút nhấn (Grid) tương ứng với kích thước bàn cờ
        for r in range(self.size):
            for c in range(self.size):
                # Định kích thước nút linh hoạt tùy theo bàn cờ to hay nhỏ
                btn_width = 4 if self.size == 6 else 3
                btn_height = 2 if self.size == 6 else 1
                font_size = 14 if self.size == 6 else 11

                btn = tk.Button(self.board_frame, text="", font=("Arial", font_size, "bold"), 
                                width=btn_width, height=btn_height, bg="#ecf0f1", activebackground="#bdc3c7",
                                command=lambda row=r, col=c: self.on_click(row, col))
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[r][c] = btn

    def on_click(self, r, c):
        """Xử lý sự kiện khi người chơi bấm vào ô cờ"""
        if self.board[r][c] == ' ' and not self.game_over:
            # Ghi nhận nước đi vào mảng dữ liệu
            self.board[r][c] = self.current_player
            
            # Hiển thị ký tự lên giao diện đồ họa
            color = "#e74c3c" if self.current_player == "X" else "#3498db"
            self.buttons[r][c].config(text=self.current_player, state=tk.DISABLED, disabledforeground=color, bg="#ffffff")

            # Kiểm tra xem nước đi này có giúp người chơi chiến thắng không
            if self.check_winner(r, c):
                self.game_over = True
                self.status_label.config(text=f"Người chơi {self.current_player} THẮNG CUỘC!", fg="#2ecc71")
                messagebox.showinfo("Kết quả", f"Chúc mừng! Người chơi {self.current_player} đã chiến thắng!")
                return

            # Kiểm tra hòa (hết ô trống)
            if self.is_board_full():
                self.game_over = True
                self.status_label.config(text="KẾT QUẢ: HÒA NHAU!", fg="#95a5a6")
                messagebox.showinfo("Kết quả", "Trận đấu hòa!")
                return

            # Đổi lượt chơi sang người tiếp theo
            self.current_player = "O" if self.current_player == "X" else "X"
            next_color = "#e74c3c" if self.current_player == "X" else "#3498db"
            self.status_label.config(text=f"Lượt đi: Người chơi {self.current_player}", fg=next_color)

    def check_winner(self, r, c):
        """Thuật toán kiểm tra thắng cuộc quanh vị trí ô cờ vừa đánh (Tối ưu hóa hiệu năng)"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Ngang, Dọc, Chéo xuôi \, Chéo ngược /
        player_char = self.board[r][c]

        for dr, dc in directions:
            count = 1  # Đếm chính ô vừa đánh

            # Đếm tiến theo một hướng
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_char:
                count += 1
                nr += dr
                nc += dc

            # Đếm lùi theo hướng ngược lại
            nr, nc = r - dr, c - dc
            while 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player_char:
                count += 1
                nr -= dr
                nc -= dc

            # Nếu chuỗi đạt hoặc vượt quá điều kiện thắng thì trả về kết quả thắng
            if count >= self.win_condition:
                return True
        return False

    def is_board_full(self):
        """Kiểm tra xem bàn cờ đã kín chỗ chưa"""
        for row in self.board:
            if ' ' in row:
                return False
        return True

# Khởi động ứng dụng 
if __name__ == "__main__":
    root = tk.Tk()
    app = XOApp(root)
    root.mainloop()
