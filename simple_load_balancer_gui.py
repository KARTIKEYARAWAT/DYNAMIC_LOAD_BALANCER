import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math

class SimpleLoadBalancerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Load Balancer GUI")

        self.num_processors = 4  # default number of processors
        self.selected_processor_id = tk.IntVar(value=0)
        self.updating = True
        self.time_step = 0

        # Number of processors input
        ttk.Label(root, text="Number of Processors:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.num_proc_entry = ttk.Entry(root)
        self.num_proc_entry.insert(0, str(self.num_processors))
        self.num_proc_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.set_proc_button = ttk.Button(root, text="Set", command=self.set_num_processors)
        self.set_proc_button.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # Processor selection dropdown
        ttk.Label(root, text="Select Processor:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.processor_combo = ttk.Combobox(root, values=list(range(self.num_processors)), state="readonly")
        self.processor_combo.current(0)
        self.processor_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.processor_combo.bind("<<ComboboxSelected>>", self.on_processor_selected)

        # Pause/Resume button
        self.pause_button = ttk.Button(root, text="Pause Updates", command=self.toggle_updates)
        self.pause_button.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # Matplotlib figure for load graph
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title("Processor Load Over Time")
        self.ax.set_xlabel("Time (most recent)")
        self.ax.set_ylabel("Load (%)")
        self.line, = self.ax.plot([], [], 'b-')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 100)
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Text box for processor stats
        ttk.Label(root, text="Processor Statistics:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.stats_text = scrolledtext.ScrolledText(root, width=80, height=10, state='disabled')
        self.stats_text.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Configure grid weights
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Initialize artificial load data
        self.load_data = {i: [] for i in range(self.num_processors)}

        # Start periodic update
        self.update_gui()

        # Bind close window event
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def set_num_processors(self):
        try:
            num = int(self.num_proc_entry.get())
            if num <= 0:
                raise ValueError
            self.num_processors = num
            self.processor_combo['values'] = list(range(self.num_processors))
            self.processor_combo.current(0)
            self.selected_processor_id.set(0)
            self.load_data = {i: [] for i in range(self.num_processors)}
            self.time_step = 0
            self.update_gui()
        except ValueError:
            pass  # ignore invalid input

    def on_processor_selected(self, event):
        selected = self.processor_combo.current()
        self.selected_processor_id.set(selected)
        self.update_gui()

    def toggle_updates(self):
        self.updating = not self.updating
        if self.updating:
            self.pause_button.config(text="Pause Updates")
            self.update_gui()
        else:
            self.pause_button.config(text="Resume Updates")

    def generate_artificial_load(self, proc_id):
        # Generate artificial load data using sine wave + random noise
        base = 50 + 30 * math.sin(0.1 * self.time_step + proc_id)
        noise = random.uniform(-10, 10)
        load = max(0, min(100, base + noise))
        return load

    def update_gui(self):
        if not self.updating:
            return

        proc_id = self.selected_processor_id.get()

        # Update artificial load data
        load = self.generate_artificial_load(proc_id)
        data = self.load_data[proc_id]
        data.append(load)
        if len(data) > 100:
            data.pop(0)

        self.time_step += 1

        # Update load line chart
        xdata = list(range(len(data)))
        ydata = data
        self.line.set_data(xdata, ydata)
        self.ax.set_xlim(0, max(100, len(data)))
        self.ax.set_ylim(0, 100)

        # Update processor stats text with artificial data
        success = int(load * 0.8)
        failed = int(load * 0.2)
        tasks_processed = success + failed
        success_rate = (success / tasks_processed * 100) if tasks_processed > 0 else 0
        avg_exec_time = max(0.1, 1.0 - load / 100)

        text = (
            f"Processor ID: {proc_id}\n"
            f"Tasks Processed: {tasks_processed}\n"
            f"Successful Tasks: {success}\n"
            f"Failed Tasks: {failed}\n"
            f"Success Rate: {success_rate:.1f}%\n"
            f"Average Execution Time: {avg_exec_time:.3f} seconds\n"
            f"Current Load: {load:.2f}%\n"
            f"Temperature: {30 + load * 0.5:.1f}°C\n"
            f"Power Consumption: {50 + load * 0.7:.1f}W\n"
        )

        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state='disabled')

        self.canvas.draw()

        # Schedule next update
        self.root.after(1000, self.update_gui)

    def on_quit(self):
        self.updating = False

def main():
    root = tk.Tk()
    app = SimpleLoadBalancerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
