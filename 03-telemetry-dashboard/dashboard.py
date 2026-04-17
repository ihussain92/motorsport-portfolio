import streamlit as st
import fastf1
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# ── PAGE SETTINGS ──────────────────────────────────────────
st.set_page_config(
    page_title="F1 Telemetry Dashboard",
    page_icon="🏎️",
    layout="wide"
    # wide layout uses full browser width   
    # looks much more professional
)

# ── CACHE SETUP ────────────────────────────────────────────
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

# ── TITLE ──────────────────────────────────────────────────
st.title("🏎️ F1 Telemetry Dashboard")
st.markdown("**2023 Bahrain Grand Prix — Qualifying**")
# st.markdown allows basic formatting like bold

# ── LOAD SESSION ───────────────────────────────────────────
# @st.cache_data tells Streamlit to save this data in memory
# so it doesn't re-download every time you change something
@st.cache_data
def load_session():
    session = fastf1.get_session(2023, 'Bahrain', 'Q')
    session.load()
    return session

# show a loading spinner while data downloads
with st.spinner("Loading session data..."):
    session = load_session()

st.success("Session loaded successfully.")

# ── GET ALL DRIVERS IN SESSION ─────────────────────────────
drivers = session.laps['Driver'].unique().tolist()
# gets list of all driver codes in this session
# like ['VER', 'HAM', 'LEC', 'SAI', 'PER' ...]
drivers.sort()
# sort alphabetically so dropdown looks clean

# ── SIDEBAR ────────────────────────────────────────────────
# sidebar is the panel on the left side of the app
st.sidebar.title("Settings")
st.sidebar.markdown("Select driver and lap to analyze")

selected_driver = st.sidebar.selectbox(
    "Select Driver",
    drivers,
    index=drivers.index('VER')
    # start with Verstappen selected by default
)

# ── LAP SELECTOR ───────────────────────────────────────────
lap_choice = st.sidebar.radio(
    "Select Lap",
    ["Fastest Lap", "All Laps"]
    # radio button = user picks one option
)

st.sidebar.markdown("---")
# adds a divider line in sidebar

st.sidebar.markdown(f"**Selected:** {selected_driver}")
st.sidebar.markdown(f"**Lap:** {lap_choice}")

# ── LOAD SELECTED DRIVER TELEMETRY ─────────────────────────
# ── LOAD SELECTED DRIVER TELEMETRY ─────────────────────────
@st.cache_data
def get_driver_telemetry(driver_code, _session):
    # _session has underscore prefix
    # this tells Streamlit not to cache the session object
    # but still allows us to pass it in
    lap = _session.laps.pick_drivers(driver_code).pick_fastest()
    telemetry = lap.get_telemetry()
    return lap, telemetry

# show spinner while loading
with st.spinner(f"Loading {selected_driver} telemetry..."):
    lap, telemetry = get_driver_telemetry(selected_driver, session)
    # now we pass session as argument instead of using it directly
    

# ── METRIC CARDS ───────────────────────────────────────────
# these are the big number displays at the top of the dashboard
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
# creates 4 equal columns side by side

with col1:
    st.metric(
        label="Lap Time",
        value=str(lap['LapTime'])[7:15]
        # slice the string to show only mm:ss.fff
    )

with col2:
    st.metric(
        label="Top Speed",
        value=f"{telemetry['Speed'].max():.0f} km/h"
        # .max() finds highest speed in the lap
    )

with col3:
    st.metric(
        label="Avg Speed",
        value=f"{telemetry['Speed'].mean():.0f} km/h"
        # .mean() calculates average speed
    )

with col4:
    st.metric(
        label="Lap Distance",
        value=f"{telemetry['Distance'].max():.0f} m"
        # total lap distance in meters
    )

# ── GRAPHS ─────────────────────────────────────────────────
st.markdown("---")
st.subheader(f"{selected_driver} — Fastest Lap Telemetry")

# create 3 graphs stacked vertically
fig, axes = plt.subplots(3, 1, figsize=(15, 10))
fig.patch.set_facecolor('black')
# black background looks very professional
# like real F1 engineering software

