#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Projeto de compilador que converte código em linguagem Mgol em arquivo objeto em C.")
    parser.add_argument("source", type=str, help="the path to source file with Mgol code.")

    