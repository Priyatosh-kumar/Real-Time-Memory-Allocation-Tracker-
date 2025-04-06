from setuptools import setup

APP = ['gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['psutil', 'matplotlib'],
    'includes': ['tkinter'],
    'iconfile': 'icon.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
