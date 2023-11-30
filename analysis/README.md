# ANALYSIS

## Things to modify and play with (Given these)
- Spawn rates of customers
- Service system of the lift (The lift picking up algorithm?)

## Things to optimize (Optimize these)
- Ideal IDLE floor
    - Based on the arrival rates
- Speed of lift
- Capacity of lift

## Thing to measure (Based on these performance metrics)
- Overall time of customer spent in system
- Wait time of customers
    - by floor
    - This is probably the KEY metric to identify
- In lift time of customers
- Utilization 
    - Number of people in lift (Capacity utilization)
    - How long lift is busy
- Customers that cannot board the first time (Only if the direction is the same)
- Number of lifts that pass by the customer, and they can't board (Regardless of lift direction?)
    - Seems a bit funny

## Data that Simulation will yield
All data will be packaged within the cycle

- System data
    - Cycle duration
    - Number of Passengers total
    - Number of Passengers moving from one floor to another
- Passenger
    - Overall time spent
    - Wait time
    - Source Floor
    - Destination Floor
    - Time in lift
    - Time it entered the system
    - Time it left the system
- Elevator
    - Active duration
    - Time spent moving UP
    - Time spent moving DOWN
    - IDLE duration
    - Number of people in the lift at any point in time
        - Only time it changes
            - Board
            - Alight
