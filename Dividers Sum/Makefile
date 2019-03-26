CFLAGS := -Wall -Wextra -lm -O3  -march=native
CXXFLAGS := $(CFLAGS)

all: clean run_test

run_test: c_dividers cpp_dividers python_dividers rust_dividers
	./run_test.sh 

c_dividers: C/dividers.c	
	gcc $(CFLAGS) C/dividers.c -o c_dividers

cpp_dividers: C++/dividers.cpp
	g++ $(CXXFLAGS) C++/dividers.cpp -o cpp_dividers

python_dividers:
	cp python/dividers.py python_dividers

rust_dividers:
	cd rust && cargo build --release && cd .. && cp rust/target/release/dividers_sum ./rust_dividers

clean: clean_results
	rm -f c_dividers cpp_dividers python_dividers rust_dividers
clean_results:
	rm -f results.md
