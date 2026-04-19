import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

print("Setup complete. Ready to simulate race strategy.")

# ── RACE SETTINGS ──────────────────────────────────────────
TOTAL_LAPS   = 57      # Bahrain Grand Prix = 57 laps
PIT_LOSS     = 22      # seconds lost every time car pits

# ── TIRE COMPOUNDS ─────────────────────────────────────────
# each compound has two properties:
# base_time  = lap time in seconds on fresh tires
# degr_rate  = how many seconds slower per lap as tire wears
# Replace your TIRES dictionary with this:
TIRES = {
    'Soft': {
        'base_time' : 95.0,
        'degr_rate' : 0.05,   # reduced from 0.08
        'color'     : 'red'
    },
    'Medium': {
        'base_time' : 96.0,
        'degr_rate' : 0.03,   # reduced from 0.05
        'color'     : 'yellow'
    },
    'Hard': {
        'base_time' : 97.0,
        'degr_rate' : 0.02,   # reduced from 0.03
        'color'     : 'white'
    }
}

print(f"Race: Bahrain Grand Prix")
print(f"Total laps: {TOTAL_LAPS}")
print(f"Pit stop time loss: {PIT_LOSS} seconds")
print(f"Tire compounds: {list(TIRES.keys())}")

# ── LAP TIME CALCULATOR ────────────────────────────────────
def calculate_lap_time(tire_compound, tire_age):
    """
    Calculate lap time based on tire compound and age.
    
    tire_compound → which tire is on the car (Soft/Medium/Hard)
    tire_age      → how many laps have been done on this tire
    
    Example:
    calculate_lap_time('Soft', 0)  → 95.0 seconds (fresh soft)
    calculate_lap_time('Soft', 10) → 95.8 seconds (10 laps old)
    calculate_lap_time('Soft', 20) → 96.6 seconds (20 laps old)
    """
    base_time  = TIRES[tire_compound]['base_time']
    degr_rate  = TIRES[tire_compound]['degr_rate']

    lap_time = base_time + (degr_rate * tire_age)
    # as tire age grows, lap time gets bigger (slower)

    return lap_time

# ── TEST THE CALCULATOR ────────────────────────────────────
print("\n--- Tire Degradation Test ---")
print(f"\n{'Tire Age':<10} {'Soft':>10} {'Medium':>10} {'Hard':>10}")
print(f"{'(laps)':<10} {'(seconds)':>10} {'(seconds)':>10} {'(seconds)':>10}")
print(f"{'':─<10} {'':─>10} {'':─>10} {'':─>10}")

for age in [0, 5, 10, 15, 20, 25, 30]:
    soft_time   = calculate_lap_time('Soft',   age)
    medium_time = calculate_lap_time('Medium', age)
    hard_time   = calculate_lap_time('Hard',   age)

    print(f"{age:<10} {soft_time:>10.2f} {medium_time:>10.2f} {hard_time:>10.2f}")

# ── STRATEGY SIMULATOR ─────────────────────────────────────
def simulate_strategy(strategy):
    """
    Simulate a full race using a given strategy.
    
    strategy is a list of tuples:
    Each tuple = (compound, number of laps on that compound)
    
    Example:
    [('Soft', 20), ('Medium', 37)]
    = start on Soft for 20 laps
    = pit and switch to Medium for remaining 37 laps
    
    Returns:
    total_time  = total race time in seconds
    lap_times   = list of every lap time during race
    compounds   = which compound was used on each lap
    """

    # validate strategy
    # total laps in strategy must equal race distance
    total_strategy_laps = sum(laps for _, laps in strategy)
    if total_strategy_laps != TOTAL_LAPS:
        print(f"Warning: strategy covers {total_strategy_laps} laps but race is {TOTAL_LAPS} laps")
        return None

    total_time = 0       # accumulate total race time
    lap_times  = []      # store every lap time
    compounds  = []      # store compound used each lap

    # go through each stint in the strategy
    for stint_number, (compound, stint_laps) in enumerate(strategy):

        # add pit stop time loss for every stint except the first
        if stint_number > 0:
            total_time += PIT_LOSS
            # first stint has no pit stop before it
            # every subsequent stint costs 22 seconds

        # simulate each lap in this stint
        for lap_in_stint in range(stint_laps):
            lap_time = calculate_lap_time(compound, lap_in_stint)
            # lap_in_stint = tire age at this point
            # starts at 0 (fresh) and counts up

            total_time += lap_time
            lap_times.append(lap_time)
            compounds.append(compound)

    return {
        'total_time' : total_time,
        'lap_times'  : lap_times,
        'compounds'  : compounds
    }

