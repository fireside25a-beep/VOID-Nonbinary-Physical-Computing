#ifndef VOID_BATCH_API_H
#define VOID_BATCH_API_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
int void_batch_cycle_init(void);
int void_batch_cycle_step(int selection, int epoch, int64_t *digest);
#ifdef __cplusplus
}
#endif
#endif
