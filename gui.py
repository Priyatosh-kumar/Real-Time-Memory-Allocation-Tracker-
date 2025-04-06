import tkinter as tk
from tkinter import ttk,filedialog, messagebox
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Pname.memory import get_process_info, sort_by_column,export_process_data_to_csv
from Graph import update_figure



# Global variables to store sort settings.
current_sort_col = None  # Column key (e.g., "Memory (MB)" or "Process Name")
sort_reverse = False     # Toggle sort order

def on_column_click(col):
    """
    Called when a column header is clicked.
    Toggle sorting for that column and refresh the table.
    """
    global current_sort_col, sort_reverse
    if current_sort_col == col:
        sort_reverse = not sort_reverse
    else:
        current_sort_col = col
        sort_reverse = False
    update_treeview()

def update_overall_memory_label():
    """
    Updates the overall memory usage label using psutil.virtual_memory().
    """
    mem = psutil.virtual_memory()
    used_mb = mem.used // (1024**2)
    total_mb = mem.total // (1024**2)
    percent = mem.percent
    mem_text = f"Overall Memory Usage: {used_mb} MB / {total_mb} MB ({percent}%)"
    mem_label.config(text=mem_text)

def update_treeview():
    """
    Update the treeview with the current list of processes,
    applying the current sort settings, and update overall memory label.
    """
    # Clear existing rows.
    for row in tree.get_children():
        tree.delete(row)
    
    processes = get_process_info()

    if current_sort_col:
        processes = sort_by_column(processes, current_sort_col, reverse=sort_reverse)
    else:
        # Default sort by CPU usage descending.
        processes.sort(key=lambda x: x.get("CPU (%)", 0), reverse=True)

    for proc in processes:
        pid = proc["PID"]
        name = proc["Process Name"]
        mem = f"{proc['Memory (MB)']:.1f}"
        cpu = f"{proc['CPU (%)']:.1f}"
        read_kb = f"{proc['Disk Read (KB)']:.1f}"
        write_kb = f"{proc['Disk Write (KB)']:.1f}"
        priority = proc["Priority"] if proc["Priority"] is not None else "N/A"
        tree.insert("", "end", values=(pid, name, mem, cpu, read_kb, write_kb, priority))
    
    update_overall_memory_label()
    root.after(1000, update_treeview)

def export_data_with_dialog():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Process Data As"
    )
    if file_path:  # If user didn't cancel
        export_process_data_to_csv(file_path)
        messagebox.showinfo("Success", f"Process data exported to:\n{file_path}")



def refresh_graph():
    """
    Update the graph by calling update_figure and redrawing the canvas.
    """
    update_figure(fig)
    canvas.draw_idle()
    root.after(1000, refresh_graph)

# Create the main window.
root = tk.Tk()
root.title("Process Monitor with Graph")

# Create main frames for left (table) and right (graph) panels.
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill="both", expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

# --- Left Panel: Process Table ---
mem_label = tk.Label(left_frame, text="Overall Memory Usage:", font=("Helvetica", 12))
mem_label.pack(pady=5)
# Export Button
export_button = tk.Button(left_frame, text="Export to CSV", command=export_data_with_dialog)
export_button.pack(pady=5)


table_frame = ttk.Frame(left_frame)
table_frame.pack(fill="both", expand=True)

# Define columns.
columns = ("PID", "Process Name", "Memory (MB)", "CPU (%)", "Disk Read (KB)", "Disk Write (KB)", "Priority")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: on_column_click(c))
    tree.column(col, width=200 if col == "Process Name" else 100)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# --- Right Panel: Embedded Graph ---
fig = Figure(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Start periodic updates.
update_treeview()
refresh_graph()

root.mainloop()
