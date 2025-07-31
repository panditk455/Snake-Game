// Socket.IO connection
const socket = io();

// Game variables
let game = null;
let gameTimer = null;
let startTime = null;
let playerName = '';

// Socket event handlers
socket.on('connect', () => {
    updateConnectionStatus('Connected', true);
});

socket.on('disconnect', () => {
    updateConnectionStatus('Disconnected', false);
});

socket.on('game_started', (data) => {
    console.log('Game started:', data);
});

socket.on('game_ended', (data) => {
    console.log('Game ended:', data);
    showGameOver(data.final_score, data.game_duration);
});

// Game classes (Snake, Food, Game) - Enhanced versions
class Snake {
    constructor(length = 2) {
        this.length = length;
        this.segments = [];
        this.movements = { x: [0], y: [0] };
        this.segmentSize = 40;
        this.initializeSnake();
    }

    initializeSnake() {
        this.segments = [];
        const startX = this.segmentSize;
        const startY = this.segmentSize;
        
        for (let i = 0; i < this.length; i++) {
            this.segments.push({
                x: startX,
                y: startY + (i * this.segmentSize)
            });
        }
    }

    draw(ctx) {
        this.segments.forEach((segment, index) => {
            // Enhanced drawing with gradients
            const gradient = ctx.createLinearGradient(
                segment.x, segment.y, 
                segment.x + this.segmentSize, segment.y + this.segmentSize
            );
            
            if (index === 0) {
                gradient.addColorStop(0, '#4169E1');
                gradient.addColorStop(1, '#1E90FF');
            } else {
                gradient.addColorStop(0, '#1E90FF');
                gradient.addColorStop(1, '#4682B4');
            }
            
            ctx.fillStyle = gradient;
            ctx.fillRect(segment.x, segment.y, this.segmentSize, this.segmentSize);
            
            // Border
            ctx.strokeStyle = '#000080';
            ctx.lineWidth = 2;
            ctx.strokeRect(segment.x, segment.y, this.segmentSize, this.segmentSize);
            
            // Eyes for head
            if (index === 0) {
                ctx.fillStyle = 'white';
                ctx.fillRect(segment.x + 8, segment.y + 8, 8, 8);
                ctx.fillRect(segment.x + 24, segment.y + 8, 8, 8);
                ctx.fillStyle = 'black';
                ctx.fillRect(segment.x + 10, segment.y + 10, 4, 4);
                ctx.fillRect(segment.x + 26, segment.y + 10, 4, 4);
            }
        });
    }

    move(direction) {
        let xMovement = 0;
        let yMovement = 0;

        switch (direction) {
            case 'Up':
            case 'w':
                if (this.movements.y[0] !== this.segmentSize) {
                    yMovement = -this.segmentSize;
                }
                break;
            case 'Down':
            case 's':
                if (this.movements.y[0] !== -this.segmentSize) {
                    yMovement = this.segmentSize;
                }
                break;
            case 'Left':
            case 'a':
                if (this.movements.x[0] !== this.segmentSize) {
                    xMovement = -this.segmentSize;
                }
                break;
            case 'Right':
            case 'd':
                if (this.movements.x[0] !== -this.segmentSize) {
                    xMovement = this.segmentSize;
                }
                break;
        }

        if (xMovement !== 0 || yMovement !== 0) {
            this.segments[0].x += xMovement;
            this.segments[0].y += yMovement;

            this.movements.x.unshift(xMovement);
            this.movements.y.unshift(yMovement);

            if (this.movements.x.length > this.length) {
                this.movements.x.pop();
                this.movements.y.pop();
            }

            for (let i = 1; i < this.segments.length; i++) {
                if (this.movements.x[i] !== undefined) {
                    this.segments[i].x += this.movements.x[i - 1];
                    this.segments[i].y += this.movements.y[i - 1];
                }
            }
        }
    }

