# Mini‑Checkers with Obstacles

A 6×6 checkers variant featuring dynamic **obstacle** squares that block movement and captures. Challenge a Minimax + alpha–beta pruning AI in a shifting, strategic environment.

---

## 🔎 Features

- **6×6 Dark‑Square Board**
- **Random Obstacles**  
  - Cannot be entered or jumped over  
  - Can be re-randomized mid‑game to create evolving choke points
- **Human vs. AI**  
  - AI (Player 2) uses Minimax with alpha–beta pruning  
  - Obstacle-aware heuristic balances material, mobility, and path clarity
- **Optional Reinforcement Learning**  
  - Self-play agent for tuning heuristic weights
- **Pygame GUI**  
  - Click to move pieces, with highlighted legal moves
- **Console Mode**  
  - Play directly from the command line (GUI optional)

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/asimajeed/mini_checkers_obstacles.git
   cd mini_checkers_obstacles
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 👥 Collaborators

- Saiyed Asim Majeed  
- Muhammad Muzammil  
- Ayan Hasan