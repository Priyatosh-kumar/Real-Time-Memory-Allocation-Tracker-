import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ProcessList.memory import get_process_info, sort_by_column, export_process_info_to_csv
from Graph import update_figure

# Global variables for sorting settings.
current_sort_col = None  # Column key, e.g., "Memory (MB)" or "Process Name"
sort_reverse = False     # Toggle sort order

def on_column_click(col):
    global current_sort_col, sort_reverse
    if current_sort_col == col:
        sort_reverse = not sort_reverse
    else:
        current_sort_col = col
        sort_reverse = False
    update_treeview()

def update_overall_memory_label():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    used_mb = mem.used // (1024**2)
    total_mb = mem.total // (1024**2)
    percent = mem.percent

    swap_used_mb = swap.used // (1024**2)
    swap_total_mb = swap.total // (1024**2)
    swap_percent = swap.percent

    mem_text = (f"RAM: {used_mb} MB / {total_mb} MB ({percent}%) | "
                f"Swap: {swap_used_mb} MB / {swap_total_mb} MB ({swap_percent}%)")
    
    mem_label.config(text=mem_text)

def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    
    query = search_entry.get().strip().lower()
    processes = get_process_info()
    
    if query:
        filtered = []
        for proc in processes:
            pid_str = str(proc["PID"])
            name = proc["Process Name"].lower() if proc["Process Name"] else ""
            if query.isdigit() and query in pid_str:
                filtered.append(proc)
            elif query in name:
                filtered.append(proc)
        processes = filtered

    if current_sort_col:
        processes = sort_by_column(processes, current_sort_col, reverse=sort_reverse)
    else:
        processes.sort(key=lambda x: x.get("CPU (%)", 0), reverse=True)

    for proc in processes:
        pid = proc["PID"]
        name = proc["Process Name"]
        mem = f"{proc['Memory (MB)']:.1f}"
        cpu = f"{proc['CPU (%)']:.1f}"
        read_mb = f"{proc['Disk Read (MB)']:.2f}"
        write_mb = f"{proc['Disk Write (MB)']:.2f}"
        priority = proc["Priority"] if proc["Priority"] is not None else "N/A"
        tree.insert("", "end", values=(pid, name, mem, cpu, read_mb, write_mb, priority))
    
    update_overall_memory_label()
    root.after(1000, update_treeview)

def refresh_graph():
    update_figure(fig)
    canvas.draw_idle()
    root.after(1000, refresh_graph)

def export_data():
    export_file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Select file for exporting process data"
    )
    if export_file_path:
        try:
            export_process_info_to_csv(export_file_path)
            messagebox.showinfo("Export Successful", f"Process data has been exported to:\n{export_file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred: {e}")

# Create main window.
root = tk.Tk()
root.title("Process Monitor with Graph")

# Create separate frames for the process table (left) and the graph (right).
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill="both", expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

# --- Left Panel: Process Table and Search ---
mem_label = tk.Label(left_frame, text="Overall Memory Usage:", font=("Helvetica", 12))
mem_label.pack(pady=5)

search_frame = tk.Frame(left_frame)
search_frame.pack(fill="x", padx=5, pady=5)

search_label = tk.Label(search_frame, text="Search (Name or PID):")
search_label.pack(side="left")

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

table_frame = ttk.Frame(left_frame)
table_frame.pack(fill="both", expand=True, padx=5, pady=5)

columns = ("PID", "Process Name", "Memory (MB)", "CPU (%)", "Disk Read (MB)", "Disk Write (MB)", "Priority")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: on_column_click(c))
    tree.column(col, width=200 if col == "Process Name" else 100)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

export_button = tk.Button(left_frame, text="Export Process Data to CSV", command=export_data)
export_button.pack(pady=10)

# --- Right Panel: Embedded Graph ---
fig = Figure(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# --- Tooltip Info Label ---
def show_priority_info(event):
    info_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-40)  # Slightly above icon
    info_label.lift()

def hide_priority_info(event):
    info_label.place_forget()

info_label = tk.Label(
    root,
    text=("Process Priority determines CPU scheduling:\n"
          "Lower 'nice' = higher priority.\n"
          "Linux: -20 (highest) to 19 (lowest)\n"
          "Windows: Idle < Normal < High < Realtime"),
    bg="lightyellow",
    fg="black",
    relief="solid",
    borderwidth=1,
    font=("Arial", 9),
    justify="left",
    padx=6,
    pady=4
)
info_label.place_forget()

# ℹ️ Icon in bottom-right corner
priority_icon = tk.Label(root, text="ℹ️", cursor="hand2", font=("Arial", 12))
priority_icon.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
priority_icon.bind("<Enter>", show_priority_info)
priority_icon.bind("<Leave>", hide_priority_info)

# Start periodic updates
update_treeview()
refresh_graph()

root.mainloop()
