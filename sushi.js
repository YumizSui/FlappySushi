class Sushi {
  constructor(x, y) {
      this.x = x;
      this.y = y;
      this.speedY = 0;
  }

  update() {
      this.speedY += GRAVITY;
      this.y += this.speedY;
  }

  flap(heldFrames) {
      if (heldFrames < WEAK_JUMP_THRESHOLD) {
          this.speedY = -WEAK_JUMP_STRENGTH;
      } else {
          const jumpStrength = WEAK_JUMP_STRENGTH + Math.min(MAX_JUMP_STRENGTH - WEAK_JUMP_STRENGTH, (heldFrames - WEAK_JUMP_THRESHOLD) * (MAX_JUMP_STRENGTH - WEAK_JUMP_STRENGTH) / (STRONG_JUMP_THRESHOLD - WEAK_JUMP_THRESHOLD));
          this.speedY = -jumpStrength;
      }
  }
}
