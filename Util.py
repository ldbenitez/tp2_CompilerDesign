#-*- coding: utf-8 -*-

class Grammar:

    def __init__(self):
        self.productions = []
        self.terminals = []
        self.non_terminals = []



class Production:

    def __init__(self):
        self.name = ""
        self.body = []
        self.first_set = []
        self.follow_set= []

    def __str__(self):
        return self.name