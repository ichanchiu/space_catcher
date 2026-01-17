const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- Configuration & Constants ---
const WIDTH = 800;
const HEIGHT = 600;

// Set logical size
canvas.width = WIDTH;
canvas.height = HEIGHT;

// Colors
const COLORS = {
    white: '#FFFFFF',
    black: '#0A0A1E',
    yellow: '#FFD700',
    red: '#FF3232',
    blue: '#3296FF',
    gray: '#646464',
    green: '#00FF64',
    orange: '#FF8000',
    cyan: '#00FFFF',
    purple: '#9370DB'
};

// Game State
let gameState = 'MENU'; // MENU, PLAYING, GAMEOVER
let score = 0;
let lastTime = 0;
let keys = {};

// Settings (default, overwritten by difficulty)
let settings = {
    playerSpeed: 8,
    supplySpeedMin: 3,
    supplySpeedMax: 7,
    planetSpeedMin: 2,
    planetSpeedMax: 5,
    planetCount: 2
};

const DIFFICULTY = {
    easy: { playerSpeed: 6, supplySpeedMin: 2, supplySpeedMax: 5, planetSpeedMin: 2, planetSpeedMax: 4, planetCount: 1 },
    normal: { playerSpeed: 9, supplySpeedMin: 4, supplySpeedMax: 8, planetSpeedMin: 3, planetSpeedMax: 7, planetCount: 3 },
    hard: { playerSpeed: 12, supplySpeedMin: 6, supplySpeedMax: 12, planetSpeedMin: 6, planetSpeedMax: 10, planetCount: 5 }
};

// --- Classes ---

class Star {
    constructor() {
        this.reset();
        // Initial random y
        this.y = Math.random() * HEIGHT;
    }

    reset() {
        this.size = Math.random() * 2 + 1;
        this.x = Math.random() * WIDTH;
        this.y = 0;
        this.speed = Math.random() * 3 + 1;
        this.alpha = Math.random() * 0.5 + 0.3;
    }

    update() {
        this.y += this.speed;
        if (this.y > HEIGHT) {
            this.reset();
        }
    }

