#include <stdio.h>
#include <linux/types.h>
#include "python2.7/Python.h"

#include "Cypher.h"
#include "Hash.h"
#include "Log.h"

static __u64 wrap_hash_calculate(void)
{
    __u64 input = 0;
    input += 0x61ull << 56;
    input += 0x62ull << 48;
    input += 0x63ull << 40;
    input += 0x64ull << 32;
    input += 0x65ull << 24;
    input += 0x66ull << 16;
    input += 0x68ull << 8;
    input += 0x0Aull;

    __u64 input2[2] = {0, 0};
    input2[0] = input;
    input2[1] = 1ll<<63;
    __u64 key = input;
    __u64 output = encrypt(input, key);

    log("\nResults:%s\n", "");
    log_hexlong(input);
    log_hexlong(key);
    log_hexlong(output);

    output = hash_calculate(input2, 2);

    log_hexlong(output);

    return output;
}

static PyObject* py_hash_calc(PyObject* self, PyObject* args)
{
    __u64 out = wrap_hash_calculate();
    return Py_BuildValue("K", out);
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef hash_methods[] = {
  {"get_hash", py_hash_calc, METH_VARARGS, "Calculate hash!"},
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
PyMODINIT_FUNC inithashModule(void)
{
  (void) Py_InitModule("hashModule", hash_methods);
}
