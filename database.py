import tkinter as tk
from tkinter import ttk, messagebox

class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, order=3):
        self.root = BTreeNode(True)
        self.order = order
        self.max_keys = order - 1

    def insert(self, key, data):
        root = self.root
        if len(root.keys) == self.max_keys:
            temp = BTreeNode(False)
            self.root = temp
            temp.children.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, key, data)
        else:
            self.insert_non_full(root, key, data)

    def insert_non_full(self, node, key, data):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = (key, data)
        else:
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.max_keys:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], key, data)

    def split_child(self, parent, i):
        child = parent.children[i]
        new_node = BTreeNode(child.leaf)
        mid = len(child.keys) // 2
        split_key_data = child.keys[mid]
        new_node.keys = child.keys[mid+1:]
        child.keys = child.keys[:mid]
        if not child.leaf:
            new_node.children = child.children[mid+1:]
            child.children = child.children[:mid+1]
        parent.children.insert(i + 1, new_node)
        parent.keys.insert(i, split_key_data)

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i][1]
        elif node.leaf:
            return None
        else:
            return self.search(key, node.children[i])


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Quản Lý Sinh Viên - B-Tree Indexing")
        self.root.geometry("1150x750")
        
        # --- BẢNG MÀU CHUYÊN NGHIỆP (Modern Dark Theme) ---
        self.BG_MAIN = "#1E1E2E"       # Nền chính (Xám xanh siêu tối, dịu mắt)
        self.BG_PANEL = "#27293D"      # Nền các khung nhập liệu (Sáng hơn nền chính 1 chút)
        self.FG_TEXT = "#E2E2E9"       # Màu chữ trắng ngà
        
        self.COLOR_PRIMARY = "#3B82F6" # Xanh dương hiện đại (Nút Tìm, Làm mới)
        self.COLOR_SUCCESS = "#10B981" # Xanh lá (Nút Thêm)
        self.COLOR_DANGER = "#EF4444"  # Đỏ nhạt (Nút Xóa)
        
        self.NODE_BG = "#2D3250"       # Nền của cục Node B-Tree
        self.NODE_BORDER = "#7091F5"   # Viền của Node B-Tree
        
        self.FONT_UI = ("Segoe UI", 10)
        self.FONT_BOLD = ("Segoe UI", 10, "bold")

        self.root.configure(bg=self.BG_MAIN)
        
        # --- CẤU HÌNH STYLE CHO BẢNG (Treeview) ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                        background=self.BG_PANEL, 
                        foreground=self.FG_TEXT, 
                        fieldbackground=self.BG_PANEL, 
                        rowheight=30,
                        font=self.FONT_UI,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', self.COLOR_PRIMARY)])
        
        style.configure("Treeview.Heading", 
                        background="#32324E", 
                        foreground=self.FG_TEXT, 
                        relief="flat", 
                        font=self.FONT_BOLD)
        style.map('Treeview.Heading', background=[('active', "#404060")])

        self.students = {}
        self.btree_id = BTree(order=3)
        self.btree_name = BTree(order=3)
        
        self.setup_ui()
        self.load_sample_data()

    def create_btn(self, parent, text, color, command, width=12):
        """Hàm tạo nút bấm phẳng với màu sắc tùy chỉnh"""
        btn = tk.Button(parent, text=text, command=command, width=width,
                        bg=color, fg="white", activebackground=self.FG_TEXT, activeforeground=self.BG_MAIN,
                        relief=tk.FLAT, font=self.FONT_BOLD, cursor="hand2", pady=3)
        return btn

    def setup_ui(self):
        # --- Khung nhập liệu (Top Frame) ---
        input_frame = tk.Frame(self.root, bg=self.BG_PANEL, pady=15, padx=20)
        input_frame.pack(fill=tk.X, padx=15, pady=(15, 5))

        tk.Label(input_frame, text="Mã SV:", bg=self.BG_PANEL, fg=self.FG_TEXT, font=self.FONT_BOLD).grid(row=0, column=0, padx=5)
        self.entry_id = tk.Entry(input_frame, width=15, font=self.FONT_UI, relief=tk.FLAT, bg="#1E1E2E", fg="white", insertbackground="white")
        self.entry_id.grid(row=0, column=1, padx=5, ipady=4)

        tk.Label(input_frame, text="Họ và tên:", bg=self.BG_PANEL, fg=self.FG_TEXT, font=self.FONT_BOLD).grid(row=0, column=2, padx=10)
        self.entry_name = tk.Entry(input_frame, width=25, font=self.FONT_UI, relief=tk.FLAT, bg="#1E1E2E", fg="white", insertbackground="white")
        self.entry_name.grid(row=0, column=3, padx=5, ipady=4)

        tk.Label(input_frame, text="Giới tính:", bg=self.BG_PANEL, fg=self.FG_TEXT, font=self.FONT_BOLD).grid(row=0, column=4, padx=10)
        self.combo_gender = ttk.Combobox(input_frame, values=["Nam", "Nữ"], width=8, state="readonly", font=self.FONT_UI)
        self.combo_gender.current(0)
        self.combo_gender.grid(row=0, column=5, padx=5, ipady=3)

        # Các nút chức năng
        frame_btns1 = tk.Frame(input_frame, bg=self.BG_PANEL)
        frame_btns1.grid(row=0, column=6, padx=(20, 0))
        self.create_btn(frame_btns1, "Thêm Mới", self.COLOR_SUCCESS, self.add_student, width=10).pack(side=tk.LEFT, padx=5)
        self.create_btn(frame_btns1, "Xóa SV", self.COLOR_DANGER, self.delete_student, width=10).pack(side=tk.LEFT, padx=5)

        # --- Khung Tìm kiếm (Middle Frame) ---
        search_frame = tk.Frame(self.root, bg=self.BG_PANEL, pady=15, padx=20)
        search_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(search_frame, text="Tìm theo Mã:", bg=self.BG_PANEL, fg=self.FG_TEXT, font=self.FONT_BOLD).grid(row=0, column=0, padx=5)
        self.search_id = tk.Entry(search_frame, width=15, font=self.FONT_UI, relief=tk.FLAT, bg="#1E1E2E", fg="white", insertbackground="white")
        self.search_id.grid(row=0, column=1, padx=5, ipady=4)
        self.create_btn(search_frame, "Tìm Mã", self.COLOR_PRIMARY, self.search_by_id, width=8).grid(row=0, column=2, padx=5)

        tk.Label(search_frame, text="Tìm theo Tên:", bg=self.BG_PANEL, fg=self.FG_TEXT, font=self.FONT_BOLD).grid(row=0, column=3, padx=(20, 5))
        self.search_name = tk.Entry(search_frame, width=25, font=self.FONT_UI, relief=tk.FLAT, bg="#1E1E2E", fg="white", insertbackground="white")
        self.search_name.grid(row=0, column=4, padx=5, ipady=4)
        self.create_btn(search_frame, "Tìm Tên", self.COLOR_PRIMARY, self.search_by_name, width=8).grid(row=0, column=5, padx=5)
        
        self.create_btn(search_frame, "Hiện tất cả", "#6B7280", self.refresh_table, width=12).grid(row=0, column=6, padx=(30, 0))

        # --- Khung Dữ liệu (Bottom) ---
        # LƯU Ý: Đã bỏ thuộc tính sashbg gây lỗi trên Windows
        main_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.BG_MAIN, bd=0, sashwidth=6)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        # Bảng hiển thị (Trái)
        table_container = tk.Frame(main_frame, bg=self.BG_MAIN)
        tk.Label(table_container, text=" DANH SÁCH SINH VIÊN", bg=self.BG_MAIN, fg=self.COLOR_PRIMARY, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        
        self.tree = ttk.Treeview(table_container, columns=("ID", "Name", "Gender"), show="headings", height=15)
        self.tree.heading("ID", text="Mã SV")
        self.tree.heading("Name", text="Họ và tên")
        self.tree.heading("Gender", text="Giới tính")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=180)
        self.tree.column("Gender", width=80, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)
        main_frame.add(table_container, minsize=380)

        # Khung vẽ B-Tree (Phải)
        canvas_frame = tk.Frame(main_frame, bg=self.BG_MAIN)
        main_frame.add(canvas_frame)

        tk.Label(canvas_frame, text=" CÂY B-TREE: CHỈ MỤC MÃ SV", bg=self.BG_MAIN, fg=self.COLOR_SUCCESS, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        self.canvas_id = tk.Canvas(canvas_frame, bg=self.BG_PANEL, height=250, highlightthickness=0)
        self.canvas_id.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        tk.Label(canvas_frame, text=" CÂY B-TREE: CHỈ MỤC HỌ TÊN", bg=self.BG_MAIN, fg=self.COLOR_SUCCESS, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        self.canvas_name = tk.Canvas(canvas_frame, bg=self.BG_PANEL, height=250, highlightthickness=0)
        self.canvas_name.pack(fill=tk.BOTH, expand=True)

    def load_sample_data(self):
        samples = [
            ("SV001", "Trần Thị Bình", "Nữ"),
            ("SV002", "Nguyễn Văn An", "Nam"),
            ("SV003", "Lê Minh Châu", "Nữ"),
            ("SV004", "Phạm Thu Hà", "Nữ"),
            ("SV005", "Vũ Duy Mạnh", "Nam")
        ]
        for sv_id, name, gender in samples:
            self.insert_data(sv_id, name, gender)

    def insert_data(self, sv_id, name, gender):
        if sv_id in self.students:
            messagebox.showwarning("Cảnh báo", "Mã SV đã tồn tại!")
            return False
            
        student_data = {"id": sv_id, "name": name, "gender": gender}
        self.students[sv_id] = student_data
        
        self.btree_id.insert(sv_id, student_data)
        self.btree_name.insert(name, student_data)
        
        self.refresh_table()
        self.draw_trees()
        return True

    def add_student(self):
        sv_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        gender = self.combo_gender.get()
        
        if not sv_id or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ Mã SV và Họ tên.")
            return
            
        if self.insert_data(sv_id, name, gender):
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng click chọn 1 sinh viên trong bảng để xóa.")
            return
            
        item = self.tree.item(selected[0])
        sv_id = item['values'][0]
        
        if sv_id in self.students:
            del self.students[sv_id]
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã xóa sinh viên: {sv_id}. \n(Cần code thêm hàm Xóa trên B-Tree để cập nhật giao diện cây)")

    def search_by_id(self):
        sv_id = self.search_id.get().strip()
        result = self.btree_id.search(sv_id)
        self.display_search_result(result)

    def search_by_name(self):
        name = self.search_name.get().strip()
        result = self.btree_name.search(name)
        self.display_search_result(result)

    def display_search_result(self, result):
        self.tree.delete(*self.tree.get_children())
        if result:
            self.tree.insert("", tk.END, values=(result["id"], result["name"], result["gender"]))
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy sinh viên khớp với thông tin!")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for sv_id, data in self.students.items():
            self.tree.insert("", tk.END, values=(data["id"], data["name"], data["gender"]))

    # --- Vẽ B-Tree ---
    def draw_trees(self):
        self.canvas_id.delete("all")
        self.canvas_name.delete("all")
        
        if self.students:
            self.draw_node(self.canvas_id, self.btree_id.root, 360, 40, 220)
            self.draw_node(self.canvas_name, self.btree_name.root, 360, 40, 220)

    def draw_node(self, canvas, node, x, y, dx):
        if not node: return
        
        text = "  |  ".join(str(k[0]) for k in node.keys)
        rect_width = max(90, len(text) * 9)
        
        # Vẽ Node hiện đại hơn
        canvas.create_rectangle(x - rect_width/2, y - 18, x + rect_width/2, y + 18, 
                                fill=self.NODE_BG, outline=self.NODE_BORDER, width=2)
        canvas.create_text(x, y, text=text, fill=self.FG_TEXT, font=("Segoe UI", 10, "bold"))
        
        if not node.leaf:
            num_children = len(node.children)
            start_x = x - dx * (num_children - 1) / 2
            for i, child in enumerate(node.children):
                child_x = start_x + i * dx
                child_y = y + 70
                # Line nối mượt mà hơn
                canvas.create_line(x, y + 18, child_x, child_y - 18, fill="#52527A", width=2)
                self.draw_node(canvas, child, child_x, child_y, dx / 1.6)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()