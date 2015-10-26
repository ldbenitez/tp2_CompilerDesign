#-*- coding: utf-8 -*-

from Util import Grammar,Production

def main():
    grammar = Grammar()
    production = None
    with open("grammar_input_example.txt",'r') as grammar_input:
        for line in grammar_input:
            tmp_split = line.rsplit("->",1)
            left_part = tmp_split[0]
            right_part = tmp_split[1].rsplit("|",1)
            grammar.non_terminals.append(left_part.strip())
            for item in right_part:
                production = Production()
                each_right_part = item.split(",")
                for subitem in each_right_part:
                    production.body.append(subitem.replace("\n","").strip())
                    production.name = left_part.strip()
                grammar.productions.append(production)

        print grammar.non_terminals
        print grammar.productions[3].body

if __name__=="__main__":
    main()