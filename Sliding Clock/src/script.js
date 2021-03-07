function move (item, value) {
  item.style.transform = `translate(0px, ${-value * 100}px)`
}

function update () {
  const date = new Date()
  move(document.querySelector('.seconds'), date.getSeconds() % 10)
  move(document.querySelector('.minutes'), date.getMinutes() % 10)
  move(document.querySelector('.hours'), date.getHours() % 10)

  move(
    document.querySelector('.seconds-tenth'),
    Math.floor(date.getSeconds() / 10)
  )
  move(
    document.querySelector('.minutes-tenth'),
    Math.floor(date.getMinutes() / 10)
  )
  move(
    document.querySelector('.hours-tenth'),
    Math.floor(date.getHours() / 10)
  )

  window.scrollTo(0, 0)
}

setInterval(update, 1000)
