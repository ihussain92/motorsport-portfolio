import fastf1
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# create cache folder if it doesn't exist
if not os.path.exists('cache'):
    os.makedirs('cache')

fastf1.Cache.enable_cache('cache')
# this creates a folder called 'cache' in your project folder
# downloaded data gets saved here
# next time you run the code it loads from cache (much faster)
print("Libraries loaded successfully.") 

# ── LOAD SESSION ───────────────────────────────────────────
print("Loading session data... (first time takes 1-2 minutes)")

session = fastf1.get_session(
    2023,        # year
    'Bahrain',   # race name
    'Q'          # Q = Qualifying
)

session.load()

print("Session loaded successfully.")
print(f"Event: {session.event['EventName']}")

# ── GET DRIVER FASTEST LAP ─────────────────────────────────
verstappen = session.laps.pick_drivers('VER').pick_fastest()
# session.laps         → all laps from all drivers in this session
# .pick_drivers('VER') → filter to only Verstappen's laps
# .pick_fastest()      → from those laps pick the single fastest one

print(f"Verstappen fastest lap time: {verstappen['LapTime']}")

# ── GET HAMILTON'S FASTEST LAP ─────────────────────────────
hamilton = session.laps.pick_drivers('HAM').pick_fastest()
hamilton_telemetry = hamilton.get_telemetry()

print(f"Verstappen fastest lap: {verstappen['LapTime']}")
print(f"Hamilton fastest lap:   {hamilton['LapTime']}")

# ── GET TELEMETRY ──────────────────────────────────────────
telemetry = verstappen.get_telemetry()
# this gives us all the sensor data for that specific lap
# speed, throttle, brake, gear, RPM at every moment

print(telemetry.columns.tolist())
# print all available data channels so we can see what we have

# ── PLOT SPEED TRACE ───────────────────────────────────────
plt.figure(figsize=(15, 6))

plt.plot(
    telemetry['Distance'],   # x axis = distance around the lap
    telemetry['Speed'],      # y axis = speed at each point
    color='blue',
    label='Verstappen'
)

