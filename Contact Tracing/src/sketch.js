/// <reference path="../../node_modules/@types/p5/global.d.ts" />
class Person {
  constructor (x, y, id) {
    this.id = id
    this.x = x
    this.y = y
    this.health = 100
    this.infection = 0
    this.updateVel()
  }

  get infected () {
    return this.infection > 0
  }

  get color () {
    if (this.dead) return '#333333'
    if (this.infected) return '#ff0000'
    return '#ffffff'
  }

  get dead () {
    return this.health <= 0
  }

  updateVel () {
    this.vel_x = randomGaussian(0, 1)
    this.vel_y = randomGaussian(0, 1)
    if (random() < 0.1) {
      this.vel_x *= 3
      this.vel_y *= 3
    }
  }

  step () {
    fill(this.color)
    stroke(this.color)
    circle(this.x, this.y, 8)
    if (this.dead) return

    if (this.infected) {
      this.health -= random()
      this.infection -= random()
    }
    if (random() < 0.02) {
      this.updateVel()
    }
    this.x += this.vel_x
    this.y += this.vel_y
    if (this.x < 0) {
      this.x = width
    }
    if (this.y < 0) {
      this.y = height
    }
    if (this.x > width) {
      this.x = 0
    }
    if (this.y > height) {
      this.y = 0
    }
  }

  contact (other) {
    if (this.id === other.id) return
    if (this.dead || other.dead) return

    const dist = (this.x - other.x) ** 2 + (this.y - other.y) ** 2
    if (dist < 4000) {
      if (!this.infected && other.infected && random() < 0.1) this.infection = 100
      stroke((this.infected && other.infected) ? 'rgba(255,0,0,0.20)' : 'rgba(255,255,255,0.20)')
      line(this.x, this.y, other.x, other.y)
    }
  }
}

const circles = []

function setup () {
  createCanvas(windowWidth, windowHeight)
  for (let id = 0; id < 500; id += 1) {
    circles.push(new Person(random(width), random(height), id))
  }
  circles[0].infection = 1000
}

function draw () {
  background(0)

  circles.forEach((c) => {
    circles.forEach((c2) => {
      c.contact(c2)
    })
    c.step()
  })
}
