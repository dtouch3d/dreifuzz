#!/bin/python2

import sys
import random
import mmap
import shutil
import os
import hashlib
import argparse

from pydbg import *
from pydbg.defines import *
import utils
import os.path


""" Randomly replaces bytes in the file"""


def bytefiddle(parent_file):
    sz = os.path.getsize(parent_file)
    offset = [random.randint(10, sz-1) for i in range(int(0.1 * sz))]
    print "offset len: %s" % len(offset)
    name, ext = os.path.splitext(parent_file)
    mutf = hashlib.sha1(str(random.random())).hexdigest() + ext
    shutil.copy(parent_file, mutf)

    with open(mutf, 'r+b') as fuzzfile:

        mm = mmap.mmap(fuzzfile.fileno(), 0)

        for off in offset:
            mm[off] = chr(random.randint(0, 255))

        mm.close()
    return mutf

def check_accessv(dbg):
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print crash_bin.crash_synopsis()
    input()
    return DBG_EXCEPTION_NOT_HANDLED


def main():
    print("[+] dreifuzz says Hallo!")

    app = sys.argv[-1]
    print("[+] File fuzzing program %s" % app)
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', store='indir', help='directory containing files to fuzz')
    args = parser.parse_args()

    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
        	log = open(os.path.join(root, f),'r')
		print("[+] Mutating file %s" % f)
		dbg = pydbg()

		mutated_file = bytefiddle(f)
		print("[+] Mutated file: %s" % mutated_file)

		dbg.load(app, mutated_file)
		dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, check_accessv)

		dbg.run()

if __name__ == "__main__":
    sys.exit(main())
