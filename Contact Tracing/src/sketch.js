// eslint-disable-next-line spaced-comment
/// <reference path="../../node_modules/@types/p5/global.d.ts" />

function getPerson(width, height, i) {
  const r = random(0, 100);
  if (r < 10) return new Traveler(width, height, i);
  return new Person(width, height, i);
}
const circles = [];

// eslint-disable-next-line no-unused-vars
function setup() {
  createCanvas(windowWidth, windowHeight);
  for (let i = 0; i < windowWidth; i += 1) {
    const c = getPerson(width, height, i);
    circles.push(c);
  }
  circles[0].infection = 1000;
  frameRate(30);
}

// eslint-disable-next-line no-unused-vars
function draw() {
  translate(width / 2, height / 2);
  background(0);
  circles.forEach(
    (c) => {
      circles.forEach((c2) => {
        c.contact(c2);
      });
      c.step();
      c.draw();
    },
  );
}
