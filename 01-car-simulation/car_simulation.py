import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

print("Setup complete. Ready to simulate.")

# ── TIME SETTINGS ──────────────────────────────────────────
dt   = 0.1
time = np.arange(0, 30, dt)

# ── CAR SETTINGS ───────────────────────────────────────────
engine_power     = 400     # watts, strong cyclist
mass             = 80      # kg rider + bike
cd               = 0.88    # crouching cyclist
frontal_area     = 0.4     # m² very small
max_engine_force = 200     # Newtons
brake_force      = 500     # Newtons

# ── STARTING VALUES ────────────────────────────────────────
velocity = 0
distance = 0

# ── STORAGE ────────────────────────────────────────────────
velocities = []
distances  = []

# ── PRE-CALCULATE DRAG COEFFICIENT ─────────────────────────
drag_coefficient = 0.5 * 1.225 * cd * frontal_area

# ── SIMULATION LOOP ────────────────────────────────────────
for t in time:

    # calculate drag at current speed
    drag = drag_coefficient * velocity**2

    if t < 15:  # phase 1: accelerating
        if velocity > 0:
            engine_force = engine_power / velocity
            # cap engine force to realistic maximum
            if engine_force > max_engine_force:
                engine_force = max_engine_force
        else:
            engine_force = max_engine_force
            # car is stationary, use max force as starting push

        net_force = engine_force - drag
        # engine pushes forward, drag pushes back

    else:  # phase 2: braking
        net_force = -brake_force - drag
        # brakes and drag both push backward

    # calculate acceleration from net force
    acceleration = net_force / mass

    # update speed
    velocity = velocity + acceleration * dt

    # prevent negative velocity (car stops, doesn't reverse)
    if velocity < 0:
        velocity = 0

    # update distance
    distance = distance + velocity * dt

    # save values for graphs
    velocities.append(velocity * 3.6)  # convert m/s to km/h
    distances.append(distance)

# ── PRINT RESULTS (outside loop) ───────────────────────────
print(f"Top speed reached:      {max(velocities):.1f} km/h")
print(f"Total distance covered: {distances[-1]:.1f} meters")

# ── GRAPHS ─────────────────────────────────────────────────
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(time, velocities, color='blue')
plt.title("Speed vs Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Speed (km/h)")
plt.axvline(x=15, color='red', linestyle='--', label='Braking starts')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(time, distances, color='green')
plt.title("Distance vs Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Distance (meters)")
plt.axvline(x=15, color='red', linestyle='--', label='Braking starts')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('car_simulation(bicycle).png', dpi=150)
print("Graph saved as car_simulation(bicycle).png")