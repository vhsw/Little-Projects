// eslint-disable-next-line spaced-comment
/// <reference path="../../node_modules/@types/p5/global.d.ts" />


let SIZE;
const DIM = 4;

function euclideanSquare(p1, p2) {
  let distance = 0;
  for (let i = 0; i < p1.length; i += 1) {
    distance += (p1[i] - p2[i]) ** 2;
  }
  return distance;
}

const sides = new Set();
const points = [];

// eslint-disable-next-line no-unused-vars
function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  SIZE = Math.min(windowWidth, windowHeight);

  for (let i = 0; i < 2 ** DIM; i += 1) {
    const coords = [];
    // eslint-disable-next-line no-bitwise
    for (let mask = 1; mask < 2 ** DIM; mask <<= 1) {
      // eslint-disable-next-line no-bitwise
      const bitSet = ((i & mask) > 0);
      coords.push(bitSet ? 0.5 : -0.5);
    }
    points.push(coords);
  }

  points.forEach((p1) => {
    points.forEach((p2) => {
      if (euclideanSquare(p1, p2) === 1) {
        const side = [p1, p2];
        side.sort();
        sides.add(side);
      }
    });
  });
}

function rotate4d(p, angle) {
  const s = Math.sin(angle);
  const c = Math.cos(angle);

  const rotationMatrix = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, c, -s],
    [0, 0, s, c],
  ];

  return rotationMatrix.map((v) => v.reduce(
    (acc, n, i) => acc + n * p[i], 0,
  ));
}


function flattern(point, distance = 1.5) {
  const len = point.length;
  const w = 1 / (distance - point[len - 1]);
  return point.slice(0, len - 1).map((c) => c * w);
}

function project(point, angle) {
  let p = point;
  for (let i = DIM; i > 4; i -= 1) {
    p = flattern(p);
  }
  if (DIM >= 4) {
    p = rotate4d(p, angle);
  }
  if (DIM > 3) {
    p = flattern(p);
  }
  return p.map((s) => s * SIZE * 0.5);
}

// eslint-disable-next-line no-unused-vars
function draw() {
  background(0);

  stroke(255);


  rotateY(frameCount * 0.003);
  const angle = frameCount * 0.02;

  points.forEach((p) => {
    push();
    const proj = project(p, angle);
    translate(...proj);
    sphere(SIZE / 100);
    pop();
  });

  sides.forEach((l) => {
    const [start, end] = l.map((p) => project(p, angle));
    line(...start, ...end);
  });
}