# ── GRAPH 1: SPEED ─────────────────────────────────────────
axes[0].plot(
    telemetry['Distance'],
    telemetry['Speed'],
    color='cyan',
    linewidth=2
)
axes[0].set_ylabel("Speed (km/h)", color='white')
axes[0].set_facecolor('black')
axes[0].tick_params(colors='white')
axes[0].grid(True, alpha=0.3)
# alpha=0.3 makes grid lines subtle not distracting
for spine in axes[0].spines.values():
    spine.set_edgecolor('white')

# ── GRAPH 2: THROTTLE ──────────────────────────────────────
axes[1].plot(
    telemetry['Distance'],
    telemetry['Throttle'],
    color='lime',
    linewidth=2
)
axes[1].set_ylabel("Throttle (%)", color='white')
axes[1].set_facecolor('black')
axes[1].tick_params(colors='white')
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(0, 110)
# set y axis limit so 100% throttle doesn't touch top of graph
for spine in axes[1].spines.values():
    spine.set_edgecolor('white')

# ── GRAPH 3: BRAKE ─────────────────────────────────────────
axes[2].fill_between(
    telemetry['Distance'],
    telemetry['Brake'].astype(int),
    # fill_between fills area under the line
    # looks much better than a simple line for brake data
    color='red',
    alpha=0.7
)
axes[2].set_ylabel("Brake", color='white')
axes[2].set_xlabel("Distance (meters)", color='white')
axes[2].set_facecolor('black')
axes[2].tick_params(colors='white')
axes[2].grid(True, alpha=0.3)
axes[2].set_ylim(0, 1.2)
# 1 = braking, 0 = not braking
for spine in axes[2].spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()

# ── DISPLAY IN STREAMLIT ───────────────────────────────────
st.pyplot(fig)
# st.pyplot displays matplotlib figure directly in browser
# no need to save as PNG anymore

plt.close()
# close figure after displaying
# prevents memory buildup if user switches drivers

# ── DRIVER COMPARISON ──────────────────────────────────────
st.markdown("---")
st.subheader("Driver Comparison")

# let user pick a second driver to compare
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Driver 1:** {selected_driver}")

with col2:
    # remove selected driver from list so user cant compare
    # a driver against themselves
    other_drivers = [d for d in drivers if d != selected_driver]

    compare_driver = st.selectbox(
        "Select Driver to Compare",
        other_drivers,
        index=other_drivers.index('HAM')
        if 'HAM' in other_drivers else 0
        # default to Hamilton if available
    )

# ── LOAD COMPARISON DRIVER TELEMETRY ───────────────────────
with st.spinner(f"Loading {compare_driver} telemetry..."):
    lap2, telemetry2 = get_driver_telemetry(compare_driver, session)

# ── COMPARISON METRIC CARDS ────────────────────────────────
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

lap1_time = lap['LapTime'].total_seconds()
lap2_time = lap2['LapTime'].total_seconds()
# convert lap time to seconds for easy comparison
diff = lap1_time - lap2_time
# negative = selected driver is faster
# positive = compare driver is faster

with col1:
    st.metric(
        label=f"{selected_driver} Lap Time",
        value=str(lap['LapTime'])[7:15]
    )

with col2:
    st.metric(
        label=f"{compare_driver} Lap Time",
        value=str(lap2['LapTime'])[7:15]
    )

with col3:
    st.metric(
        label="Gap",
        value=f"{abs(diff):.3f}s",
        delta=f"{selected_driver} faster" if diff < 0 else f"{compare_driver} faster",
        delta_color="normal"
    )

with col4:
    top_speed_diff = telemetry['Speed'].max() - telemetry2['Speed'].max()
    st.metric(
        label="Top Speed Diff",
        value=f"{abs(top_speed_diff):.0f} km/h",
        delta=f"{selected_driver} faster" if top_speed_diff > 0 else f"{compare_driver} faster"
    )

# ── COMPARISON SPEED TRACE ─────────────────────────────────
st.markdown("---")
st.subheader(f"{selected_driver} vs {compare_driver} — Speed Trace")

fig2, ax = plt.subplots(figsize=(15, 5))
fig2.patch.set_facecolor('black')

ax.plot(
    telemetry['Distance'],
    telemetry['Speed'],
    color='cyan',
    linewidth=2,
    label=selected_driver
)
ax.plot(
    telemetry2['Distance'],
    telemetry2['Speed'],
    color='orange',
    linewidth=2,
    linestyle='--',
    label=compare_driver
)