    increaseLength() {
        this.length++;
        const lastSegment = this.segments[this.segments.length - 1];
        this.segments.push({
            x: lastSegment.x,
            y: lastSegment.y
        });
    }

    checkSelfCollision() {
        const head = this.segments[0];
        for (let i = 3; i < this.segments.length; i++) {
            if (head.x === this.segments[i].x && head.y === this.segments[i].y) {
                return true;
            }
        }
        return false;
    }

    checkWallCollision() {
        const head = this.segments[0];
        return head.x < 0 || head.x >= 600 || head.y < 0 || head.y >= 600;
    }

    getHead() { return this.segments[0]; }
    getLastSegmentX() { return this.segments[this.segments.length - 1].x; }
}

class Food {
    constructor() {
        this.position = { x: 0, y: 0 };
        this.size = 15;
    }

    generate(tailX, snakeLength) {
        let x, y;
        
        if (snakeLength % 10 >= 1 && snakeLength % 10 <= 4 && snakeLength > 4) {
            const corners = [
                { x: 5, y: 5 }, { x: 5, y: 575 },
                { x: 575, y: 575 }, { x: 575, y: 5 }
            ];
            const corner = corners[Math.floor(Math.random() * corners.length)];
            x = corner.x;
            y = corner.y;
        } else {
            x = Math.max(5, Math.min(575, tailX + 5));
            y = Math.max(5, Math.min(575, tailX + 5));
        }

        this.position = { x, y };
    }

    draw(ctx) {
        // Enhanced food with glow effect
        ctx.shadowColor = '#ff4444';
        ctx.shadowBlur = 10;
        ctx.fillStyle = '#ff4444';
        ctx.fillRect(this.position.x, this.position.y, this.size, this.size);
        
        ctx.shadowBlur = 0;
        ctx.strokeStyle = '#cc0000';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.position.x, this.position.y, this.size, this.size);
        
        ctx.fillStyle = '#ff8888';
        ctx.fillRect(this.position.x + 2, this.position.y + 2, 6, 6);
    }

    checkCollision(snake) {
        const head = snake.getHead();
        return head.x < this.position.x + this.size &&
               head.x + 40 > this.position.x &&
               head.y < this.position.y + this.size &&
               head.y + 40 > this.position.y;
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.snake = new Snake(2);
        this.food = new Food();
        this.score = 0;
        this.gameRunning = true;
        this.isPaused = false;
        this.direction = 'Down';
        this.gameSpeed = 150;
        
        this.setupEventListeners();
        this.generateFood();
        this.gameLoop();
        
        // Notify server about game start
        socket.emit('start_game', { player_name: playerName });
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            const key = e.key;
            
            if (key === ' ') {
                e.preventDefault();
                this.togglePause();
                return;
            }

            const validKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'w', 'a', 's', 'd'];
            
            if (validKeys.includes(key)) {
                e.preventDefault();
                
                if (this.isPaused) {
                    this.isPaused = false;
                    document.getElementById('pauseScreen').style.display = 'none';
                }
                
                let direction;
                switch (key) {
                    case 'ArrowUp': case 'w': direction = 'Up'; break;
                    case 'ArrowDown': case 's': direction = 'Down'; break;
                    case 'ArrowLeft': case 'a': direction = 'Left'; break;
                    case 'ArrowRight': case 'd': direction = 'Right'; break;
                }
                
                if (direction) this.direction = direction;
            } else {
                if (!this.isPaused && this.gameRunning) {
                    this.isPaused = true;
                    document.getElementById('pauseScreen').style.display = 'block';
                }
            }
        });
    }

    togglePause() {
        if (!this.gameRunning) return;
        this.isPaused = !this.isPaused;
        document.getElementById('pauseScreen').style.display = this.isPaused ? 'block' : 'none';
    }

    generateFood() {
        this.food.generate(this.snake.getLastSegmentX(), this.score);
    }

    update() {
        if (this.isPaused || !this.gameRunning) return;

        this.snake.move(this.direction);

        if (this.food.checkCollision(this.snake)) {
            this.snake.increaseLength();
            this.score++;
            this.updateScore();
            this.generateFood();
            
            // Notify server about score update
            socket.emit('update_score', { score: this.score });
            
            if (this.score === 15) {
                this.gameSpeed = 50;
            }
        }

        if (this.snake.checkWallCollision() || this.snake.checkSelfCollision()) {
            this.gameOver();
        }
    }

    draw() {
        // Enhanced background with grid
        const gradient = this.ctx.createLinearGradient(0, 0, 600, 600);
        gradient.addColorStop(0, '#2d5a2d');
        gradient.addColorStop(1, '#1a4a1a');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, 600, 600);

        // Grid
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        for (let i = 0; i <= 600; i += 40) {
            this.ctx.beginPath();
            this.ctx.moveTo(i, 0);
            this.ctx.lineTo(i, 600);
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.moveTo(0, i);
            this.ctx.lineTo(600, i);
            this.ctx.stroke();
        }

        this.snake.draw(this.ctx);
        this.food.draw(this.ctx);
    }

    updateScore() {
        document.getElementById('score').textContent = this.score;
    }

    gameOver() {
        this.gameRunning = false;
        const gameTime = Math.floor((Date.now() - startTime) / 1000);
        
        // Notify server about game over
        socket.emit('game_over', { score: this.score, game_time: gameTime });
        
        clearInterval(gameTimer);
        showGameOver(this.score, gameTime);
    }

    gameLoop() {
        this.update();
        this.draw();

        if (this.gameRunning) {
            setTimeout(() => this.gameLoop(), this.gameSpeed);
        }
    }
}

