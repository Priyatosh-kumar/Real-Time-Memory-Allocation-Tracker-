import psutil
import csv
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
            cpu = proc.cpu_percent(interval=None) / psutil.cpu_count(logical=True)

            try:
                io_counters = proc.io_counters()
                read_mb = io_counters.read_bytes / (1024 ** 2)
                write_mb = io_counters.write_bytes / (1024 ** 2)

            except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                read_mb = write_mb = 0.0
            try:
                priority = proc.nice()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                priority = None

            process_list.append({
    "PID": pid,
    "Process Name": name,
    "Memory (MB)": mem,
    "CPU (%)": cpu,
    "Disk Read (MB)": read_mb,
    "Disk Write (MB)": write_mb,
    "Priority": priority
})

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_list

def sort_by_column(processes, col, reverse=False):
    """
    Sorts the list of process dictionaries based on the column key 'col'.
    Uses a numeric sort if the values are numbers, or a string sort otherwise.
    """
    # Determine the type based on the first non-None value.
    for proc in processes:
        value = proc.get(col)
        if value is not None:
            if isinstance(value, (int, float)):
                key_func = lambda x: x.get(col, 0)
            else:
                key_func = lambda x: str(x.get(col, "")).lower()
            break
    else:
        key_func = lambda x: str(x.get(col, "")).lower()

    processes.sort(key=key_func, reverse=reverse)
    return processes


def export_process_info_to_csv(filename="process_data.csv"):
    """
    Exports the process info (as returned by get_process_info()) into a CSV file.
    """
    # Retrieve current process information.
    processes = get_process_info()
    
    # Define fieldnames matching the keys in your process dictionaries.
    fieldnames = [
        "PID", 
        "Process Name", 
        "Memory (MB)", 
        "CPU (%)", 
        "Disk Read (MB)", 
        "Disk Write (MB)", 
        "Priority"
    ]
    
    # Open the file with write permissions and create a CSV writer.
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row.
        writer.writeheader()
        
        # Write each process' data.
        for proc in processes:
            writer.writerow(proc)
