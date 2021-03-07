function drawImage (n, size = 8) {
  const canvas = document.getElementById('largeCanvas')
  const width = canvas.width / size
  const height = canvas.height / size
  const ctx = canvas.getContext('2d')
  const bits = n.toString(2).padStart(size * size, '0')
  console.log(n, bits)
  for (let x = 0; x < size; x++) {
    for (let y = 0; y < size; y++) {
      let color
      if (bits[x * size + y] == '1') {
        color = 'black'
      } else {
        color = 'white'
      }
      const top_x = x * width
      const top_y = y * height
      const bot_x = top_x + width
      const bot_y = top_y + height
      ctx.fillStyle = color
      ctx.fillRect(top_x, top_y, bot_x, bot_y)
      console.log(bits[x * size + y], top_x, top_y, bot_x, bot_y)
    }
  }
}

function getRandomInt (max) {
  return Math.floor(Math.random() * Math.floor(max))
}

const size = 8
const id = BigInt(window.location.pathname.substr(1))
drawImage(id, size)
