FC ?= gfortran
CC = gcc
CXX = g++
FFLAGS = -std=f2008 -O2 -Wall -Wextra -Werror -fcheck=all -fbacktrace -ffree-line-length-none
CFLAGS = -std=c11 -O2 -Wall -Wextra -Werror -fstack-protector-strong -D_FORTIFY_SOURCE=2
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -Werror -fstack-protector-strong -D_FORTIFY_SOURCE=2
LIBS = -llapack -lblas -lcrypto -lstdc++ -lm
SRC_BVH = ../../03_CPU_NATIVE/05_ENTROPY_AVX_HARDENED
C_OBJS = build/hx89_exec.o build/cpu_feedback.o build/cpu_cycle.o build/acdc_link.o build/cpu_batch_link.o
CXX_OBJS = build/entropy_bvh_link.o build/bvh_spatial.o build/procedural.o
all: build/void_unified
build:
	mkdir -p build
build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c $< -o $@
build/entropy_bvh_link.o: src/entropy_bvh_link.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@
build/bvh_spatial.o: $(SRC_BVH)/bvh_spatial.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@
build/procedural.o: $(SRC_BVH)/procedural.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@
build/void_unified: src/void_native.f90 $(C_OBJS) $(CXX_OBJS)
	$(FC) $(FFLAGS) -J build src/void_native.f90 $(C_OBJS) $(CXX_OBJS) -o $@ $(LIBS)
build/native_cpu_state_contract: tests/native_cpu_state_contract.c src/cpu_cycle.c | build
	$(CC) $(CFLAGS) $^ -o $@
build/native_driver_contract: tests/native_driver_contract.c src/hx89_exec.c src/cpu_feedback.c src/cpu_cycle.c | build
	$(CC) $(CFLAGS) $^ -o $@ -lcrypto
clean:
	rm -f build/*.o build/*.mod build/void_unified build/native_cpu_state_contract build/native_driver_contract
.PHONY: all clean
