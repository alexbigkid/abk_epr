#!/usr/bin/env python3

import os

class Phonebook:

    def __init__(self) -> None:
        self.numbers = {}
        self.filename = "phonebook.txt"
        self.cache = open(self.filename, "w")

    def add(self, name, number):
        self.numbers[name] = number

    def lookup(self, name):
        return self.numbers[name]

    def names(self):
        return set(self.numbers.keys())

    def clear(self):
        self.cache.close()
        os.remove(self.filename)