# ── STRATEGIES TO TEST ─────────────────────────────────────
strategies = {

    # ── ONE STOP STRATEGIES ────────────────────────────────
    'S-M (lap 20)': [('Soft', 20),   ('Medium', 37)],
    # start Soft 20 laps → pit → Medium to end

    'S-M (lap 25)': [('Soft', 25),   ('Medium', 32)],
    # start Soft 25 laps → pit → Medium to end

    'S-H (lap 20)': [('Soft', 20),   ('Hard', 37)],
    # start Soft 20 laps → pit → Hard to end

    'M-H (lap 25)': [('Medium', 25), ('Hard', 32)],
    # start Medium 25 laps → pit → Hard to end

    'M-S (lap 30)': [('Medium', 30), ('Soft', 27)],
    # start Medium 30 laps → pit → Soft to end
    # saving Soft for end = fresh fast tire for final laps

    # ── TWO STOP STRATEGIES ────────────────────────────────
    'S-M-S (20,20)': [('Soft', 20),   ('Medium', 20), ('Soft', 17)],
    # Soft 20 → Medium 20 → Soft 17
    # aggressive two stop

    'S-H-S (15,25)': [('Soft', 15),   ('Hard', 25),   ('Soft', 17)],
    # Soft 15 → Hard 25 → Soft 17
    # mixed two stop

    'M-H-S (20,20)': [('Medium', 20), ('Hard', 20),   ('Soft', 17)],
    # Medium 20 → Hard 20 → Soft 17
    # save Soft for end
}

print(f"\nStrategies to simulate: {len(strategies)}")
print("Simulating all strategies...")

# ── RUN ALL SIMULATIONS ────────────────────────────────────
results = {}

for strategy_name, strategy in strategies.items():
    result = simulate_strategy(strategy)
    if result:
        results[strategy_name] = result

print(f"Simulations complete: {len(results)} strategies calculated")

# ── PRINT RESULTS TABLE ────────────────────────────────────
print("\n--- Race Strategy Results ---")
print(f"\n{'Strategy':<20} {'Total Time':>12} {'vs Best':>10} {'Pit Stops':>10}")
print(f"{'':─<20} {'(mm:ss)':>12} {'(seconds)':>10} {'':>10}")

# sort strategies by total time (fastest first)
sorted_results = sorted(
    results.items(),
    key=lambda x: x[1]['total_time']
)
# lambda x: x[1]['total_time']
# → sort by total_time value inside each result dictionary

best_time = sorted_results[0][1]['total_time']
# fastest strategy total time = our reference point

for strategy_name, result in sorted_results:
    total_time = result['total_time']

    # convert total seconds to mm:ss format
    minutes = int(total_time // 60)
    seconds = total_time % 60

    # calculate gap to best strategy
    gap = total_time - best_time

    # count pit stops = number of stints minus 1
    pit_stops = len(strategies[strategy_name]) - 1

    # add trophy for best strategy
    marker = " 🏆" if gap == 0 else ""

    print(
        f"{strategy_name + marker:<20}"
        f"{minutes}:{seconds:05.2f}{'':>4}"
        f"{gap:>+10.1f}"
        f"{pit_stops:>10}"
    )

# ── GRAPH 1: LAP TIME PROGRESSION ─────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(15, 12))
fig.patch.set_facecolor('black')

# plot lap time progression for top 4 strategies only
# plotting all 8 would be too crowded
top_4 = sorted_results[:4]

for strategy_name, result in top_4:
    axes[0].plot(
        range(1, TOTAL_LAPS + 1),
        result['lap_times'],
        linewidth=2,
        label=strategy_name
    )

axes[0].set_title(
    "Lap Time Progression — Top 4 Strategies",
    color='white',
    fontsize=14
)
axes[0].set_xlabel("Lap Number", color='white')
axes[0].set_ylabel("Lap Time (seconds)", color='white')
axes[0].set_facecolor('black')
axes[0].tick_params(colors='white')
axes[0].grid(True, alpha=0.3)
axes[0].legend(
    facecolor='black',
    labelcolor='white',
    fontsize=10
)
for spine in axes[0].spines.values():
    spine.set_edgecolor('white')

# ── GRAPH 2: STRATEGY COMPARISON BAR CHART ─────────────────
strategy_names = [name for name, _ in sorted_results]
gaps           = [result['total_time'] - best_time
                  for _, result in sorted_results]
# gap from best strategy for each strategy

colors = []
for gap in gaps:
    if gap == 0:
        colors.append('gold')      # winner = gold
    elif gap < 10:
        colors.append('lime')      # very close = green
    elif gap < 30:
        colors.append('orange')    # moderate gap = orange
    else:
        colors.append('red')       # far behind = red

bars = axes[1].barh(
    strategy_names,
    gaps,
    color=colors,
    edgecolor='white',
    linewidth=0.5
)
# barh = horizontal bar chart
# easier to read strategy names on y axis

# add gap value label on each bar
for bar, gap in zip(bars, gaps):
    axes[1].text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f'+{gap:.1f}s',
        va='center',
        color='white',
        fontsize=10
    )

