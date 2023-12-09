# 40.305 Project - Elevator Group Control

Project for 40.305 Adv Topics in Stochastic Modelling
Based on Elevator Group Control Problem

## Data Analysed
- Wait Times of passengers by floor
- Idle Times of each elevator
- Number of passengers each elevator service

## Algorithms Tested
- Random Assignment (Control)
- Zoning (Sectoring)
- Nearest Elevator (Feasibility Score)
- Lifts dedicated to moving up and down
- Custom Feasibility Score (Based on IDLE, distance, movement)

## Various Arrival distributions
- Uniform
- 1st Floor heavy
- Multi-floor heavy

## Installation
Requires Python >= 3.11
Create a new virtual environment and activate it:

```shell
python -m venv venv
./venv/Scripts/activate
```

Install the requirements:

```shell
pip install -r requirements.txt
```

## Running the simulation

To run the simulation, simply run 

```shell
python main.py
```

from the main project folder

Various argparsers will be implemented soon to specify features of the simulation

Code for the analysis can be found in `/analysis`.

## Running interactively with Jupyter Notebook

A sample jupyter notebook is shown in `interactive_analysis.ipynb`
The simulation can be imported as shown in the notebook.

