#include <stdio.h>
#include <linux/types.h>

#include "Cypher.h"
#include "Hash.h"

#define log_hexlong(value)  printf("[%s]%s = %llx\n", __func__, #value, value)

int main (void)
{
    __u64 input = 0;
    input += 0x61ull << 56;
    input += 0x62ull << 48;
    input += 0x63ull << 40;
    input += 0x64ull << 32;
    input += 0x65ull << 24;
    input += 0x66ull << 16;
    input += 0x67ull << 8;
    input += 0x0Aull;

    __u64 key = input;
    __u64 output = encrypt(input, key);

    printf("\nResults:\n");
    log_hexlong(input);
    log_hexlong(key);
    log_hexlong(output);
    return 0;
}
