export default function (dates) {
    let min = Math.min(...dates);
    return dates.map(it => (it - min) / 1000 / 60 / 60 / 24);
}