axes[1].set_title(
    "Strategy Comparison — Gap to Best (seconds)",
    color='white',
    fontsize=14
)
axes[1].set_xlabel("Gap to Best Strategy (seconds)", color='white')
axes[1].set_facecolor('black')
axes[1].tick_params(colors='white')
axes[1].grid(True, alpha=0.3, axis='x')
axes[1].invert_yaxis()
# invert so best strategy appears at top
for spine in axes[1].spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()
plt.savefig('race_strategy.png', dpi=150)
print("\nGraphs saved as race_strategy.png")

# ── OPTIMAL PIT LAP FINDER ─────────────────────────────────
# instead of testing fixed strategies like lap 20 or lap 25
# we test EVERY possible pit lap from lap 5 to lap 52
# and find which one gives the absolute best race time

print("\n--- Finding Optimal Pit Lap ---")
print("Testing every possible pit lap for S-M strategy...")

best_time_optimal  = float('inf')
# float('inf') = infinity
# any real time will be smaller than this
# so first result automatically becomes the best

best_pit_lap       = 0
all_pit_laps       = []
all_times          = []

for pit_lap in range(5, 53):
    # test every pit lap from lap 5 to lap 52
    # we don't pit on lap 1-4 (too early)
    # we don't pit after lap 52 (too late, not enough laps left)

    stint1_laps = pit_lap
    # first stint = from lap 1 to pit lap
    stint2_laps = TOTAL_LAPS - pit_lap
    # second stint = remaining laps after pit

    strategy = [
        ('Soft',   stint1_laps),
        ('Medium', stint2_laps)
    ]

    result = simulate_strategy(strategy)

    if result:
        total_time = result['total_time']
        all_pit_laps.append(pit_lap)
        all_times.append(total_time)

        # check if this is the best time found so far
        if total_time < best_time_optimal:
            best_time_optimal = total_time
            best_pit_lap      = pit_lap

# convert best time to mm:ss
best_minutes = int(best_time_optimal // 60)
best_seconds = best_time_optimal % 60

print(f"\nOptimal pit lap found: LAP {best_pit_lap}")
print(f"Optimal race time:     {best_minutes}:{best_seconds:05.2f}")
print(f"Strategies tested:     {len(all_pit_laps)}")

# ── PLOT OPTIMAL PIT LAP ───────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(15, 6))
fig3.patch.set_facecolor('black')

# plot race time for every pit lap tested
ax3.plot(
    all_pit_laps,
    all_times,
    color='cyan',
    linewidth=2,
    label='Race time by pit lap'
)

# highlight the optimal pit lap with a vertical line
ax3.axvline(
    x=best_pit_lap,
    color='gold',
    linestyle='--',
    linewidth=2,
    label=f'Optimal pit lap: {best_pit_lap}'
)

# add a dot on the optimal point
ax3.scatter(
    [best_pit_lap],
    [best_time_optimal],
    color='gold',
    s=100,
    zorder=5
    # zorder=5 makes dot appear on top of the line
)

# add text annotation showing the optimal time
ax3.annotate(
    f'Best: Lap {best_pit_lap}\n{best_minutes}:{best_seconds:05.2f}',
    xy=(best_pit_lap, best_time_optimal),
    xytext=(best_pit_lap + 3, best_time_optimal + 10),
    # position text slightly away from the dot
    color='gold',
    fontsize=11,
    arrowprops=dict(
        arrowstyle='->',
        color='gold'
    )
)

ax3.set_title(
    "Optimal Pit Lap Finder — Soft to Medium Strategy\n"
    "Every possible pit lap tested",
    color='white',
    fontsize=14
)
ax3.set_xlabel("Pit Lap", color='white')
ax3.set_ylabel("Total Race Time (seconds)", color='white')
ax3.set_facecolor('black')
ax3.tick_params(colors='white')
ax3.grid(True, alpha=0.3)
ax3.legend(
    facecolor='black',
    labelcolor='white',
    fontsize=11
)
for spine in ax3.spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()
plt.savefig('optimal_pit_lap.png', dpi=150)
print("Optimal pit lap graph saved as optimal_pit_lap.png")