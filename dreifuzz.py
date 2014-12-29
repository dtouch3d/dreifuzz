#!/usr/bin/python2

import sys
import random
import mmap
import shutil
import os
import hashlib
import os.path

sys.path.append("./vivisect")

import vtrace
import vdb


""" Randomly replaces bytes in the file"""


def bytefiddle(parent_file):
    sz = os.path.getsize(parent_file)
    offset = [random.randint(10, sz-1) for i in range(int(0.1 * sz))]
    print("offset len: %s" % len(offset))
    name, ext = os.path.splitext(parent_file)
    mutf = hashlib.sha1(str(random.random())).hexdigest() + ext
    shutil.copy(parent_file, mutf)

    with open(mutf, 'r+b') as fuzzfile:

        mm = mmap.mmap(fuzzfile.fileno(), 0)

        for off in offset:
            mm[off] = chr(random.randint(0, 255))

        mm.close()
    return mutf


def load_binary(trace, exepath, filepath):
    cmdline = exepath + " " + filepath
    trace.execute(cmdline)

    print("Executing: %s") % (cmdline)
    trace.run()

def check_accessv(dbg):
    return


def main():
    if len(sys.argv) < 3:
        print("dreifuzz -- a effortlessly uncomplicated fuzzer\n"
                "usage: ./dreifuzz.py [executable] [file]")
        return

    exepath = sys.argv[1]
    filepath = sys.argv[2]

    trace = vtrace.getTrace()

    load_binary(trace, exepath, filepath)

if __name__ == "__main__":
    sys.exit(main())