ax.set_ylabel("Speed (km/h)", color='white')
ax.set_xlabel("Distance (meters)", color='white')
ax.set_facecolor('black')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.3)
ax.legend(
    facecolor='black',
    labelcolor='white',
    fontsize=12
)
for spine in ax.spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()
st.pyplot(fig2)
plt.close()

# ── GEAR TRACE ─────────────────────────────────────────────
st.markdown("---")
st.subheader(f"{selected_driver} — Gear Changes")

fig3, ax3 = plt.subplots(figsize=(15, 4))
fig3.patch.set_facecolor('black')

# create a colorful gear trace
# each gear gets its own color so changes are very visible
gear_colors = {
    1: 'red',
    2: 'orange',
    3: 'yellow',
    4: 'lime',
    5: 'cyan',
    6: 'blue',
    7: 'purple',
    8: 'white'
}

# plot each gear segment separately with its own color
for gear in telemetry['nGear'].unique():
    # filter data to only this gear
    gear_data = telemetry[telemetry['nGear'] == gear]
    ax3.scatter(
        gear_data['Distance'],
        gear_data['nGear'],
        color=gear_colors.get(gear, 'white'),
        s=2,
        # s = size of each dot, small so they form a line
        label=f"Gear {gear}"
    )

ax3.set_ylabel("Gear", color='white')
ax3.set_xlabel("Distance (meters)", color='white')
ax3.set_facecolor('black')
ax3.tick_params(colors='white')
ax3.grid(True, alpha=0.3)
ax3.set_yticks(range(1, 9))
# show gear numbers 1 to 8 on y axis
ax3.legend(
    facecolor='black',
    labelcolor='white',
    fontsize=8,
    ncol=8,
    # show all gear labels in one row
    loc='upper left'
)
for spine in ax3.spines.values():
    spine.set_edgecolor('white')

plt.tight_layout()
st.pyplot(fig3)
plt.close()

# ── SUMMARY SECTION ────────────────────────────────────────
st.markdown("---")
st.subheader("Lap Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {selected_driver}")

    # calculate statistics
    full_throttle_pct = (
        (telemetry['Throttle'] > 98).sum() / len(telemetry) * 100
    )
    # percentage of lap spent at full throttle (above 98%)

    braking_pct = (
        telemetry['Brake'].astype(int).sum() / len(telemetry) * 100
    )
    # percentage of lap spent braking

    max_gear = telemetry['nGear'].max()
    # highest gear reached

    gear_changes = (telemetry['nGear'].diff() != 0).sum()
    # count how many times gear changed

    st.markdown(f"- **Lap time:** {str(lap['LapTime'])[7:15]}")
    st.markdown(f"- **Top speed:** {telemetry['Speed'].max():.0f} km/h")
    st.markdown(f"- **Full throttle:** {full_throttle_pct:.1f}% of lap")
    st.markdown(f"- **Braking:** {braking_pct:.1f}% of lap")
    st.markdown(f"- **Highest gear:** {max_gear}")
    st.markdown(f"- **Gear changes:** {gear_changes}")

with col2:
    st.markdown(f"### {compare_driver}")

    full_throttle_pct2 = (
        (telemetry2['Throttle'] > 98).sum() / len(telemetry2) * 100
    )
    braking_pct2 = (
        telemetry2['Brake'].astype(int).sum() / len(telemetry2) * 100
    )
    max_gear2    = telemetry2['nGear'].max()
    gear_changes2 = (telemetry2['nGear'].diff() != 0).sum()

    st.markdown(f"- **Lap time:** {str(lap2['LapTime'])[7:15]}")
    st.markdown(f"- **Top speed:** {telemetry2['Speed'].max():.0f} km/h")
    st.markdown(f"- **Full throttle:** {full_throttle_pct2:.1f}% of lap")
    st.markdown(f"- **Braking:** {braking_pct2:.1f}% of lap")
    st.markdown(f"- **Highest gear:** {max_gear2}")
    st.markdown(f"- **Gear changes:** {gear_changes2}")

# ── FOOTER ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with FastF1 and Streamlit · "
    "Data: Formula 1 2023 · "
    "Project 3 of Motorsport Engineering Portfolio"
)