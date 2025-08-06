let currentBoard = [];
let gameOver = false;

function startNewGame() {
    const mode = document.getElementById('mode').value;
    const difficulty = document.getElementById('difficulty').value;

    fetch('/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode, difficulty })
    })
    .then(res => res.json())
    .then(() => {
        gameOver = false;
        document.getElementById('status').textContent = '';
        document.getElementById('reset-btn').style.display = 'none';
        drawBoard();
    });
}

function drawBoard() {
    const boardDiv = document.getElementById('game-board');
    boardDiv.innerHTML = '';

    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.addEventListener('click', handleClick);
            boardDiv.appendChild(cell);
        }
    }
}

function handleClick(e) {
    if (gameOver) return;

    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);

    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'occupied') {
            alert('Cell already taken!');
            return;
        }

        updateBoard(data.board);

        if (data.win && data.win.length > 0) {
            document.getElementById('status').textContent = `${data.current} wins!`;
            highlightWinningCells(data.win);
            gameOver = true;
        } else if (data.draw) {
            document.getElementById('status').textContent = "It's a draw!";
            gameOver = true;
        }

        if (data.ai_move && !gameOver) {
            // Highlight AI move
            setTimeout(() => {
                updateBoard(data.board);
                if (data.win && data.win.length > 0) {
                    document.getElementById('status').textContent = `O wins!`;
                    highlightWinningCells(data.win);
                    gameOver = true;
                } else if (data.draw) {
                    document.getElementById('status').textContent = "It's a draw!";
                    gameOver = true;
                }
            }, 300);
        }

        if (gameOver) {
            document.getElementById('reset-btn').style.display = 'inline-block';
        }
    });
}

function updateBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        const val = board[row][col];
        cell.textContent = val === '.' ? '' : val;
    });
}

function highlightWinningCells(cells) {
    cells.forEach(([row, col]) => {
        const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
        if (cell) {
            cell.classList.add('win');
        }
    });
}
