#-*- coding: utf-8 -*-

from Grammar import Grammar


def main():
    grammar = Grammar()
    production = None
    input_list = []

    grammar.init_grammar("grammar_input_example.txt")
    print "Non Terminals: " + grammar.non_terminals.__str__()
    print "Terminals:" + grammar.terminals.__str__()

    grammar.define_first_sets()
    grammar.define_follow_sets()

    print "First Set: \n\t" + grammar.get_first_sets().__str__()
    print "Follow Set: \n\t" + grammar.get_follow_sets().__str__()

if __name__ == "__main__":
    main()