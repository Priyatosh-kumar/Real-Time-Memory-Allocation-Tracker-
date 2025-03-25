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