    draw() {
        ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha})`;
        ctx.beginPath();
        ctx.rect(this.x, this.y, this.size, this.size);
        ctx.fill();
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = Math.random() * 3 + 2;
        this.speedX = (Math.random() - 0.5) * 6;
        this.speedY = (Math.random() - 0.5) * 6;
        this.life = 1.0;
        this.decay = Math.random() * 0.03 + 0.01;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.life -= this.decay;
        this.size *= 0.95;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

class Player {
    constructor() {
        this.width = 50;
        this.height = 60;
        this.x = WIDTH / 2 - this.width / 2;
        this.y = HEIGHT - this.height - 20;
        this.speedX = 0;
    }

    update() {
        this.speedX = 0;
        if (keys['ArrowLeft']) this.speedX = -settings.playerSpeed;
        if (keys['ArrowRight']) this.speedX = settings.playerSpeed;

        this.x += this.speedX;

        // Boundaries
        if (this.x < 0) this.x = 0;
        if (this.x + this.width > WIDTH) this.x = WIDTH - this.width;
    }

    draw() {
        // Draw similar to Python version but with path
        let x = this.x;
        let y = this.y;
        let w = this.width;
        let h = this.height;

        ctx.save();

        // Wings (Gray)
        ctx.fillStyle = COLORS.gray;
        ctx.beginPath();
        ctx.moveTo(x, y + h);
        ctx.lineTo(x + w, y + h);
        ctx.lineTo(x + w / 2, y + h / 2);
        ctx.fill();

        // Body (Blue with White border)
        ctx.fillStyle = COLORS.blue;
        ctx.strokeStyle = COLORS.white;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x + w / 2, y);
        ctx.lineTo(x + 10, y + h - 5);
        ctx.lineTo(x + w - 10, y + h - 5);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Cockpit (Cyan)
        ctx.fillStyle = COLORS.cyan;
        ctx.beginPath();
        ctx.ellipse(x + w / 2, y + h / 2 - 5, 5, 10, 0, 0, Math.PI * 2);
        ctx.fill();

        // Flame (Orange, flickering)
        let flameH = Math.random() * 15 + 10;
        ctx.fillStyle = COLORS.orange;
        ctx.beginPath();
        ctx.moveTo(x + 15, y + h - 5);
        ctx.lineTo(x + w / 2, y + h - 5 + flameH);
        ctx.lineTo(x + w - 15, y + h - 5);
        ctx.fill();

        ctx.restore();
    }
}

class Supply {
    constructor() {
        this.reset();
        // Allow initial random y offscreen but varied
        this.y = Math.random() * -500 - 50;
    }

    reset() {
        const types = ['small', 'medium', 'large'];
        this.type = types[Math.floor(Math.random() * types.length)];

        if (this.type === 'small') {
            this.radius = 15; this.color = COLORS.green; this.value = 10;
        } else if (this.type === 'medium') {
            this.radius = 20; this.color = COLORS.cyan; this.value = 20;
        } else {
            this.radius = 25; this.color = COLORS.yellow; this.value = 30;
        }

        this.x = Math.random() * (WIDTH - this.radius * 2) + this.radius;
        this.y = -this.radius * 2;
        this.speedY = Math.random() * (settings.supplySpeedMax - settings.supplySpeedMin) + settings.supplySpeedMin;
    }

    update() {
        this.y += this.speedY;
        if (this.y - this.radius > HEIGHT) {
            this.reset();
        }
    }

    draw() {
        ctx.save();

        // Glow
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;

        // Circle body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        // Inner highlight
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath();
        ctx.arc(this.x - this.radius * 0.3, this.y - this.radius * 0.3, this.radius * 0.4, 0, Math.PI * 2);
        ctx.fill();

        // Plus sign
        ctx.strokeStyle = COLORS.white;
        ctx.lineWidth = 3;
        ctx.shadowBlur = 0; // reset shadow for sharp line
        ctx.beginPath();
        // Horizontal
        ctx.moveTo(this.x - this.radius * 0.5, this.y);
        ctx.lineTo(this.x + this.radius * 0.5, this.y);
        // Vertical
        ctx.moveTo(this.x, this.y - this.radius * 0.5);
        ctx.lineTo(this.x, this.y + this.radius * 0.5);
        ctx.stroke();

        ctx.restore();
    }
}

class Planet {
    constructor() {
        this.reset();
        this.y = Math.random() * -1000 - 100;
    }

    reset() {
        this.radius = Math.random() * 30 + 35; // 35-65
        this.x = Math.random() * (WIDTH - this.radius * 2) + this.radius;
        this.y = -this.radius * 2;
        this.speedY = Math.random() * (settings.planetSpeedMax - settings.planetSpeedMin) + settings.planetSpeedMin;

        const colors = ['#8B0000', '#4B0082', '#323232'];
        this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
        this.y += this.speedY;
        if (this.y - this.radius > HEIGHT) {
            this.reset();
        }
    }

    draw() {
        ctx.save();

        // Main Body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        // Craters / Texture
        ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
        ctx.beginPath();
        ctx.arc(this.x - 15, this.y - 15, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(this.x + 20, this.y + 10, 15, 0, Math.PI * 2);
        ctx.fill();

        // Warning Border
        ctx.strokeStyle = COLORS.red;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.stroke();

        ctx.restore();
    }
}

// --- Audio ---
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const sounds = {};

async function loadSound(name, path) {
    try {
        const response = await fetch(path);
        const arrayBuffer = await response.arrayBuffer();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
        sounds[name] = audioBuffer;
    } catch (e) {
        console.warn(`Failed to load sound ${name}:`, e);
    }
}

function playSound(name) {
    if (sounds[name] && audioCtx.state === 'running') {
        const source = audioCtx.createBufferSource();
        source.buffer = sounds[name];
        source.connect(audioCtx.destination);
        source.start(0);
    } else if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

// Load sounds
loadSound('coin', 'assets/coin.wav');
loadSound('explosion', 'assets/explosion.wav');
loadSound('select', 'assets/select.wav');

// --- Managers ---

let player;
let starField = [];
let supplyList = [];
let planetList = [];
let particleList = [];

function initGame() {
    // Ensure Audio Context is resumed on user interaction
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    player = new Player();
    starField = [];
    for (let i = 0; i < 50; i++) starField.push(new Star());

    supplyList = [];
    for (let i = 0; i < 3; i++) supplyList.push(new Supply());

    planetList = [];
    for (let i = 0; i < settings.planetCount; i++) planetList.push(new Planet());

    particleList = [];
    score = 0;
    document.getElementById('score-display').innerText = `Score: 0`;
}

function spawnExplosion(x, y, color) {
    for (let i = 0; i < 15; i++) {
        particleList.push(new Particle(x, y, color));
    }
}

function spawnSparkles(x, y, color) {
    for (let i = 0; i < 8; i++) {
        particleList.push(new Particle(x, y, color));
    }
}

function checkCollisions() {
    // Player Rect
    // Simple rect collision for player vs circle center approximation
    // This assumes the player hit box is close to the image rect
    let pRect = {
        l: player.x + 10, // shrink bit for fairness
        r: player.x + player.width - 10,
        t: player.y + 10,
        b: player.y + player.height - 10
    };

    // Check Supplies
    for (let s of supplyList) {
        // Circle vs Rect
        let closestX = Math.max(pRect.l, Math.min(s.x, pRect.r));
        let closestY = Math.max(pRect.t, Math.min(s.y, pRect.b));
        let dx = s.x - closestX;
        let dy = s.y - closestY;

        if ((dx * dx + dy * dy) < (s.radius * s.radius)) {
            // Hit
            playSound('coin');
            score += s.value;
            document.getElementById('score-display').innerText = `Score: ${score}`;
            spawnSparkles(s.x, s.y, s.color);
            s.reset();
        }
    }

    // Check Planets
    for (let p of planetList) {
        let closestX = Math.max(pRect.l, Math.min(p.x, pRect.r));
        let closestY = Math.max(pRect.t, Math.min(p.y, pRect.b));
        let dx = p.x - closestX;
        let dy = p.y - closestY;

        if ((dx * dx + dy * dy) < (p.radius * p.radius)) {
            // Crash
            playSound('explosion');
            spawnExplosion(player.x + player.width / 2, player.y + player.height / 2, COLORS.orange);
            endGame();
        }
    }
}

function endGame() {
    gameState = 'GAMEOVER';
    document.getElementById('final-score').innerText = `Final Score: ${score}`;
    document.getElementById('game-over-screen').classList.add('active');
}

function loop(timestamp) {
    // Delta time could be used, but fixed step is simpler for this port
    if (gameState === 'PLAYING') {
        ctx.clearRect(0, 0, WIDTH, HEIGHT);

        // Update & Draw Stars
        starField.forEach(star => { star.update(); star.draw(); });

        // Update & Draw Player
        player.update();
        player.draw();

        // Update & Draw Supplies
        supplyList.forEach(s => { s.update(); s.draw(); });

        // Update & Draw Planets
        planetList.forEach(p => { p.update(); p.draw(); });

        // Update & Draw Particles
        for (let i = particleList.length - 1; i >= 0; i--) {
            let p = particleList[i];
            p.update();
            p.draw();
            if (p.life <= 0) {
                particleList.splice(i, 1);
            }
        }

        checkCollisions();
    }

    if (gameState === 'PLAYING') {
        requestAnimationFrame(loop);
    }
}

// --- Input & UI Handling ---

window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Diff buttons
document.querySelectorAll('.difficulty-menu .btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        let diff = e.target.dataset.diff;
        settings = Object.assign({}, settings, DIFFICULTY[diff]);

        document.getElementById('start-screen').classList.remove('active');
        gameState = 'PLAYING';
        initGame();
        requestAnimationFrame(loop);
    });
});

// Restart button
document.getElementById('restart-btn').addEventListener('click', () => {
    document.getElementById('game-over-screen').classList.remove('active');
    document.getElementById('start-screen').classList.add('active');
    gameState = 'MENU';
});

// Start initial render for background (optional, or just wait for click)
function drawMenuBackground() {
    if (gameState !== 'PLAYING') {
        ctx.clearRect(0, 0, WIDTH, HEIGHT);
        // Draw some static stars or animation
        if (!starField.length) {
            for (let i = 0; i < 50; i++) starField.push(new Star());
        }
        starField.forEach(star => { star.update(); star.draw(); });
        requestAnimationFrame(drawMenuBackground);
    }
}
drawMenuBackground();
