import { erf } from 'mathjs';

export default function ([amp, offset, sigma]) {
    let day_ms = 60 * 60 * 24 * 1000;
    return (t) => amp / 2 * (erf((t - offset) / (sigma * 0.34 * day_ms)) + 1)
}