# labels and formatting
plt.title("Verstappen - Fastest Lap Speed Trace\n2023 Bahrain Grand Prix Qualifying")
plt.xlabel("Distance (meters)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('verstappen_speed_trace.png', dpi=150)
print("Speed trace saved as verstappen_speed_trace.png")


# ── PLOT BOTH DRIVERS ──────────────────────────────────────
plt.figure(figsize=(15, 8))

# verstappen speed trace
plt.plot(
    telemetry['Distance'],
    telemetry['Speed'],
    color='blue',
    label='Verstappen',
    linewidth=2
)

# hamilton speed trace
plt.plot(
    hamilton_telemetry['Distance'],
    hamilton_telemetry['Speed'],
    color='red',
    label='Hamilton',
    linewidth=2,
    linestyle='--'    # dashed line so we can tell them apart
)

# labels and formatting
plt.title("Verstappen vs Hamilton - Fastest Lap Speed Trace\n2023 Bahrain Grand Prix Qualifying")
plt.xlabel("Distance (meters)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('ver_vs_ham_speed_trace.png', dpi=150)
print("Comparison graph saved as ver_vs_ham_speed_trace.png")


# ── THROTTLE AND BRAKE COMPARISON ──────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(15, 12))
# creates 3 graphs stacked vertically
# axes[0] = top graph    = speed
# axes[1] = middle graph = throttle
# axes[2] = bottom graph = brake

# ── TOP GRAPH: SPEED ───────────────────────────────────────
axes[0].plot(
    telemetry['Distance'],
    telemetry['Speed'],
    color='blue',
    label='Verstappen',
    linewidth=2
)
axes[0].plot(
    hamilton_telemetry['Distance'],
    hamilton_telemetry['Speed'],
    color='red',
    label='Hamilton',
    linewidth=2,
    linestyle='--'
)
axes[0].set_ylabel("Speed (km/h)")
axes[0].legend()
axes[0].grid(True)
axes[0].set_title("Verstappen vs Hamilton - Speed, Throttle and Brake\n2023 Bahrain Grand Prix Qualifying")

# ── MIDDLE GRAPH: THROTTLE ─────────────────────────────────
axes[1].plot(
    telemetry['Distance'],
    telemetry['Throttle'],
    color='blue',
    label='Verstappen',
    linewidth=2
)
axes[1].plot(
    hamilton_telemetry['Distance'],
    hamilton_telemetry['Throttle'],
    color='red',
    label='Hamilton',
    linewidth=2,
    linestyle='--'
)
axes[1].set_ylabel("Throttle (%)")
# 100 = full throttle, 0 = completely off throttle
axes[1].legend()
axes[1].grid(True)

# ── BOTTOM GRAPH: BRAKE ────────────────────────────────────
axes[2].plot(
    telemetry['Distance'],
    telemetry['Brake'].astype(int),
    # .astype(int) converts True/False to 1/0
    # 1 = brakes applied, 0 = brakes not applied
    color='blue',
    label='Verstappen',
    linewidth=2
)
axes[2].plot(
    hamilton_telemetry['Distance'],
    hamilton_telemetry['Brake'].astype(int),
    color='red',
    label='Hamilton',
    linewidth=2,
    linestyle='--'
)
axes[2].set_ylabel("Brake (1=on, 0=off)")
axes[2].set_xlabel("Distance (meters)")
axes[2].legend()
axes[2].grid(True)

plt.tight_layout()
plt.savefig('ver_vs_ham_full_trace.png', dpi=150)
print("Full trace saved as ver_vs_ham_full_trace.png")

# ── BRAKING ZONE DETECTION ─────────────────────────────────

# we use verstappen's telemetry for this analysis
# first make a clean copy so we don't modify the original
data = telemetry[['Distance', 'Speed', 'Brake']].copy()
# we only need 3 columns:
# Distance → where on track
# Speed    → how fast
# Brake    → is brake pedal pressed

# reset index so rows are numbered 0, 1, 2, 3...
data = data.reset_index(drop=True)

print(f"Total data points in this lap: {len(data)}")
print(data.head(10))
# .head(10) shows first 10 rows so we can see the data structure


# ── FIND BRAKING ZONES ─────────────────────────────────────
braking_zones = []
# empty list to store each braking zone we find

in_braking_zone = False
# flag to track whether we are currently inside a braking zone
# False = not braking, True = braking happening

zone_start_distance = 0
zone_start_speed    = 0

# go through every data point one by one
for i in range(1, len(data)):

    current_speed  = data['Speed'][i]
    previous_speed = data['Speed'][i - 1]
    current_distance = data['Distance'][i]
    brake_applied  = data['Brake'][i]

    # BRAKING ZONE STARTS when:
    # brake pedal is pressed AND speed is dropping
    if brake_applied and current_speed < previous_speed and not in_braking_zone:
        in_braking_zone      = True
        zone_start_distance  = current_distance
        zone_start_speed     = current_speed
        # remember where and how fast when braking started

    # BRAKING ZONE ENDS when:
    # brake pedal is released OR speed starts rising again
    if in_braking_zone and (not brake_applied or current_speed > previous_speed):
        in_braking_zone = False
        zone_end_distance = current_distance
        zone_end_speed    = current_speed

        speed_drop = zone_start_speed - zone_end_speed
        # how much speed was lost in this braking zone

        zone_length = zone_end_distance - zone_start_distance
        # how many meters the braking zone lasted

        # only save braking zones where speed dropped more than 30 km/h
        # this filters out tiny speed fluctuations that are not real corners
        if speed_drop > 30:
            braking_zones.append({
                'zone_number'   : len(braking_zones) + 1,
                'start_distance': round(zone_start_distance),
                'end_distance'  : round(zone_end_distance),
                'zone_length'   : round(zone_length),
                'entry_speed'   : round(zone_start_speed),
                'exit_speed'    : round(zone_end_speed),
                'speed_drop'    : round(speed_drop)
            })

print(f"\nTotal braking zones detected: {len(braking_zones)}")

# ── PRINT BRAKING ZONES ────────────────────────────────────
print("\n--- Verstappen Braking Zones ---")
print(f"{'Zone':<6} {'Start':>8} {'End':>8} {'Length':>8} {'Entry':>8} {'Exit':>8} {'Drop':>8}")
print(f"{'':─<6} {'(m)':>8} {'(m)':>8} {'(m)':>8} {'km/h':>8} {'km/h':>8} {'km/h':>8}")

for zone in braking_zones:
    print(
        f"{zone['zone_number']:<6}"
        f"{zone['start_distance']:>8}"
        f"{zone['end_distance']:>8}"
        f"{zone['zone_length']:>8}"
        f"{zone['entry_speed']:>8}"
        f"{zone['exit_speed']:>8}"
        f"{zone['speed_drop']:>8}"
    )

    # ── PLOT SPEED TRACE WITH BRAKING ZONES HIGHLIGHTED ────────
plt.figure(figsize=(15, 6))

# draw the speed trace
plt.plot(
    data['Distance'],
    data['Speed'],
    color='blue',
    linewidth=2,
    label='Verstappen speed'
)

# highlight each braking zone with a red shaded area
for zone in braking_zones:
    plt.axvspan(
        zone['start_distance'],
        zone['end_distance'],
        color='red',
        alpha=0.2,
        # alpha = transparency, 0.2 means lightly shaded
        label='Braking zone' if zone == braking_zones[0] else ""
        # only add label once to avoid duplicates in legend
    )

    # add zone number as text above each shaded area
    plt.text(
        (zone['start_distance'] + zone['end_distance']) / 2,
        # position text in middle of braking zone
        310,
        # height of text on graph
        f"Z{zone['zone_number']}",
        # label text e.g. Z1, Z2, Z3
        fontsize=8,
        ha='center',
        color='red'
    )

plt.title("Verstappen Fastest Lap - Braking Zones Detected\n2023 Bahrain Grand Prix Qualifying")
plt.xlabel("Distance (meters)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('braking_zones.png', dpi=150)
print("\nBraking zones graph saved as braking_zones.png")

# ── HAMILTON BRAKING ZONE DETECTION ────────────────────────
ham_data = hamilton_telemetry[['Distance', 'Speed', 'Brake']].copy()
ham_data = ham_data.reset_index(drop=True)

ham_braking_zones = []
# empty list to store Hamilton's braking zones

in_braking_zone     = False
zone_start_distance = 0
zone_start_speed    = 0

for i in range(1, len(ham_data)):
    current_speed    = ham_data['Speed'][i]
    previous_speed   = ham_data['Speed'][i - 1]
    current_distance = ham_data['Distance'][i]
    brake_applied    = ham_data['Brake'][i]

    if brake_applied and current_speed < previous_speed and not in_braking_zone:
        in_braking_zone     = True
        zone_start_distance = current_distance
        zone_start_speed    = current_speed

    if in_braking_zone and (not brake_applied or current_speed > previous_speed):
        in_braking_zone   = False
        zone_end_distance = current_distance
        zone_end_speed    = current_speed
        speed_drop        = zone_start_speed - zone_end_speed
        zone_length       = zone_end_distance - zone_start_distance

        if speed_drop > 30:
            ham_braking_zones.append({
                'zone_number'   : len(ham_braking_zones) + 1,
                'start_distance': round(zone_start_distance),
                'end_distance'  : round(zone_end_distance),
                'zone_length'   : round(zone_length),
                'entry_speed'   : round(zone_start_speed),
                'exit_speed'    : round(zone_end_speed),
                'speed_drop'    : round(speed_drop)
            })

print(f"Hamilton braking zones detected: {len(ham_braking_zones)}")


# ── PRINT COMPARISON TABLE ─────────────────────────────────
print("\n--- Braking Zone Comparison: Verstappen vs Hamilton ---")
print(f"\n{'Zone':<6} {'VER Start':>10} {'HAM Start':>10} {'Difference':>12} {'Who brakes later':>18}")
print(f"{'':─<6} {'(m)':>10} {'(m)':>10} {'(m)':>12} {'':>18}")

for i, ver_zone in enumerate(braking_zones):
    ver_start = ver_zone['start_distance']

    # find the Hamilton zone closest to this Verstappen zone
    # instead of matching by number, match by track position
    closest_ham_zone = min(
        ham_braking_zones,
        key=lambda z: abs(z['start_distance'] - ver_start)
        # find Hamilton zone whose start distance is
        # closest to Verstappen's zone start distance
    )

    ham_start = closest_ham_zone['start_distance']
    diff      = ham_start - ver_start

    # only show if they are within 200 meters of each other
    # otherwise they are not the same corner
    if abs(diff) > 200:
        print(f"{i+1:<6}{ver_start:>10}{'No match':>10}{'---':>12}{'Cannot compare':>18}")
        continue

    if diff > 0:
        later = f"Hamilton by {diff}m"
    elif diff < 0:
        later = f"Verstappen by {abs(diff)}m"
    else:
        later = "Same"

    print(f"{i+1:<6}{ver_start:>10}{ham_start:>10}{diff:>+12}{later:>18}")