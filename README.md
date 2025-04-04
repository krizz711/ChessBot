♟️ Personal Chess Bot — Trained on My Own Games
I was inspired by the idea of chess bots that mimic the styles of famous players on Chess.com. After seeing how unique and personalized those bots are, I decided to create my own chess bot that plays like me.

🧠 Inspiration & Idea
While exploring Chess.com bots based on grandmasters and streamers, I wondered:

"What if I could train a bot to play like myself?"

So I exported my own games from Chess.com using Linktree, and began working on a bot that learns my move patterns and decision-making.

🔨 What I Did

✅ Data Collection: Downloaded my personal gameplay data from Chess.com using linkedtree

✅ Data Processing: Converted each game into FEN positions (board state) and corresponding best move responses

✅ Model Training: Used Random Forest Regression to predict my moves based on board positions

✅ Enhancement: Integrated Stockfish as a helper to improve move quality where predictions are uncertain

✅ Interface: Built a playable chess game GUI using Qt, where you can play against the trained bot

🚀 Features

Mimics your personal playstyle

Learns from real game data

Hybrid decision-making: combines ML predictions with Stockfish

Graphical interface for playing directly against your own AI

🧰 Tech Stack

Language: Python

ML Model: Random Forest Regression (via Scikit-learn)

Chess Engine: Stockfish

Data Format: PGN → FEN

GUI: PyQt5 / Qt for Python

### ♟️ Stockfish Setup

This project uses [Stockfish](https://stockfishchess.org/download/) to assist with move evaluation.

🔧 **How to set it up:**

1. Download the Stockfish binary for your OS from the [official site](https://stockfishchess.org/download/).
2. Place the `stockfish` executable inside the project folder.
3. Make sure your Python script points to the correct file path:
   ```python
   engine = chess.engine.SimpleEngine.popen_uci("stockfish")

📁 Coming Soon

Adjustable difficulty using model confidence

Side-by-side comparison with Stockfish-only bot
