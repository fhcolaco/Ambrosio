# Map Route Finder

This project is a route finder. It uses different algorithms to find the optimal route between two cities.


## How to Run

1. Ensure that you have Python installed on your machine.
    -   For windows systems `winget install python --source winget`
    -   For linux systems `sudo apt-get install python3`
    -   For MacOs systems
        -   Install Homebrew `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
        -   Install Python `brew install python3`

2. Run `main.py` to start the application (eg. on terminal type `python main.py`).

## Algorithms

The application supports the following algorithms for finding the route:

- Uniform Cost Search
- Depth-Limited Search (DLS)
- Greedy Search
- A* Search

## Files

- `main.py`: Main script that runs the application.

- `ui.py`: Handles the user interface of the application.

- `algorithms.py`: Contains the implementation of the different algorithms used for finding the route.

- `city.py`: Defines the City class, which represents a city with its location and connections.

- `functions.py`: Contains various utility functions.

- `requirements.txt`: List of Python packages that the project depends on.
  
- `installrequirements.py`: Checks if the necessary Python packages are installed. If not, it installs them.

- `maps\`: This folder contains .txt .xlsx and .csv files with a list of cities and their connections.

- `adittional_files\`: This folder contains other .txt files relevant to the project