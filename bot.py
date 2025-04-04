import sys
import chess
import chess.svg
import numpy as np
import pandas as pd
import stockfish
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtSvg import QSvgWidget

# Load dataset
df = pd.read_excel("optimized_chess_fen_responses.xlsx")

# Create a move mapping to avoid hashing issues
unique_moves = list(df["Response Move"].unique())
move_to_index = {move: idx for idx, move in enumerate(unique_moves)}
index_to_move = {idx: move for move, idx in move_to_index.items()}

def extract_features(fen):
    board = chess.Board(fen)
    features = [len(board.pieces(piece, chess.WHITE)) for piece in chess.PIECE_TYPES] + \
               [len(board.pieces(piece, chess.BLACK)) for piece in chess.PIECE_TYPES]
    return np.array(features)

# Prepare data
X = np.array([extract_features(fen) for fen in df["FEN"]])
y = np.array([move_to_index[move] for move in df["Response Move"]])

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Initialize Stockfish
stockfish_engine = stockfish.Stockfish("stockfish-windows-x86-64-avx2.exe")
stockfish_engine.set_skill_level(10)

class ChessBot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chess Bot")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()
        self.status_label = QLabel("Your Move:")
        layout.addWidget(self.status_label)

        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(400, 400)
        layout.addWidget(self.svg_widget)

        self.move_input = QLineEdit(self)
        self.move_input.setPlaceholderText("Enter your move (e.g., e2e4)")
        layout.addWidget(self.move_input)

        self.move_button = QPushButton("Make Move")
        self.move_button.clicked.connect(self.player_move)
        layout.addWidget(self.move_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.update_board()

    def update_board(self):
        svg_data = chess.svg.board(self.board).encode("UTF-8")
        self.svg_widget.load(svg_data)

    def player_move(self):
        move = self.move_input.text().strip()
        if move in [str(m) for m in self.board.legal_moves]:
            self.board.push_uci(move)
            self.update_board()
            self.move_input.clear()

            if self.board.is_game_over():
                self.status_label.setText("Game Over! " + self.board.result())
                return

            self.bot_move()
        else:
            self.status_label.setText("Invalid move. Try again.")

    def bot_move(self):
        features = extract_features(self.board.fen()).reshape(1, -1)
        predicted_index = int(model.predict(features)[0])
        predicted_move = index_to_move.get(predicted_index, None)

        if predicted_move and predicted_move in [str(m) for m in self.board.legal_moves]:
            best_move = chess.Move.from_uci(predicted_move)
        else:
            stockfish_engine.set_fen_position(self.board.fen())
            best_move = chess.Move.from_uci(stockfish_engine.get_best_move())

        self.board.push(best_move)
        self.update_board()

        if self.board.is_game_over():
            self.status_label.setText("Game Over! " + self.board.result())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chess_bot = ChessBot()
    chess_bot.show()
    sys.exit(app.exec_())
