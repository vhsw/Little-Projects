/// <reference path="../../node_modules/@types/p5/global.d.ts" />

const N_POINTS = 30
const N_WEIGHTS = (N_POINTS - 1) * N_POINTS / 2
let weightSilder
let distanceSlider
/** @type Point[] */
let points = []
let decaySlider
let showLabels
let weights = {}
let best = Infinity

class Point {
  /**
   * @param {number} x
   * @param {number} y
   * @param {number} id
   */
  constructor (x, y, id) {
    this.id = id
    this.x = x
    this.y = y
  }

  display () {
    strokeWeight(10)
    stroke('white')
    point(this.x, this.y)
    if (showLabels.checked()) {
      stroke(0)
      strokeWeight(1)
      text(`id=${this.id}`, this.x + 5, this.y - 10)
    }
  }

  /**
   * @param {Point} other
   */
  distance (other) {
    return Math.sqrt((this.x - other.x) ** 2 + (this.y - other.y) ** 2) / max(windowWidth, windowHeight)
  }
}

function resetWeights () {
  for (let i = 0; i < N_POINTS; i++) {
    for (let j = 0; j < i; j++) {
      weights[[j, i]] = 1 / N_WEIGHTS
    }
  }
  best = Infinity
}
function randomWeights () {
  for (let i = 0; i < N_POINTS; i++) {
    for (let j = 0; j < i; j++) {
      weights[[j, i]] = random() / N_WEIGHTS
    }
  }
}
function circlePoints () {
  points = []
  for (let i = 0; i < N_POINTS; i++) {
    const offset = 1 / N_POINTS
    const step = 2 * PI / N_POINTS
    const x = (sin(step * i) + randomGaussian(0, offset)) * windowWidth / 3 + windowWidth / 2
    const y = (cos(step * i) + randomGaussian(0, offset)) * windowHeight / 3 + windowHeight / 2
    points.push(new Point(x, y, i))
  }
  resetWeights()
}
function gridPoints () {
  points = []
  const side = int(sqrt(N_POINTS))
  const offset = 200

  for (let i = 0; i < side; i++) {
    for (let j = 0; j < side; j++) {
      const x = (i + randomGaussian(0, 0.1)) * (windowWidth - offset) / side + offset
      const y = (j + +randomGaussian(0, 0.1)) * (windowHeight - offset) / side + offset
      points.push(new Point(x, y, i * side + j))
    }
  }
  for (let i = side * side; i < N_POINTS; i++) {
    const x = random(offset, windowWidth - offset)
    const y = random(offset, windowHeight - offset)
    points.push(new Point(x, y, i))
  }
  resetWeights()
}
function randomPoints () {
  points = []
  for (let i = 0; i < N_POINTS; i++) {
    const offset = 50
    const x = random(offset, windowWidth - offset)
    const y = random(offset, windowHeight - offset)
    points.push(new Point(x, y, i))
  }
  resetWeights()
}

function setup () {
  createCanvas(windowWidth, windowHeight)
  showLabels = createCheckbox('Show labels', false)
  showLabels.position(20, 20).style('color', 'white')
  decaySlider = createSlider(0.01, 1, 0.95, 0).position(20, 40)
  createSpan('Decay').position(160, 40).style('color', 'white')

  weightSilder = createSlider(0, 10, 4, 0).position(20, 60)
  createSpan('Weight Value').position(160, 60).style('color', 'white')

  distanceSlider = createSlider(0, 10, 4, 0).position(20, 80)

  createSpan('Distanve Value').position(160, 80).style('color', 'white')

  createButton('Reset Weights').position(20, 110).mouseClicked(resetWeights)

  createButton('Random Weights').position(20, 140).mouseClicked(randomWeights)

  createButton('Random Points').position(20, 170).mouseClicked(randomPoints)

  createButton('Circle Points').position(20, 200).mouseClicked(circlePoints)

  createButton('Grid Points').position(20, 230).mouseClicked(gridPoints)

  randomPoints()
  frameRate(10)
}
/**
 * @param {Point} p1
 * @param {Point} p2
 */
