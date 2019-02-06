function drawImage(n, size = 8) {
    let canvas = document.getElementById("largeCanvas");
    let width = canvas.width / size;
    let height = canvas.height / size;
    let ctx = canvas.getContext("2d");
    let bits = n.toString(2).padStart(size * size, '0');
    console.log(n, bits);
    for (let x = 0; x < size; x++) {
        for (let y = 0; y < size; y++) {
            let color;
            if (bits[x * size + y] == '1') {
                color = "black";
            } else {
                color = "white";
            }
            let top_x = x * width;
            let top_y = y * height;
            let bot_x = top_x + width;
            let bot_y = top_y + height;
            ctx.fillStyle = color;
            ctx.fillRect(top_x, top_y, bot_x, bot_y);
            console.log(bits[x * size + y], top_x, top_y, bot_x, bot_y);
        }
    }
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

let size = 8;
let id = BigInt(window.location.pathname.substr(1));
drawImage(id, size)