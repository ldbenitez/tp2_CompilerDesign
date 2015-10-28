#-*- coding: utf-8 -*-


class Production:

    def __init__(self):
        self.name = ""
        self.body = []
        self.first_set = []
        self.follow_set = []

    def __str__(self):
        return self.name

    def first_union(self, f):
        for token in f:
            if token not in self.first_set:
                self.first_set.append(token)

    def follow_union(self, f):
        for token in f:
            if token not in self.follow_set:
                self.follow_set.append(token)

    def define_first_set(self, grammar):

        if not self.first_set:

            for token in self.body:
                if token in grammar.terminals:
                    self.first_union([token])
                    break

                elif token in grammar.non_terminals:

                    join_prod = grammar.get_join_production(token)

                    self.first_union(join_prod.first_set)

                    if '@' not in join_prod.first_set:
                        break

                elif token == '@':
                    self.first_set = ['@']
                    break

    def define_follow_set(self, grammar):
        if not self.follow_set:
            if self.name == grammar.initial:
                grammar.add_to_follow_sets(self.name, ['$'])

            next_symbols = grammar.get_next_symbols(self.name)

            for [prod_name, token] in next_symbols:

                if token in grammar.terminals:
                    grammar.add_to_follow_sets(self.name, [token])

                elif token in grammar.non_terminals:

                    join_prod = grammar.get_join_production(token)

                    grammar.add_to_follow_sets(self.name, join_prod.first_set)

                    if ('@' in join_prod.first_set) and (prod_name != self.name):
                        join_prod = grammar.get_join_production(prod_name)
                        grammar.add_to_follow_sets(self.name, join_prod.follow_set)

                elif (token == '@') and (prod_name != self.name):

                    join_prod = grammar.get_join_production(prod_name)
                    grammar.add_to_follow_sets(self.name, join_prod.follow_set)