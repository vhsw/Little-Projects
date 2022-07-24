window.onload = async () => {
  const viewport = document.getElementById("viewport");
  const viewportCtx = viewport.getContext("2d");
  const overlay = document.getElementById("overlay");
  const overlayCtx = overlay.getContext("2d");
  let blink = true;
  window.ondblclick = () => {
    blink = !blink;
    toggleDisplay(overlay);
  };
  setInterval(() => {
    if (blink) toggleDisplay(overlay);
  }, 500);
  await loadImage(viewportCtx, "place2022.png");
  // findAmongii(viewportCtx, (x, y, w, h) => stroke(overlayCtx, x, y, w, h));

  // Using cached image, because finding all amongii takes around 10 seconds
  await loadImage(overlayCtx, "amongii.png");
};

/**
 * @param {CanvasRenderingContext2D } ctx
 * @param {string } src
 */
async function loadImage(ctx, src) {
  const image = new Image();
  image.src = src;
  await image.decode();
  ctx.drawImage(image, 0, 0);
}

/**
 * @param {CanvasRenderingContext2D } ctx
 * @param {(x: number, y: number, w: number, h: number) => void} onAmongus
 */
function findAmongii(ctx, onAmongus) {
  const detectors = createDetectors();
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;
  const data = toIndex(ctx);
  const amongii = [];
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      for (const detector of detectors) {
        const detected = detector(x, y, data, width, height);
        if (detected) {
          onAmongus(x, y, detected.width, detected.height);
          amongii.push({
            x,
            y,
            width: detected.width,
            height: detected.height,
          });
          break;
        }
      }
    }
  }
}
/**
 * @param {CanvasRenderingContext2D } ctx
 */
function toIndex(ctx) {
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;
  const data = ctx.getImageData(0, 0, width, height).data;
  const pixels = [];
  for (let index = 0; index < data.length; index += 4) {
    const pixel = new DataView(data.buffer, index, 4).getUint32();
    pixels.push(pixel);
  }
  return pixels;
}

/**
 * @param {CanvasRenderingContext2D} ctx
 */
function createDetectors() {
  // 'X' - body
  // ' ' - background
  // '?' - any color
  // prettier-ignore
  const amongii = [
    [
      " XXX",
      "XX  ",
      "XX  ",
      "XXXX",
      " XXX",
      " X X",
    ],
    [
      " XXX",
      "XX  ",
      "XXXX",
      " XXX",
      "?X X",
    ],
    [
      " XXX",
      "?X  ",
      "?XXX",
      "?XXX",
      " X X",
    ],
    [
      " XXX",
      "XX  ",
      "XXXX",
      " X X",
    ],
  ];
  return amongii.flatMap(mirror).map(createSingleDetector);
  /**
   * @param {string[]} original
   */
  function mirror(original) {
    const mirrored = original.map((line) => [...line].reverse().join(""));
    return [original, mirrored];
  }

  /**
   * @param {string[]} shape
   */
  function createSingleDetector(shape) {
    const width = shape[0].length;
    const height = shape.length;
    const line = shape.join("");
    const amoungus = [];
    const background = [];
    line.split("").forEach((char, index) => {
      if (char == "?") return;
      const target = char == "X" ? amoungus : background;
      target.push(index);
    });

    /**
     * @param {number[]} data
     * @param {number} x
     * @param {number} y
     * @param {number} dataWidth
     * @param {number} dataHeight
     */
    function detector(x, y, data, dataWidth, dataHeight) {
      if (x + width >= dataWidth || y + height >= dataHeight) return;
      const pixels = [];
      for (let i = y; i < y + height; i++) {
        for (let j = x; j < x + width; j++) {
          pixels.push(data[i * dataWidth + j]);
        }
      }
      const amongusPixels = amoungus.map((i) => pixels[i]);

      const amongusColor = amongusPixels[0];

      if (amongusPixels.some((p) => p !== amongusColor)) return;
      const backgroundPixels = background.map((i) => pixels[i]);
      if (backgroundPixels.some((p) => p === amongusColor)) return;
      return { width, height };
    }
    return detector;
  }
}

/**
 * @param {CanvasRenderingContext2D } ctx
 * @param {number} x
 * @param {number} y
 */
function stroke(ctx, x, y, w, h) {
  ctx.lineWidth = 1;
  ctx.strokeStyle = "red";
  ctx.strokeRect(x - 1, y - 1, w + 2, h + 2);
}

/**
 * @param {HTMLElement} element
 */
function toggleDisplay(element) {
  element.style.display = element.style.display == "none" ? "block" : "none";
}
