# Real-Time-Memory-Allocation-Tracker-
This project is a Python tool that visualizes memory allocation in real time. It not only tracks overall memory usage but also simulates paging and segmentation metrics, providing insights into how memory is allocated and managed on your system.
Overview

The application continuously monitors system memory and displays the following key metrics:

**Memory Allocation:**
    Shows current memory usage as a percentage of total available memory.

**Paging:**
    Simulates paging activity by using swap memory metrics.

  **Segmentation:**
    Simulates segmentation by generating random values, illustrating potential segmentation events.

  **Process Information:**
    Displays a detailed list of processes including memory usage, CPU utilization, disk I/O, and process priority.

The tool combines a graphical visualization with a process list in a user-friendly Tkinter GUI.

**File Structure**

    Real-Time-Memory-Allocation-Tracker-/
    └── ProcessList/
      └── memory.py
    ├── Graph.py
    ├── gui.py
    ├── requirements.txt




**Stand-Alone Release Installation**

To run the application, please download the stand-alone release package for macOS or Linux from the [Releases](https://github.com/Priyatosh-kumar/Real-Time-Memory-Allocation-Tracker-/releases) section. Detailed installation and usage instructions specific to each platform are provided in the release notes. Follow those instructions to install and launch the application on your system.


**Running from Source**

If you prefer to run the application directly from source, follow these steps:

**Clone the Repository:**

    git clone https://github.com/Priyatosh-kumar/Real-Time-Memory-Allocation-Tracker-
    cd Real-Time-Memory-Allocation-Tracker-

**Create and Activate a Virtual Environment:**
```
# Create the virtual environment
    python3 -m venv venv

# Activate it (Linux/macOS)
    source venv/bin/activate

# On Windows
    venv\Scripts\activate

```
**Install Dependencies:**

Ensure you have Python 3.6 or later installed, then run:

    pip install -r requirements.txt

**Start the Application:**

Launch the application by running:

    python gui.py
