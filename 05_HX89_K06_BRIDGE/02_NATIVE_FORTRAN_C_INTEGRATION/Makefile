FC = gfortran
CC = gcc
FFLAGS = -std=f2008 -O2 -Wall -Wextra -Werror -fcheck=all -fbacktrace -ffree-line-length-none
CFLAGS = -std=c11 -O2 -Wall -Wextra -Werror -fstack-protector-strong -D_FORTIFY_SOURCE=2
LDFLAGS = -llapack -lblas -lcrypto -lm
ACDC = ../../02_ANALOG_MATH/01_ACDC_LINEAR_NETWORK
BATCH = ../../03_CPU_NATIVE/06_CPU_BATCH_TARGETED_INTRINSICS
all: build/void_loop
build/void_loop: src/void_native.f90 src/hx89_exec.c src/cpu_feedback.c src/cpu_cycle.c $(ACDC)/analog_core.c $(BATCH)/cpu_batch.c
	mkdir -p build
	$(CC) $(CFLAGS) -c src/hx89_exec.c -o build/hx89_exec.o
	$(CC) $(CFLAGS) -c src/cpu_feedback.c -o build/cpu_feedback.o
	$(CC) $(CFLAGS) -c src/cpu_cycle.c -o build/cpu_cycle.o
	$(CC) $(CFLAGS) -Wno-unused-function -Wno-unused-const-variable -DVOID_ACDC_LIBRARY -c $(ACDC)/analog_core.c -o build/acdc_core.o
	$(CC) $(CFLAGS) -Wno-unused-function -DVOID_BATCH_LIBRARY -c $(BATCH)/cpu_batch.c -o build/cpu_batch_kernel.o
	$(FC) $(FFLAGS) -J build src/void_native.f90 build/hx89_exec.o build/cpu_feedback.o build/cpu_cycle.o build/acdc_core.o build/cpu_batch_kernel.o -o $@ $(LDFLAGS)
build/native_cpu_state_contract: tests/native_cpu_state_contract.c src/cpu_cycle.c
	mkdir -p build
	$(CC) $(CFLAGS) tests/native_cpu_state_contract.c src/cpu_cycle.c -o $@

clean:
	rm -f build/void_loop build/hx89_exec.o build/cpu_feedback.o build/cpu_cycle.o build/acdc_core.o build/cpu_batch_kernel.o build/*.mod
.PHONY: all clean

build/native_driver_contract: tests/native_driver_contract.c src/hx89_exec.c src/cpu_feedback.c src/cpu_cycle.c
	$(CC) $(CFLAGS) tests/native_driver_contract.c src/hx89_exec.c src/cpu_feedback.c src/cpu_cycle.c -o $@ -lcrypto
