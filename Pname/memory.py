import psutil

def get_process_info():
    """
    Gather information for each process:
      - PID (int)
      - Process Name (str)
      - Memory (MB) as float
      - CPU (%) as float
      - Disk Read (KB) as float
      - Disk Write (KB) as float
      - Priority (nice value)
    Returns a list of dictionaries.
    """
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            mem = proc.memory_info().rss / (1024**2)  # Memory in MB
            cpu = proc.cpu_percent(interval=None)
            try:
                io_counters = proc.io_counters()
                read_kb = io_counters.read_bytes / 1024
                write_kb = io_counters.write_bytes / 1024
            except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                read_kb = write_kb = 0.0
            try:
                priority = proc.nice()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                priority = None

            process_list.append({
                "PID": pid,
                "Process Name": name,
                "Memory (MB)": mem,
                "CPU (%)": cpu,
                "Disk Read (KB)": read_kb,
                "Disk Write (KB)": write_kb,
                "Priority": priority
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_list

def sort_by_column(processes, col, reverse=False):
    """
    Sorts the list of processes based on column values.
    Ensures numeric values are sorted correctly.
    """
    def key_func(proc):
        value = proc.get(col)
        if isinstance(value, (int, float)):
            return value
        return str(value).lower() if value is not None else ""

    return sorted(processes, key=key_func, reverse=reverse)

#New Feature.

import csv
from datetime import datetime
from Pname.memory import get_process_info  # Add this if not already there

def export_process_data_to_csv(filename=None):
    processes = get_process_info()  # Fetch processes internally

    if not processes:
        print("No processes to export.")
        return

    fieldnames = ["PID", "Process Name", "Memory (MB)", "CPU (%)", "Disk Read (KB)", "Disk Write (KB)", "Priority"]

    if not filename:

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"process_data_{timestamp}.csv"

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for process in processes:
                writer.writerow(process)
        print(f"[+] Exported process data to {filename}")
    except Exception as e:
        print(f"[!] Failed to export CSV: {e}")