function getWeight (p1, p2) {
  if (p1.id === p2.id) return 0
  let route = [p1.id, p2.id]
  if (p1.id > p2.id) { route = [p2.id, p1.id] }
  return Math.pow(weights[route], weightSilder.value()) / Math.pow(p1.distance(p2), distanceSlider.value())
}

/**
 * @param {Point} src
 * @param {Set<Point>} todo
 */
function getNext (src, todo) {
  if (todo.size === 0) return
  const choices = Array.from(todo)
  const weight = choices.map((dst) => getWeight(src, dst))
  let randomVal = random(weight.reduce((p, c) => p + c))
  for (let i = 0; i < choices.length; i++) {
    randomVal -= weight[i]
    if (randomVal <= 0) return choices[i]
  }
  throw Error('what?!')
}

function draw () {
  background(0)
  fill('white')
  strokeCap(ROUND)
  for (let i = 0; i < N_POINTS; i++) {
    for (let j = 0; j < i; j++) {
      const weight = weights[[j, i]] * N_WEIGHTS
      const [x1, y1] = [points[i].x, points[i].y]
      const [x2, y2] = [points[j].x, points[j].y]
      stroke(`rgba(255,255,255,${weight})`)
      strokeWeight(weight)
      line(x1, y1, x2, y2)
      if (showLabels.checked()) {
        stroke(0)
        strokeWeight(1)
        text(`w=${weight.toFixed(2)}`, (x1 + x2) / 2, (y1 + y2) / 2)
        fill('white')
      }
    }
  }
  points.forEach(p => p.display())

  const tmpWeights = { ...weights }
  /** @type number[][] */
  const pathes = []
  /** @type number[] */
  const costs = []

  for (let ant = 0; ant < N_POINTS; ant++) {
    const todo = new Set(points)
    costs[ant] = 0
    pathes[ant] = []
    let src = points[ant]
    while (todo.size > 0) {
      todo.delete(src)
      const dst = getNext(src, todo) || points[ant]
      pathes[ant].push(dst.id)
      costs[ant] += src.distance(dst)
      src = dst
    }
  }
  const minCost = min(costs)
  best = min(best, minCost)
  const mean = costs.reduce((a, b) => a + b) / costs.length
  stroke(0)
  strokeWeight(1)
  text(`Best Length=${best.toFixed(2)}`, 320, 20)
  text(`Current Best=${minCost.toFixed(2)}`, 320, 40)
  text(`Current Mean=${mean.toFixed(2)}`, 320, 60)

  for (let ant = 0; ant < N_POINTS; ant++) {
    const path = pathes[ant]
    const cost = costs[ant]
    const goodness = (best / cost)
    if (goodness > 0.9) {
      for (let i = 0; i < path.length - 1; i++) {
        const route = [path[i], path[i + 1]].sort((a, b) => a - b)
        tmpWeights[route] = weights[route] + Math.pow(goodness + 0.1, 3) / N_WEIGHTS / N_POINTS
      }
    }
  }
  const minIdx = costs.indexOf(minCost)
  const bestPath = pathes[minIdx]
  bestPath.push(bestPath[0])
  for (let i = 0; i < bestPath.length - 1; i++) {
    stroke('red')
    strokeWeight(3)
    const [x1, y1] = [points[bestPath[i]].x, points[bestPath[i]].y]
    const [x2, y2] = [points[bestPath[i + 1]].x, points[bestPath[i + 1]].y]
    line(x1, y1, x2, y2)
  }

  let totalWeight = 0
  for (const key in tmpWeights) {
    totalWeight += tmpWeights[key]
  }
  if (totalWeight > 0) {
    for (const key in tmpWeights) {
      tmpWeights[key] /= totalWeight
    }
  }
  for (const key in tmpWeights) {
    tmpWeights[key] *= decaySlider.value()
    totalWeight += tmpWeights[key]
  }
  weights = tmpWeights
}
