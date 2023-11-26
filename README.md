# 40.305 Project - Elevator Group Control

Project for 40.305 Adv Topics in Stochastic Modelling
Based on Elevator Group Control Problem

## Installation

Create a new virtual environment and activate it:

```shell
python -m venv venv
./venv/Scripts/activate
```

Install the requirements:

```shell
pip install -r requirements.txt
```

## Assumptions

- Once an elevator reaches a certain floor and alights passengers, they will have to open their doors for a fixed amount of time before moving off
- Passengers alight and board instantaneously
- Once an elevator starts moving to an Idle position, it cannot be interrupted.
