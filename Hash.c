#include <linux/types.h>

#include "Log.h"
#include "Cypher.h"

__u64 hash_calculate(__u64 *a_message, __u32 a_size)
{
    __u64 current = 0;
    __u64 next = 0;
    __u32 i = 0;

    log("Block %i\n", i);
    log("\t hash is %llx", next);

    for (;i < a_size; ++i) {
        next = encrypt(a_message[i] ^ current, a_message[i]) ^ current;
        current = next;
        log("Block %i\n", i);
        log("\t hash is %llx", next);
    }
    return current;
}
