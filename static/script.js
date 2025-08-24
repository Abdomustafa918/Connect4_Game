const rows = 6;
const cols = 7;
let board = Array.from({ length: rows }, () => Array(cols).fill(0));
let gameOver = false;

function createBoard() {
    const gameBoard = document.getElementById("gameBoard");
    gameBoard.innerHTML = "";
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement("div");
            cell.className = "cell empty";
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener("click", () => makeMove(c));
            gameBoard.appendChild(cell);
        }
    }
}

function makeMove(col) {
    if (gameOver) return;
    
    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board, column: col })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("status").textContent = data.error;
            return;
        }
        
        board = data.board;
        updateBoard();
        
        if (data.winner) {
            let winMessage = "";
            if (data.winner === 'Player') {
                winMessage = `🎉 Player wins! 🎉`; 
            } else {
                winMessage = `🤖 AI wins! 💻`; 
            }
            document.getElementById("status").textContent = winMessage;
            gameOver = true;
        }
    })
    .catch(error => console.error("Error:", error));
}

function updateBoard() {
    const cells = document.querySelectorAll(".cell");
    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);
        
        cell.className = "cell";
        if (board[r][c] === 1) {
            cell.classList.add("player");
        } else if (board[r][c] === 2) {
            cell.classList.add("ai");
        } else {
            cell.classList.add("empty");
            if (gameOver) {
                cell.style.pointerEvents = "none";
            } else {
                cell.style.pointerEvents = "auto";
            }
        }
    });
}

function restartGame() {
    board = Array.from({ length: rows }, () => Array(cols).fill(0));
    document.getElementById("status").textContent = "";
    gameOver = false;
    createBoard();
}

document.addEventListener("DOMContentLoaded", createBoard);