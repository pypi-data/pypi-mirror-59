#!/usr/bin/env python3
# coding: utf-8

from joker.stream.shell import ShellStream


def _minus(path1, path2):
    s1 = set(ShellStream(path1).dense())
    s2 = set(ShellStream(path2).dense())
    for x in s1 - s2:
        print(x)


def run(prog, args):
    _minus(args[0], args[1])
