use std::env;

fn divisors_sum(n: usize) {
    let mut arr: Vec<usize> =  vec![0; (n+1) as usize];
    let upper_lim: usize = (n as f64).sqrt() as usize + 1;
    for  k1 in 1usize..upper_lim {
        for k2 in k1..(n / k1 + 1) {
            let val = if k1 != k2  {k1 + k2} else {k1};
            arr[k1 * k2] += val;
        }
    }

    println!("{}", arr.last().unwrap());
}

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        2 => {
            let n: usize = args[1].parse::<usize>().unwrap();
            divisors_sum(n);
        },
        _ => {
            eprintln!("Usage: {} maxN", args[0]);
        }
    }
}
