import os
import random
import io
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    Image = None
    PIL_AVAILABLE = False


class FractureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fracture")
        self.root.resizable(False, False)

        self.window_width = 620
        self.window_height = 260

        self.root.attributes("-topmost", True)

        self.root.bind("<Map>", self._on_map)

        bg_main = "#111217"
        bg_panel = "#181a20"
        bg_entry = "#101218"
        fg_text = "#e5e7eb"
        fg_muted = "#9ca3af"
        accent = "#6366f1"
        accent_hover = "#818cf8"
        danger = "#f97373"
        success = "#22c55e"

        self.root.configure(bg=bg_main)

        self.file_path = None

        wrapper = tk.Frame(root, bg=bg_main)
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        header = tk.Frame(wrapper, bg=bg_main)
        header.pack(fill="x", pady=(0, 8))

        lbl_title = tk.Label(
            header,
            text="Fracture",
            font=("Segoe UI", 18, "bold"),
            bg=bg_main,
            fg=fg_text,
        )
        lbl_title.pack(side="left")

        lbl_subtitle = tk.Label(
            header,
            text="(Data corruption)",
            font=("Segoe UI", 9),
            bg=bg_main,
            fg=fg_muted,
        )
        lbl_subtitle.pack(side="left", padx=(3, 0), pady=(7, 0))

        controls_frame = tk.Frame(header, bg=bg_main)
        controls_frame.pack(side="right")

        btn_close = tk.Button(
            controls_frame,
            text="\u2715",
            command=self.close_window,
            bg="#4b5563",
            fg="#e5e7eb",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            width=3,
            height=1,
            font=("Segoe UI", 9),
            cursor="hand2",
        )
        btn_close.pack(side="left")

        panel = tk.Frame(wrapper, bg=bg_panel, bd=0, highlightthickness=1, highlightbackground="#272a33")
        panel.pack(fill="both", expand=True, pady=(4, 8))

        frame_file = tk.Frame(panel, bg=bg_panel)
        frame_file.pack(fill="x", padx=12, pady=(12, 6))

        tk.Label(frame_file, text="\u0424\u0430\u0439\u043b", bg=bg_panel, fg=fg_text).pack(side="left")

        self.entry_file = tk.Entry(
            frame_file,
            width=52,
            state="readonly",
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            relief="flat",
        )
        self.entry_file.pack(side="left", padx=8, ipady=2)

        btn_browse = tk.Button(
            frame_file,
            text="\u041e\u0431\u0437\u043e\u0440",
            command=self.browse_file,
            bg="#272a33",
            fg=fg_text,
            activebackground="#333643",
            activeforeground=fg_text,
            relief="flat",
            padx=12,
            pady=4,
        )
        btn_browse.pack(side="left")

        frame_bytes = tk.Frame(panel, bg=bg_panel)
        frame_bytes.pack(fill="x", padx=12, pady=4)

        tk.Label(
            frame_bytes,
            text="\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0431\u0430\u0439\u0442 \u0434\u043b\u044f \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f",
            bg=bg_panel,
            fg=fg_text,
        ).pack(side="left")

        self.entry_bytes = tk.Entry(
            frame_bytes,
            width=10,
            bg=bg_entry,
            fg=fg_text,
            insertbackground=fg_text,
            relief="flat",
            justify="right",
        )
        self.entry_bytes.pack(side="left", padx=8, ipady=2)
        self.entry_bytes.insert(0, "100")

        lbl_hint = tk.Label(
            frame_bytes,
            text="(\u0447\u0435\u043c \u0431\u043e\u043b\u044c\u0448\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435, \u0442\u0435\u043c \u0431\u043e\u043b\u044c\u0448\u0435 \u043f\u043e\u0432\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0439)",
            bg=bg_panel,
            fg=fg_muted,
            font=("Segoe UI", 8),
        )
        lbl_hint.pack(side="left", padx=(4, 0))

        self.label_info = tk.Label(
            panel,
            text="\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d",
            bg=bg_panel,
            fg=fg_muted,
            anchor="w",
        )
        self.label_info.pack(fill="x", padx=12, pady=(8, 6))

        frame_actions = tk.Frame(panel, bg=bg_panel)
        frame_actions.pack(fill="x", padx=12, pady=(4, 12))

        frame_actions.columnconfigure(0, weight=1)
        frame_actions.columnconfigure(1, weight=0)
        frame_actions.columnconfigure(2, weight=1)

        btn_mutate = tk.Button(
            frame_actions,
            text="Mutate",
            command=self.mutate_file,
            bg=accent,
            fg="white",
            activebackground=accent_hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=28,
            pady=6,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )
        btn_mutate.grid(row=0, column=1)

        footer = tk.Frame(wrapper, bg=bg_main)
        footer.pack(fill="x")

        self.footer_label = tk.Label(
            footer,
            text="Fracture \u00b7 \u044d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u044b\u0435 \u043c\u0443\u0442\u0430\u0446\u0438\u0438, \u0434\u0435\u043b\u0430\u0439\u0442\u0435 \u0431\u044d\u043a\u0430\u043f\u044b \u043e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u043e\u0432",
            bg=bg_main,
            fg=fg_muted,
            anchor="w",
            font=("Segoe UI", 8),
        )
        self.footer_label.pack(fill="x")

        self.root.update_idletasks()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.update_idletasks()

    def _on_map(self, event):
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

    def close_window(self):
        self.root.destroy()

    def browse_file(self):
        path = filedialog.askopenfilename(title="\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b")
        if not path:
            return

        self.file_path = path
        self.entry_file.config(state="normal")
        self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, path)
        self.entry_file.config(state="readonly")

        try:
            size = os.path.getsize(path)
            self.label_info.config(
                text=f"\u0412\u044b\u0431\u0440\u0430\u043d \u0444\u0430\u0439\u043b: {os.path.basename(path)} ({size} \u0431\u0430\u0439\u0442)",
                fg="white"
            )
        except Exception as e:
            self.label_info.config(text=f"\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0440\u0430\u0437\u043c\u0435\u0440 \u0444\u0430\u0439\u043b\u0430: {e}", fg="red")

    def mutate_file(self):
        if not self.file_path:
            messagebox.showwarning("\u0412\u043d\u0438\u043c\u0430\u043d\u0438\u0435", "\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b.")
            return

        try:
            mutate_count = int(self.entry_bytes.get())
            if mutate_count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("\u041e\u0448\u0438\u0431\u043a\u0430", "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e\u0435 \u043f\u043e\u043b\u043e\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e \u0431\u0430\u0439\u0442 \u0434\u043b\u044f \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f.")
            return

        try:
            with open(self.file_path, "rb") as f:
                data = bytearray(f.read())
        except Exception as e:
            messagebox.showerror("\u041e\u0448\u0438\u0431\u043a\u0430", f"\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u0442\u044c \u0444\u0430\u0439\u043b:\n{e}")
            return

        file_size = len(data)
        if file_size == 0:
            messagebox.showerror("\u041e\u0448\u0438\u0431\u043a\u0430", "\u0424\u0430\u0439\u043b \u043f\u0443\u0441\u0442\u043e\u0439, \u0438\u0437\u043c\u0435\u043d\u044f\u0442\u044c \u043d\u0435\u0447\u0435\u0433\u043e.")
            return

        mutate_count = min(mutate_count, file_size)

        _, file_name = os.path.split(self.file_path)
        name, ext = os.path.splitext(file_name)
        ext = ext.lower()

        protected_indices = set()

        if ext in {".jpg", ".jpeg"}:
            for i in range(file_size):
                if i < file_size - 1:
                    if data[i] == 0xFF:
                        protected_indices.add(i)
                        protected_indices.add(i + 1)
                if i < 20:
                    protected_indices.add(i)
                if i >= file_size - 2:
                    protected_indices.add(i)
        elif ext in {".png"}:
            for i in range(min(8, file_size)):
                protected_indices.add(i)
            for i in range(max(0, file_size - 12), file_size):
                protected_indices.add(i)
        elif ext in {".gif"}:
            for i in range(min(6, file_size)):
                protected_indices.add(i)
            if file_size > 0:
                protected_indices.add(file_size - 1)
        elif ext in {".bmp"}:
            for i in range(min(54, file_size)):
                protected_indices.add(i)
        else:
            for i in range(min(1024, file_size)):
                protected_indices.add(i)

        mutable_indices = [i for i in range(file_size) if i not in protected_indices]
        mutable_range_size = len(mutable_indices)

        if mutable_range_size <= 0:
            messagebox.showerror("\u041e\u0448\u0438\u0431\u043a\u0430", "\u0421\u043b\u0438\u0448\u043a\u043e\u043c \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439 \u0444\u0430\u0439\u043b \u0438\u043b\u0438 \u0432\u0441\u0435 \u0431\u0430\u0439\u0442\u044b \u0437\u0430\u0449\u0438\u0449\u0435\u043d\u044b \u0434\u043b\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0439 \u043c\u0443\u0442\u0430\u0446\u0438\u0438.")
            return

        mutate_count = min(mutate_count, mutable_range_size)

        original_data = bytearray(data)

        def apply_mutation(buf, count=None):
            if count is None:
                count = mutate_count
            selected_indices = random.sample(mutable_indices, min(count, len(mutable_indices)))
            for i in selected_indices:
                original_byte = buf[i]
                if ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp"}:
                    change = random.randint(-50, 50)
                    new_byte = (original_byte + change) % 256
                    if ext in {".jpg", ".jpeg"} and new_byte == 0xFF:
                        new_byte = 0xFE
                else:
                    new_byte = random.randint(0, 255)
                    if new_byte == original_byte:
                        new_byte = (new_byte + 1) % 256
                buf[i] = new_byte

        def is_valid(mutated_bytes):
            image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".tif"}
            if ext in image_exts and PIL_AVAILABLE:
                try:
                    img_data = io.BytesIO(mutated_bytes)
                    with Image.open(img_data) as img:
                        img.verify()
                    img_data.seek(0)
                    with Image.open(img_data) as img:
                        img.load()
                        if img.size[0] <= 0 or img.size[1] <= 0:
                            return False
                    return True
                except Exception:
                    return False

            return True

        max_attempts = 50
        success = False
        final_mutate_count = mutate_count

        self.label_info.config(text="Выполняется мутация...", fg="blue")
        self.root.update()

        for attempt in range(max_attempts):
            data = bytearray(original_data)
            apply_mutation(data, mutate_count)
            if is_valid(bytes(data)):
                success = True
                final_mutate_count = mutate_count
                break

        if not success:
            if mutate_count > 10:
                self.label_info.config(text="Пробуем более безопасную мутацию...", fg="blue")
                self.root.update()
                conservative_count = max(1, mutate_count // 5)
                conservative_count = min(conservative_count, mutable_range_size)

                for attempt in range(max_attempts):
                    data = bytearray(original_data)
                    apply_mutation(data, conservative_count)
                    if is_valid(bytes(data)):
                        success = True
                        final_mutate_count = conservative_count
                        break

            if not success:
                messagebox.showerror(
                    "\u041e\u0448\u0438\u0431\u043a\u0430",
                    f"\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u0443\u044e \u043c\u0443\u0442\u0430\u0446\u0438\u044e \u0444\u0430\u0439\u043b\u0430 \u043f\u043e\u0441\u043b\u0435 {max_attempts * 2} \u043f\u043e\u043f\u044b\u0442\u043e\u043a.\n"
                    f"\u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0443\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0431\u0430\u0439\u0442 (\u0442\u0435\u043a\u0443\u0449\u0435\u0435: {mutate_count}) \u0438\u043b\u0438 \u0432\u044b\u0431\u0440\u0430\u0442\u044c \u0434\u0440\u0443\u0433\u043e\u0439 \u0444\u0430\u0439\u043b."
                )
                self.label_info.config(text="\u041c\u0443\u0442\u0430\u0446\u0438\u044f \u043d\u0435 \u0443\u0434\u0430\u043b\u0430\u0441\u044c", fg="red")
                return

        dir_name, file_name = os.path.split(self.file_path)
        new_name = f"{name}_mutated{ext}"
        new_path = os.path.join(dir_name, new_name)

        try:
            with open(new_path, "wb") as f:
                f.write(data)
        except Exception as e:
            messagebox.showerror("\u041e\u0448\u0438\u0431\u043a\u0430", f"\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0437\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0451\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b:\n{e}")
            return

        messagebox.showinfo(
            "\u0413\u043e\u0442\u043e\u0432\u043e",
            f"\u0424\u0430\u0439\u043b \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043c\u0443\u0442\u0438\u0440\u043e\u0432\u0430\u043d!\n"
            f"\u0418\u0441\u0445\u043e\u0434\u043d\u044b\u0439: {file_name}\n"
            f"\u041d\u043e\u0432\u044b\u0439: {new_name}\n"
            f"\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u043e \u0431\u0430\u0439\u0442: {final_mutate_count}"
        )

        self.label_info.config(
            text=f"\u0421\u043e\u0437\u0434\u0430\u043d \u0444\u0430\u0439\u043b: {new_name} (\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u043e {final_mutate_count} \u0431\u0430\u0439\u0442)",
            fg="green"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

    app = FractureApp(root)
    root.mainloop()