// Game control functions
function startNewGame() {
    playerName = document.getElementById('playerName').value || 'Anonymous';
    
    // Hide any open modals
    document.getElementById('gameOver').style.display = 'none';
    document.getElementById('pauseScreen').style.display = 'none';
    document.getElementById('highScoresModal').style.display = 'none';
    
    // Reset score and timer
    document.getElementById('score').textContent = '0';
    startTime = Date.now();
    
    // Start timer
    gameTimer = setInterval(updateTimer, 1000);
    
    // Create new game
    game = new Game();
}

function restartGame() {
    startNewGame();
}

function showGameOver(score, gameTime) {
    document.getElementById('finalScore').textContent = score;
    document.getElementById('timePlayed').textContent = formatTime(gameTime);
    document.getElementById('gameOver').style.display = 'block';
}

function updateTimer() {
    if (startTime) {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('timer').textContent = formatTime(elapsed);
    }
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateConnectionStatus(status, connected) {
    const statusElement = document.getElementById('connectionStatus');
    statusElement.textContent = status;
    statusElement.className = connected ? '' : 'disconnected';
}

async function showHighScores() {
    try {
        const response = await fetch('/api/high-scores');
        const scores = await response.json();
        
        const listElement = document.getElementById('highScoresList');
        listElement.innerHTML = '';
        
        if (scores.length === 0) {
            listElement.innerHTML = '<p>No high scores yet. Be the first!</p>';
        } else {
            scores.forEach((score, index) => {
                const item = document.createElement('div');
                item.className = 'high-score-item';
                item.innerHTML = `
                    <span>${index + 1}. ${score.player_name}</span>
                    <span>Score: ${score.score}</span>
                    <span>${formatTime(score.game_duration)}</span>
                `;
                listElement.appendChild(item);
            });
        }
        
        document.getElementById('highScoresModal').style.display = 'block';
    } catch (error) {
        console.error('Failed to load high scores:', error);
        alert('Failed to load high scores. Please try again.');
    }
}

function closeHighScores() {
    document.getElementById('highScoresModal').style.display = 'none';
}

// Initialize connection status
updateConnectionStatus('Connecting...', false);