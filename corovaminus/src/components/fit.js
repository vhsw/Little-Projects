import LM from 'ml-levenberg-marquardt';

export default function (x, y, func, options) {
    let data = {
        x: x,
        y: y
    };


    return LM(data, func, options);
}
