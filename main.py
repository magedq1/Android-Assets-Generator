import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import logic
import os

class AndroidAssetGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Android Assets Generator")
        self.root.geometry("600x500")
        
        # Variables
        self.input_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.input_mode = tk.StringVar(value="file") # file or dir

        # UI Setup
        self.create_widgets()
        
    def create_widgets(self):
        # --- Mode Selection ---
        mode_frame = tk.LabelFrame(self.root, text="Input Mode", padx=10, pady=5)
        mode_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Radiobutton(mode_frame, text="Single Image File", variable=self.input_mode, value="file", command=self.clear_input).pack(side="left", padx=10)
        tk.Radiobutton(mode_frame, text="Directory (Batch)", variable=self.input_mode, value="dir", command=self.clear_input).pack(side="left", padx=10)

        # --- Input Section ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(input_frame, text="Input Path:").pack(anchor="w")
        
        input_inner_frame = tk.Frame(input_frame)
        input_inner_frame.pack(fill="x")
        
        self.input_entry = tk.Entry(input_inner_frame, textvariable=self.input_path_var, width=50)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(input_inner_frame, text="Browse...", command=self.browse_input).pack(side="right")

        # --- Output Section ---
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(output_frame, text="Output Directory (Optional):").pack(anchor="w")
        
        output_inner_frame = tk.Frame(output_frame)
        output_inner_frame.pack(fill="x")
        
        self.output_entry = tk.Entry(output_inner_frame, textvariable=self.output_path_var, width=50)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(output_inner_frame, text="Browse...", command=self.browse_output).pack(side="right")

        # --- Generate Button ---
        self.generate_btn = tk.Button(self.root, text="Generate Assets", command=self.start_generation_thread, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.generate_btn.pack(pady=10)

        # --- Log Area ---
        log_frame = tk.LabelFrame(self.root, text="Logs", padx=5, pady=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10)
        self.log_text.pack(fill="both", expand=True)

    def clear_input(self):
        self.input_path_var.set("")

    def browse_input(self):
        mode = self.input_mode.get()
        if mode == "file":
            path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp"), ("All Files", "*.*")])
        else:
            path = filedialog.askdirectory()
            
        if path:
            self.input_path_var.set(path)
            # Auto-set default output if empty
            if not self.output_path_var.get():
                if mode == "file":
                    parent = os.path.dirname(path)
                else:
                    parent = path
                self.output_path_var.set(os.path.join(parent, "android"))

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_var.set(path)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_generation_thread(self):
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or directory.")
            return

        self.generate_btn.config(state='disabled')
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Run in thread
        thread = threading.Thread(target=self.run_generation, args=(input_path, output_path))
        thread.start()

    def run_generation(self, input_path, output_path):
        def thread_safe_log(msg):
            self.root.after(0, self.log, msg)

        try:
            logic.process_input(input_path, output_path, thread_safe_log)
        except Exception as e:
            thread_safe_log(f"Critical Error: {e}")
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state='normal'))

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidAssetGeneratorApp(root)
    root.mainloop()
