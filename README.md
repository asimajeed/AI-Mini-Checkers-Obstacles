# Mini‑Checkers with Obstacles

A 6×6 checkers variant featuring dynamic **obstacle** squares that block movement and captures. Challenge a Minimax + alpha–beta pruning AI in a shifting, strategic environment.

## Demonstration by Ayan Hasan

<video width="1280" height="720" controls>
  <source src="AI Project Demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

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
   git clone https://github.com/your-org/mini_checkers_obstacles.git
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

## 🎮 Usage

**Play vs. AI**

```bash
python run_game.py [--ai-depth N] [--obstacles M] [--width W] [--height H]
```

- `--ai-depth` AI search depth in plies (default: `4`)
- `--obstacles` Initial obstacle count (default: `2`)
- `--width` / `--height` Window dimensions in pixels (default: `600×600`)

---

## 📂 Project Structure

```
mini_checkers_obstacles/
├── README.md
├── requirements.txt
├── run_game.py
└── src/
    └── checkers/
        ├── board.py           # Board model + dynamic obstacle logic
        ├── piece.py           # Piece and promotion logic
        ├── move_generator.py  # Move & capture generation with obstacles
        ├── ai/
        │   ├── minimax.py     # Minimax + alpha–beta pruning
        │   └── heuristic.py   # Evaluation function (material, mobility, etc.)
        └── ui/
            ├── gui.py         # Pygame event loop & input handling
            └── renderer.py    # Board, pieces & highlight rendering
```

---

## 👥 Collaborators

- [Saiyed Asim Majeed](https://github.com/asimajeed)
- [Muhammad Muzammil](https://github.com/MuhammadMuzammil21)
- [Ayan Hasan](https://github.com/ayanh786)
