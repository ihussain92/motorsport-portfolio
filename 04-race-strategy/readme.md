# Race Strategy Simulator

A race strategy optimization tool that simulates every possible
pit stop strategy for a Formula 1 Grand Prix.

## What it does
- Simulates tire degradation for Soft, Medium and Hard compounds
- Tests 8 predefined pit stop strategies
- Automatically finds the optimal pit lap by testing all possibilities
- Visualizes results with lap time progression and comparison charts

## Key Results — Bahrain Grand Prix Simulation

### Strategy Comparison
| Strategy      | Total Time  | Gap     | Pit Stops |
|---------------|-------------|---------|-----------|
| M-S (lap 30)  | 91:37.60    | +0.0s   | 1         |
| S-M (lap 25)  | 91:38.88    | +1.3s   | 1         |
| S-M-S (20,20) | 91:41.00    | +3.4s   | 2         |
| S-M (lap 20)  | 91:43.48    | +5.9s   | 1         |

### Optimal Pit Lap
- Best strategy: Soft → Medium
- Optimal pit lap: Lap 34
- Optimal race time: 91:35.64

## Physics Used
- Lap time = base time + (degradation rate × tire age)
- Pit stop time loss = 22 seconds per stop
- Net force optimization across all 57 laps

## Libraries
- NumPy
- Matplotlib
- Pandas
