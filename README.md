# Tic Tac Toe - Web Version with AI & Local Play

A modern, responsive Tic Tac Toe game built with **Python (Flask)** and **HTML/CSS/JS**. This project features:
- Single-player mode with **Easy, Medium, and Hard (Minimax)** AI
- 👥 Two-player (local) mode
- Stylish dark-mode UI with responsive design for **mobile/touch play**
- Play directly in your **browser** — works on phone and desktop

---

## Features

- 🧠 AI Difficulty Levels:
  - Easy
  - Medium
  - Hard
- Local multiplayer mode
- Beautiful, clean UI with dark theme
- Touch-friendly design for phones/tablets
- Built with Flask + vanilla JS frontend

---


## 🧠 AI Logic

The AI opponent offers three difficulty levels, powered by different logic layers:

| Difficulty | Strategy Description |
|------------|----------------------|
| Easy       | Picks a random available cell (no strategy) |
| Medium     | Checks for immediate win or blocks player's winning move |
| Hard       | Uses the **Minimax algorithm** to play optimally — impossible to beat |

> The AI logic is implemented in Python and interacts with the frontend through AJAX calls, making real-time decisions after each move.

---

## 🛠️ Tech Stack

### Backend:
- **Python**
- **Flask** (lightweight web framework for routing and server logic)

### Frontend:
- **HTML5** (structure)
- **CSS3** (custom dark theme with modern color palette)
- **JavaScript (Vanilla)** (DOM interaction and event handling)
- **AJAX** (asynchronous communication with Flask server)

### UI/UX:
- Responsive layout with CSS Grid
- **Dark Mode UI** with:
  - Light green for win highlights
  - Blue/orange for buttons
  - Red for reset
- Touch-friendly design (mobile optimized)
- Google Fonts (Nunito)

---

