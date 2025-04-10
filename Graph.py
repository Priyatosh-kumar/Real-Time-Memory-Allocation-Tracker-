import psutil
import random
from matplotlib.figure import Figure

# Global lists for history
memory_usage = []
page_faults = []
segment_table = []

def get_memory_usage():
    """Return current memory usage percentage."""
    return psutil.virtual_memory().percent

def get_page_faults():
    """Return swap usage as an indicator of page faults."""
    swap = psutil.swap_memory()
    return swap.used // (1024**2)  # Return used swap in MB


def get_segmentation():
    """Simulate segmentation by randomly generating values."""
    return random.randint(1, 10)  # Simulated segmentation fault count

def get_top_processes(n=5):
    """Fetches top N unique processes by memory usage, including thread count."""
    processes = []
    seen_names = set()

    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            info = proc.info
            name = info.get('name')
            if name in seen_names or info['memory_percent'] is None:
                continue
            info['threads'] = proc.num_threads()
            seen_names.add(name)
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort and return top N unique-named processes
    return sorted(processes, key=lambda p: p.get('memory_percent', 0), reverse=True)[:n]


def update_figure(fig):
    """
    Update the given matplotlib Figure with new data.
    This function appends new data, clears the figure, and draws the plots and a process table.
    """
    global memory_usage, page_faults, segment_table
    # Append new data
    memory_usage.append(get_memory_usage())
    page_faults.append(get_page_faults())
    segment_table.append(get_segmentation())

    # Limit history length to 15 entries
    if len(memory_usage) > 15:
        memory_usage.pop(0)
        page_faults.pop(0)
        segment_table.pop(0)

    # Clear the figure
    fig.clf()

    # First subplot: Memory Usage
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(memory_usage, label="Memory Usage (%)", color="blue")
    ax1.set_ylabel("Memory (%)")
    ax1.legend()

    # Second subplot: Segmentation Faults
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(segment_table, label="Segmentation Faults", color="green")
    ax2.set_ylabel("Segmentation")
    ax2.legend()

    # Third subplot: Top Processes Table
    ax3 = fig.add_subplot(3, 1, 3)
    ax3.axis("off")  # Hide axes

    # Fetch process info
    processes = get_top_processes()

    # Prepare table data
    table_data = [["PID", "Name", "Memory %", "Threads"]]
    for proc in processes:
        table_data.append([
            proc['pid'],
            proc['name'][:20],
            f"{proc['memory_percent']:.2f}%",
            proc['threads']
        ])


    # Draw table
    table = ax3.table(
        cellText=table_data,
        loc='center',
        cellLoc='left'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.5)

    fig.tight_layout()


