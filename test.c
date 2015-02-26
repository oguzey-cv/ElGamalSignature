#include <stdio.h>
#include <linux/types.h>
#include "python2.7/Python.h"
#include <errno.h>

#include "Cypher.h"
#include "Hash.h"
#include "Log.h"

static size_t read_data(char **buff, const char *a_path)
{
    FILE *file = NULL;
    size_t size = 0;
    char *data = NULL;
    int i, c;

    if ((file = fopen(a_path, "r")) == NULL) {
        printf("Could not open file '%s'. Reason is '%d'", a_path, errno);
        goto fail;
    }

    while (fgetc(file) != EOF) {
        size++;
    }
    fseek(file, 0, SEEK_SET);
    printf("Will read %d bytes\n", size);
    data = malloc(size);
    memset(data, 0, size);
    i = 0;
    while ((c = fgetc(file)) != EOF) {
        data[i++] = c;
    }
    *buff = data;

fail:
    fclose(file);
    return size;
}

void main (void)
{
    char * data = NULL;
    size_t size = read_data(&data, "./test2");
    size_t amount = size;
    if (size % 16 != 0) {
        amount = (size / 16);
        if (amount % 2 == 0) {
            amount = amount * 2 + 2;
        } else {
            amount = amount * 2 + 1;
        }
    }
    log("input size is %d\n", size);
    log("pad size is %d\n", amount* 8 - size);
    log("size numbers is %d\n", amount);
    __u64 *numbers = malloc(sizeof(__u64) * amount);
    memset(numbers, 0, sizeof(__u64) * amount);

    size_t i = 0, k = 0;

    for (i = 0; i < amount; ++i) {
        __u64 tmp;
        for (k = i * 8; k <(i + 1)*8 && k < size; ++k) {
            tmp = data[k];
            tmp <<= (7 - k % 8) * 8;
            numbers[i] += tmp;
        }

        if (k == size && k != (i + 1)*8 ) {
            tmp = 0x80;
            tmp <<= (7 - k % 8) * 8;
            numbers[i] += tmp;
            break;
        }
    }
    free(data);
    return numbers;
}
