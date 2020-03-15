class Traveler extends Person {
  move() {
    this.x += this.vel_x * 4;
    this.y += this.vel_y * 4;
  }
}
