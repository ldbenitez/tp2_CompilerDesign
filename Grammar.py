#-*- coding: utf-8 -*-

from Production import Production


class Grammar:

    def __init__(self):
        self.productions = []
        self.terminals = []
        self.non_terminals = []
        self.initial = ""

    def init_grammar(self, filepath):
        flag = 0
        with open(filepath, 'r') as grammar_input:

            for line in grammar_input:
                print line
                tmp_split = line.rsplit("->", 1)
                left_part = tmp_split[0].replace("\n", "").strip()

                if flag == 0:
                    self.initial = left_part.replace("\n", "").strip()
                    flag = 1

                right_part = tmp_split[1].rsplit("|")

                self.non_terminals.append(left_part.strip())

                for item in right_part:

                    production = Production()

                    each_right_part = item.split(",")

                    for subitem in each_right_part:
                        production.body.append(subitem.replace("\n", "").strip())
                        production.name = left_part.strip()

                    self.productions.append(production)

            for p in self.productions:
                for item in p.body:
                    if(item not in self.non_terminals) and (item not in self.terminals) and (item != '@'):
                        self.terminals.append(item)

    def get_production(self, production_name):

        result = []
        for p in self.productions:
            if p.name == production_name:
                result.append(p)

        return result

    def get_join_production(self, prod_name):
        new_production = Production()

        productions = self.get_production(prod_name)

        new_production.name = prod_name
        for p in productions:
            p.define_first_set(self)
            new_production.first_union(p.first_set)
            new_production.follow_union(p.follow_set)

        return new_production

    def define_first_sets(self):
        for p in self.productions:
            p.define_first_set(self)

    def define_follow_sets(self):
        for p in self.productions:
            p.define_follow_set(self)

    def get_next_symbols(self, prod_name):

        result = []

        for p in self.productions:
            if prod_name in p.body:
                index = p.body.index(prod_name)
                if index == len(p.body) - 1:
                    result.append([p.name, '@'])
                else:
                    result.append([p.name, p.body[index+1]])

        return result

    def add_to_follow_sets(self, name, token_list):
        for p in self.get_production(name):
            for token in token_list:
                if (token not in p.follow_set) and (token != '@'):
                    p.follow_set.append(token)
