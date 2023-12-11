# 40.305 Project - Elevator Group Control

Project for 40.305 Adv Topics in Stochastic Modelling
Based on Elevator Group Control Problem

For more information about the project report details, please go to the [wiki](https://github.com/becauselol/40.305-Project---Elevator-Group-Control/wiki)

## Installation and running the simulation
Requires Python >= 3.10
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


## Objectives to Minimize
- Wait Times of passengers by floor
- Idle Times of each elevator

## Variables Tested
### Controller Type
- Random Assignment (Control)
- Zoning (Sectoring)
- Nearest Elevator (Feasibility Score)

### Idle Floor Configuration

## Various Arrival distributions
To test the limits of various Idle Configurations, we experimented with different kinds of arrival distributions
Namely
- Uniform Arrival Distribution
- Ground Floor Heavy Arrival Distribution

### Uniform Arrival Assumptions
- Assumes that an equal amount of people arrive at every floor
- Equal proportion of people want to go from one floor to every other floor

### Ground Floor Heavy
- A fixed proportion of people arriving and leaving every floor
- An equal proportion of people go from ground floor to every other floor
- Same proportion of people going from ground to other floors is same as proportion going from other floors to ground
- Remaining proportion of people going between the remaining floors are split equally

## Future Works
- Update algorithm of elevator movement. Current one has some flaws in logic
- Also create elevator that has capacity constraints, currently there are no limitations to capacity

