#!/usr/bin/env python3

import os
import sys

benchmarks = ['fibonacci.min', 'primes.min', 'break.min', 'error_checking.min' ]


import re

def compare(text1, text2):
    text1 = re.sub(r'\s+', ' ', text1).strip()
    text2 = re.sub(r'\s+', ' ', text2).strip()

    if (text1 == text2):
        return True
    return False

def main(folders):
    print(folders)
    cwd = os.getcwd()
    
    all_score = []
    for folder in folders:
        os.chdir(folder)
        if os.path.exists('miniL'):
            os.remove('miniL')
        os.system('make')
        out = ""
        if os.path.exists('miniL'):
            out += ",1 "
        else:
            out += ",0 "
        
        if os.path.exists('../curr.out'):
            os.remove('../curr.out')
        for b in benchmarks:
            os.system('./miniL < ../testdir/' + b + ' > ../curr.out')
            with open('../curr.out', 'r') as f1:
                with open('../testdir/' + b+'.out', 'r') as f2:
                    if compare(f1.read(), f2.read()):
                        out += ",1 "
                    else:
                        os.system('code -d ../curr.out ../testdir/' + b + '.out')
                        if input("Score> ") == '1':
                            out += ",1 "
                        else:
                            out += ",0 "
        print(out)
        all_score.append(folder+out)
        os.chdir(cwd)
        with open('score.csv', 'w') as f:
            for s in all_score:
                f.write(s + '\n')
        
if __name__ == '__main__':
    # list all folders in the current directory
    folders = [f.path for f in os.scandir(os.getcwd()) 
                      if f.is_dir() and 
                         os.path.exists(os.path.join(f.path, 'Makefile')) ]
    if len(sys.argv) <= 1:
        main(folders)
    else:
        folders = [os.path.abspath(f) for f in sys.argv[1:]]
        main(folders)
