# CMSE 202 Final Project: Forest Fire and Tornado Evacuation Simulation

## 🔥 Abstract

This project simulates real-time evacuation during two different natural hazards — a **forest fire** and a **tornado** — in a grid-based town environment. The simulation models the spread of hazards, the reaction of EMS (emergency responders), and evacuation outcomes using emoji-based visualization. Each simulation tracks:
- Hazard spread
- Rescue paths
- Collisions with EMS or houses
- Rescue times
- Destruction logs

We use **NumPy** and **matplotlib** for simulation and visualization. The results help analyze evacuation success and timing under dynamic disaster scenarios.

## 🧪 Files

| File | Purpose |
|------|---------|
| `fire_sim.py` | Simulates fire spread and rescue |
| `tornado_sim.py` | Simulates tornado movement and house destruction |
| `common_plot.py` | Shared emoji grid plotter |
| `README.md` | This file |
| `slides/final_presentation.pdf` | Final project presentation slides |

## ▶️ How to Run

Run from terminal:
```bash
python fire_sim.py
python tornado_sim.py

## 📈 Results

- ✅ Total houses rescued: *X*
- ❌ Total houses destroyed: *Y*
- ⏱️ Average rescue time: *Z minutes*
- 💥 Hazards involved: Fire, Tornado
- 🔁 Rescue collisions handled dynamically

