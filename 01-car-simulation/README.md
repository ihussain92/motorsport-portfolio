# Car Acceleration Simulator

A physics-based vehicle simulation built in Python.

## What it does
Simulates how different vehicles accelerate and brake
using real physics equations including:
- Newton's Second Law (F = ma)
- Aerodynamic drag force
- Power to force conversion

## Results
| Vehicle        | Top Speed  | Distance (15s) |
|----------------|------------|----------------|
| F1 Car         | 344 km/h   | 1190 meters    |
| Toyota Corolla | 145 km/h   | 400 meters     |
| Heavy Truck    | 123 km/h   | 502 meters     |
| Bicycle        | 37 km/h    | 117 meters     |

## Physics Used
- Drag = 0.5 × air_density × Cd × frontal_area × v²
- Net Force = Engine Force - Drag
- Acceleration = Net Force / Mass

## Libraries
- NumPy
- Matplotlib
