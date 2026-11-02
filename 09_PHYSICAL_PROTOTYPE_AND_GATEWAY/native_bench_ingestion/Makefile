CC = cc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Werror -pedantic -fstack-protector-strong -D_FORTIFY_SOURCE=2
LDLIBS = -lcrypto -lm
all: void_bench_ingest
void_bench_ingest: void_bench_ingest.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
clean:
	rm -f void_bench_ingest
.PHONY: all clean
