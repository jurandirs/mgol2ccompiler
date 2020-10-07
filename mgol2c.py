#!/usr/bin/env python3
import argparse
from scanners.dfa import DFA
from symbol_table import SymbolTable

def read_mgol_code(file_name):
    codeinlist = [[]]
    with open(file_name,'r') as F:
        code = F.read()
        code = mgol_replaces(code)
        return [line.split() for line in code.split('\n')]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Projeto de compilador que converte código em linguagem Mgol em arquivo objeto em C.")
    parser.add_argument("--source", type=str, help="the path to source file with Mgol code.")
    args = parser.parse_args()

    mgol_code = read_mgol_code(args.source)
    print(*mgol_code,sep="\n")

    symbol_table = 


