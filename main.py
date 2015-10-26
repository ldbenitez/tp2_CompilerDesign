#-*- coding: utf-8 -*-

from Util import Grammar,Production

def main():
    grammar = Grammar()
    production = Production()
    with open("grammar_example_input.txt",'r') as grammar_input:
        print grammar_input.read()


if __name__=="__main__":
    main()