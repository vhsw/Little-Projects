// eslint-disable-next-line no-unused-vars
class Person {
  constructor(width, height, id) {
    this.id = id;
    this.x = random(-width / 2, width / 2);
    this.y = random(-height / 2, height / 2);
    this.vel_x = randomGaussian(0, 1);
    this.vel_y = randomGaussian(0, 1);
    this.traveler = random(0, 10) < 1;
    this.radius = 5;
    this.health = 100;
    this.damage = random(1, 5);
    this.infection = 0;
    this.immune = random(1, 5);
  }

  get infected() {
    return this.infection > 0;
  }

  get color() {
    if (this.dead) return 'rgb(10, 10, 10)';
    if (this.infected) return 'red';
    return 'white';
  }

  get dead() {
    return this.health <= 0;
  }

  move() {
    if (random(0, 10) < 1) {
      this.vel_x = randomGaussian(0, 1);
      this.vel_y = randomGaussian(0, 1);
    }
    this.x += this.vel_x;
    this.y += this.vel_y;
  }

  step() {
    if (this.dead) return;

    if (this.infected) {
      this.health -= this.damage;
      this.infection -= this.immune;
    }
    this.move();
    if (this.x < -width / 2) {
      this.x = -width / 2;
      this.vel_x = -this.vel_x;
    }
    if (this.y < -height / 2) {
      this.y = -height / 2;
      this.vel_y = -this.vel_y;
    }
    if (this.x > width / 2) {
      this.x = width / 2;
      this.vel_x = -this.vel_x;
    }
    if (this.y > height / 2) {
      this.y = height / 2;
      this.vel_y = -this.vel_y;
    }
  }


  draw() {
    fill(this.color);
    // eslint-disable-next-line no-undef
    circle(this.x, this.y, this.radius);
  }

  contact(other) {
    if (this.id === other.id) return;
    if (this.dead || other.dead) return;

    const dist = Math.sqrt((this.x - other.x) ** 2 + (this.y - other.y) ** 2);
    if (dist < 25) {
      stroke('rgba(255,255,255,0.20)');
      line(this.x, this.y, other.x, other.y);
      if (this.infected) return;
      if (other.infected && random(0, 100) < 10) this.infection = 100;
    }
  }
}
