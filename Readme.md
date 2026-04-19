# 🏎️ Motorsport Engineering Portfolio

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastF1](https://img.shields.io/badge/FastF1-3.x-red)](https://theoehrly.github.io/Fast-F1/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-orange)](https://streamlit.io)

A self-built motorsport engineering portfolio developed to 
transition from Software Engineering into Motorsport Engineering.
All projects built from scratch using real F1 data and physics.

---

## 👤 About Me

**Name:** Irfan Hussain  
Background: B.E Software Engineering  
Goal: MSc Motorsport Engineering  
Interests: Race data analysis, vehicle dynamics, strategy optimization

I built this portfolio independently to prove that a software 
engineering background is a genuine asset in modern motorsport — 
where data analysis, telemetry, and simulation are as important 
as mechanical engineering.

---

## 📁 Projects

### 🚗 Project 1 — Car Acceleration Simulator
> Physics-based vehicle simulation from scratch

**What it does:**
Simulates how any vehicle accelerates and brakes using 
real physics equations. Tested on 4 vehicles with real specs.

**Physics used:**
- Newton's Second Law (F = ma)
- Aerodynamic drag force
- Power to force conversion (F = P ÷ v)

**Results:**

| Vehicle        | Engine Power | Mass    | Top Speed   |
|----------------|-------------|---------|-------------|
| F1 Car         | 1000 hp     | 800 kg  | 344 km/h    |
| Toyota Corolla | 140 hp      | 1500 kg | 145 km/h    |
| Heavy Truck    | 400 hp      | 5000 kg | 123 km/h    |
| Bicycle        | 0.5 hp      | 80 kg   | 37 km/h     |

**Key insight:**
A 400hp truck is slower than a 140hp Corolla — proving that 
top speed depends on the balance between engine force, 
mass and aerodynamic drag — not engine power alone.

**Libraries:** NumPy, Matplotlib

---

### 📊 Project 2 — Real F1 Data Analysis
> Telemetry analysis using actual Formula 1 race data

**What it does:**
Loads real 2023 F1 qualifying telemetry using FastF1 and 
performs engineering-level analysis comparing two drivers.

**Analysis performed:**
- Speed trace comparison: Verstappen vs Hamilton
- Automatic braking zone detection (7 zones found)
- Throttle and brake trace analysis
- Lap time gap breakdown by sector

**Key findings:**

| Metric        | VER      | HAM      | Difference      |
|---------------|----------|----------|-----------------|
| Lap Time      | 1:29.708 | 1:30.332 | 0.624s VER      |
| Top Speed     | 323 km/h | 321 km/h | 2 km/h VER      |
| Full Throttle | 61.9%    | 59.3%    | 2.6% more VER   |
| Braking %     | 19.0%    | 19.0%    | identical       |
| Gear Changes  | 50       | 52       | 2 more HAM      |

**Engineering conclusion:**
Verstappen's entire 0.624s advantage came from spending 
2.6% more time at full throttle — confirming Red Bull's 
superior traction and corner exit performance in 2023.

**Libraries:** FastF1, Pandas, Matplotlib

---

### 📡 Project 3 — Live Telemetry Dashboard
> Interactive web dashboard built with Streamlit

**What it does:**
A professional web application that visualizes F1 telemetry 
data interactively — select any driver and compare their 
speed, throttle, brake and gear traces in real time.

**Features:**
- Driver selector dropdown
- Metric cards (lap time, top speed, avg speed, distance)
- Speed trace on professional black background
- Throttle and brake visualization
- Color coded gear trace
- Two driver comparison with gap indicator
- Full lap summary statistics

**To run locally:**
pip install streamlit fastf1 matplotlib pandas
streamlit run dashboard.py

**Libraries:** Streamlit, FastF1, Matplotlib, Pandas

---

### 🏁 Project 4 — Race Strategy Simulator
> Pit stop optimization tool for Formula 1

**What it does:**
Simulates every possible pit stop strategy for a Grand Prix 
and finds the mathematically optimal pit lap using 
a tire degradation model.

**Strategy results — Bahrain GP simulation:**

| Strategy      | Total Time | Gap    | Pit Stops |
|---------------|------------|--------|-----------|
| M-S (lap 30)  | 91:37.60   | +0.0s  | 1         |
| S-M (lap 25)  | 91:38.88   | +1.3s  | 1         |
| S-M-S (20,20) | 91:41.00   | +3.4s  | 2         |
| S-M (lap 20)  | 91:43.48   | +5.9s  | 1         |

**Optimal pit lap finder:**
- Tested all 48 possible pit laps automatically
- Optimal pit lap: **Lap 34**
- Optimal race time: **91:35.64**

**Physics used:**
Lap time = base time + (degradation rate × tire age)
Pit loss = 22 seconds per stop

**Libraries:** NumPy, Matplotlib, Pandas

---

## 🛠️ Skills Demonstrated
Vehicle Physics        → drag, force, acceleration, power
Data Analysis          → real F1 telemetry, Pandas, visualization
Software Development   → Python, Streamlit web app, Git
Engineering Thinking   → optimization, pattern recognition
Motorsport Knowledge   → tire strategy, telemetry, braking zones

---

## 🎯 Target Universities

- Oxford Brookes University — MSc Motorsport Engineering
- Cranfield University — MSc Automotive Engineering
- University of Birmingham — MSc Mechanical Engineering
- University of Leeds — MSc Automotive Engineering

---

## 📚 What I Learned

Building this portfolio taught me that modern motorsport 
engineering is not just about mechanical knowledge — it is 
about understanding data. Every tenth of a second on a 
lap time can be explained by numbers. Every strategic 
decision in a race can be optimized by simulation.

My software engineering background gives me a unique 
advantage in this field — I can build the tools that 
extract these insights, not just use them.

---

## 📬 Contact

- **GitHub:** github.com/ihussain92
- **Email:** your email here

---

*Built independently as part of MSc Motorsport Engineering 
application preparation — 2024*
