# Chess AI Project

A desktop Chess application featuring a custom graphical user interface and an AI opponent driven by the Minimax algorithm. 

Built as a final high school senior year coding project.

---

## Features

* **Interactive Graphical UI:** Inspired by Chess.com's visual layout and board design.
* **AI Opponent:** Play against an automated player powered by the Minimax decision-making algorithm.
* **Chess Logic Engine:** Complete board state management, legal move generation, and game-over detection (checkmate, stalemate).

---

## How It Works

### Minimax Algorithm
The AI evaluates potential future moves by building a decision tree up to a set search depth:
1. **Maximizing vs. Minimizing:** The AI simulates possible moves for both itself (maximizing board advantage) and the player (minimizing the AI's advantage).
2. **Evaluation Function:** Assigns a score to board states based on piece values and positional positioning to select the optimal move.

---

## Getting Started

### Prerequisites
* Python 3.8+
* [Pygame](https://www.pygame.org/) library

### Installation & Running

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AriLer/chess-ai-project.git](https://github.com/AriLer/chess-ai-project.git)
   cd chess-ai-project
