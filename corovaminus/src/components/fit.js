// import library
import LM from 'ml-levenberg-marquardt';

// const LM = require('ml-levenberg-marquardt').default;

// function that receives the parameters and returns
// a function with the independent variable as a parameter

export default function (x, y, func, initialValues, minValues, maxValues) {

    // array of points to fit
    let data = {
        x: x,
        y: y
    };

    const options = {
        damping: 1e-4,
        initialValues: initialValues,
        minValues: minValues,
        maxValues: maxValues,
        gradientDifference: 0.01,
        maxIterations: 10000,
        errorTolerance: 65
    };

    let fittedParams = LM(data, func, options);
    return fittedParams;
}
