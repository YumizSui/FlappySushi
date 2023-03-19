class Pipe {
  constructor(x, y, isBottom) {
      this.x = x;
      this.y = y;
      this.isBottom = isBottom;
  }

  update() {
      this.x -= SUSHI_SPEED;
  }
}
