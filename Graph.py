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
    """Simulate page faults using swap memory usage."""
    swap = psutil.swap_memory()
    return swap.total  # Using total swap memory to represent paging activity

def get_segmentation():
    """Estimate segmentation faults using swap-ins (more realistic)."""
    swap_info = psutil.swap_memory()
    return swap_info.sin / 1024  # Convert bytes to KB


def get_top_processes(n=5):
    """Fetches top N processes by memory usage safely."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            info = proc.info
            if info['memory_percent'] is not None:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(processes, key=lambda p: p.get('memory_percent', 0), reverse=True)[:n]

def update_figure(fig):
    """
    Update the given matplotlib Figure with new data.
    This function appends new data, clears the figure, and draws the plots.
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

    # Second subplot: Segmentation Faults (for illustration)
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(segment_table, label="Segmentation Faults", color="green")
    ax2.set_ylabel("Segmentation")
    ax2.legend()

    # Display top processes text
    processes = get_top_processes()
    text_x, text_y = 0.05, 0.25
    fig.text(text_x, text_y + 0.05, "**Top Processes (by Memory Usage):**",
             fontsize=12, fontweight='bold', ha='left', color="black")
    for process in processes:
        fig.text(text_x, text_y,
                 f"{process['name']} (PID: {process['pid']}) - {process['memory_percent']:.2f}% RAM",
                 fontsize=10, ha='left', va='bottom', color="black")
        text_y -= 0.05

    fig.tight_layout()
