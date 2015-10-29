#-*- coding: utf-8 -*-

from Grammar import Grammar
from texttable import Texttable
"""Convension para valor en una celda especifica en la tabla
    de parsing """
VACIO = -1
SYNC = -2

def main():
    keep_enter = True
    grammar = Grammar()
    grammar.init_grammar("grammar_input_example2.txt")
    print "\nNon Terminals: " + grammar.non_terminals.__str__()
    print "\nTerminals:" + grammar.terminals.__str__()

    grammar.define_first_sets()
    grammar.define_follow_sets()

    print "\nFirst and Follow Set of Productions:\n"
    print_table_first_follow_set(grammar)

    print "\nParse Table of the Grammar: \n"
    parse_table = build_parse_table(grammar)
    print_parse_table(parse_table,grammar)

    # while(keep_enter):
    #     input_string = raw_input("Enter the string to analize: ")
    #     print ll_parsing(parse_table,grammar,input_string)


# def ll_parsing(parse_table,grammar,input_string):
#     stack = []
#     stack.append(grammar.terminals[0].name)
#
#     #while the stack is not empty
#     while(stack):
#         x = stack.pop()
#         input_token = next_input_token(input_string,grammar)
#
#         if x in grammar.terminals or x is '$':
#             if x == input_token:
#                 read(input_token)
#             else:
#                 error()
#         else:
#             production = get entry of table with(X,input_token)
#             if production is '':
#                 error()
#             else
#                 push the right side of production in reverse order.
#     return ""



def build_parse_table(grammar):

    size_terminals = len(grammar.terminals)
    size_non_terminals = len(grammar.non_terminals)
    parse_table = [['' for i in range(size_terminals+1)] for j in range(size_non_terminals)]

    for production in grammar.productions:
        #print production.name
        index_production = grammar.productions.index(production)
        index_non_terminal = grammar.non_terminals.index(production.name)
        for terminal in production.first_set:
           #print terminal
           if terminal is not '@':
                index_terminal = grammar.terminals.index(terminal)
                insert_on_parse_table(parse_table,index_non_terminal,index_terminal,index_production)

        if '@' in production.first_set:
            for terminal in production.follow_set:
                if terminal is '$':
                    index_terminal = size_terminals
                else:
                    index_terminal = grammar.terminals.index(terminal)
                insert_on_parse_table(parse_table,index_non_terminal,index_terminal,index_production)


    return parse_table

def insert_on_parse_table(parse_table,index_nt,index_t,index_p):

    """ se presenta en el caso de que la gramatica es ambigua, si la gramatica es ambigua
         la tabla de parseo no tendra entradas simples, es decir que una celda en la tabla
         puede tener mas de una entrada.
    """
    if parse_table[index_nt][index_t] !='':
        list_tmp = []
        list_tmp.extend(parse_table[index_nt][index_t])
        list_tmp.append(index_p)
        parse_table[index_nt][index_t] = list_tmp
    else:
        parse_table[index_nt][index_t] = index_p

def print_parse_table(parse_table,grammar):

    table = Texttable()
    header = [' ']
    header.extend(grammar.terminals)
    header.append('$')
    numbers_columns = len(grammar.terminals)+2
    table.header(header)
    table.set_cols_align(['c' for i in range(numbers_columns)])
    table.set_cols_width([12 for i in range(numbers_columns)])

    index_tmp = 0
    for non_terminal in grammar.non_terminals:
        row = []
        row.append(non_terminal)
        row_parse_table = parse_table[index_tmp]
        for column in row_parse_table:
            if column is not '':
                production = grammar.productions[column]

                """ se presenta en el caso de que la gramatica es ambigua, si la gramatica es ambigua
                    la tabla de parseo no tendra entradas simples, es decir que una celda en la tabla
                    puede tener mas de una entrada.
                """
                if isinstance(production,list):
                    string_productions=""
                    for index in production:
                        string_productions +=grammar.productions[index].get_object_as_string()+"\n"
                    row.append(string_productions)
                else:
                    row.append(production.get_object_as_string())
            else:
                row.append('')
        index_tmp+=1
        table.add_row(row)

    s = table.draw()
    print s

def print_table_first_follow_set(grammar):
    table = Texttable()
    table.header([' ','First','Follow'])
    for production in grammar.productions:
        row = []
        row.append(production.name)
        row.append(production.first_set)
        row.append(production.follow_set)
        table.add_row(row)
    s = table.draw()
    print s

if __name__ == "__main__":
    main()