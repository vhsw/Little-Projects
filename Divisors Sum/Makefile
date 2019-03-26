CFLAGS := -Wall -Wextra -lm -O3  -march=native
CXXFLAGS := $(CFLAGS)

all: clean run_test

run_test: c_divisors cpp_divisors python_divisors rust_divisors
	./run_test.sh 

c_divisors: C/divisors.c	
	gcc $(CFLAGS) C/divisors.c -o c_divisors

cpp_divisors: C++/divisors.cpp
	g++ $(CXXFLAGS) C++/divisors.cpp -o cpp_divisors

python_divisors:
	cp python/divisors.py python_divisors

rust_divisors:
	cd rust && cargo build --release && cd .. && cp rust/target/release/divisors_sum ./rust_divisors

clean: clean_results
	rm -f c_divisors cpp_divisors python_divisors rust_divisors
clean_results:
	rm -f results.md
