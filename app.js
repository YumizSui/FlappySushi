const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const game = {
  started: false,
  over: false,
  score: 0,
  bestScore: 0,
  pipes: [],
  pipeTimer: 0,
  jumpStartFrame: 0,
  sushi: new Sushi(50, HEIGHT / 2),
  assets: loadAssets(),
};

canvas.addEventListener("keydown", handleEvent);
canvas.addEventListener("keyup", handleEvent);
canvas.tabIndex = 1000;
canvas.focus();
requestAnimationFrame(gameLoop);

function gameLoop() {
  update();
  draw();
  requestAnimationFrame(gameLoop);
}

function handleEvent(event) {
  if (event.type === "keydown" && event.key === " ") {
    if (game.over) {
      restartGame();
    } else if (!game.started) {
      game.started = true;
      game.jumpStartFrame = performance.now();
      game.sushi.flap(0);
    } else {
      game.jumpStartFrame = performance.now();
    }
  } else if (
    event.type === "keyup" &&
    event.key === " " &&
    !game.over &&
    game.started
  ) {
    const heldFrames = ((performance.now() - game.jumpStartFrame) * FPS) / 1000;
    game.sushi.flap(heldFrames);
  }
}


function addPipePair() {
  const gapY = Math.random() * (HEIGHT - GAP_SIZE - HEIGHT / 4) + HEIGHT / 8;
  const pipeTop = new Pipe(WIDTH, gapY - 512, false);
  const pipeBottom = new Pipe(WIDTH, gapY + GAP_SIZE, true);
  game.pipes.push(pipeTop, pipeBottom);
}

function restartGame() {
  game.started = false;
  game.over = false;
  game.score = 0;
  game.sushi = new Sushi(50, HEIGHT / 2);
  game.pipes = [];
}

function checkCollision() {
  if (game.sushi.y < 0 || game.sushi.y + game.assets.sushi.height > HEIGHT) {
    return true;
  }

  for (const pipe of game.pipes) {
    const pipeImage = pipe.isBottom
      ? game.assets.pipeBottom
      : game.assets.pipeTop;
    const pipeRect = {
      x: pipe.x,
      y: pipe.y,
      width: pipeImage.width,
      height: pipeImage.height,
    };
    const sushiRect = {
      x: game.sushi.x,
      y: game.sushi.y,
      width: game.assets.sushi.width,
      height: game.assets.sushi.height,
    };

    if (rectsIntersect(pipeRect, sushiRect)) {
      return true;
    }
  }
  return false;
}

function rectsIntersect(a, b) {
  return a.x < b.x + b.width &&
         a.x + a.width > b.x &&
         a.y < b.y + b.height &&
         a.y + a.height > b.y;
}

function update() {
  if (!game.over && game.started) {
      game.sushi.update();
      game.pipes.forEach(pipe => pipe.update());

      // Pipe generation
      if (game.pipeTimer <= 0) {
          addPipePair();
          game.pipeTimer = 100;
      }
      game.pipeTimer--;

      // Check for collisions
      if (checkCollision()) {
          game.over = true;
      } else {
          // Update the score
          game.score++;
          if (game.score > game.bestScore) {
              game.bestScore = game.score;
          }
      }
  }
}

function draw() {
  ctx.drawImage(game.assets.background, 0, 0);
  ctx.drawImage(game.assets.sushi, game.sushi.x, game.sushi.y);

  game.pipes.forEach(pipe => {
      const pipeImage = pipe.isBottom ? game.assets.pipeBottom : game.assets.pipeTop;
      ctx.drawImage(pipeImage, pipe.x, pipe.y);
  });

  // Draw score and best score
  ctx.fillStyle = 'white';
  ctx.font = '36px sans-serif';
  ctx.fillText(`Best: ${game.bestScore}`, WIDTH / 2 - ctx.measureText(`Best: ${game.bestScore}`).width / 2, 50);
}

