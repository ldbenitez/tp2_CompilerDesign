# -*- coding: utf-8 -*-

from Grammar import Grammar
from texttable import Texttable
from Util import Stack

ERROR = -1
SYNC = -2

def main():

    exit = False
    exit2 = False

    while not exit:
        file_name = raw_input("\n>Where is the Grammar =) ?:  ")
        print "\nGrammar:"
        grammar = Grammar()
        grammar.init_grammar(file_name)
        print "\nNon Terminals: " + grammar.non_terminals.__str__()
        print "\nTerminals:" + grammar.terminals.__str__()

        grammar.define_first_sets()
        grammar.define_follow_sets()

        print "\nFirst and Follow Set of Productions:\n"
        print_table_first_follow_set(grammar)

        print "\nParse Table of the Grammar: \n"
        parse_table = build_parse_table(grammar)
        parse_table_with_sync_set(parse_table,grammar)
        is_ambiguous = print_parse_table(parse_table, grammar)

        if is_ambiguous:
            print "The Grammar is Ambiguous"
        else:
            print "The Grammar is not Ambiguous"

        while not exit2:
            input_string = raw_input("\nString to Analyze: ")
            if '$' in input_string:
                ll_parsing(parse_table, grammar, input_string)
            else:
                print "\nYou must enter the end of string character ($)"

            exit2 = raw_input("\nEnter another String to Analyze? ") != 'yes'

        exit = raw_input("\nEnter another Grammar? ") != 'yes'
        print "*"*100



def parse_table_with_sync_set(parse_table,grammar):

    for production in grammar.productions:
        follow_set_p = production.follow_set
        index_non_terminal = grammar.non_terminals.index(production.name)
        for item in follow_set_p:
            if item == '$':
                index_terminal = len(grammar.terminals)
            else:
                index_terminal = grammar.terminals.index(item)

            if parse_table[index_non_terminal][index_terminal] == ERROR:
                parse_table[index_non_terminal][index_terminal] = SYNC



def ll_parsing(parse_table, grammar, input_string):

    print "\nOutput: "
    input_symbols = input_string.split(",")
    stack = Stack()
    stack.push('$')
    stack.push(grammar.non_terminals[0])
    input_token = input_symbols[0]

    i = 0
    errors = []

    x = stack.peek()
    error = False
    while x is not '$':
        if x == input_token:
            print "MATCH " + input_token
            stack.pop()
            input_symbols.pop(0)
            input_token = str(input_symbols[0])
            i += 1
        elif x in grammar.terminals:
            print "Error in " + input_string
            errors.append(i)
            error = True
            break
        else:
            parse_table_entry = look_parse_table(parse_table, x, input_token,grammar)
            if parse_table_entry is ERROR:
                print "Error in " + input_token
                errors.append(i)
                error = True
                break
            elif parse_table_entry is SYNC:
                print "****Error in " + input_token
                errors.append(i)
                error = True
                stack.pop()
            else:
                production = grammar.productions[parse_table_entry]
                print production.get_object_as_string()
                stack.pop()
                if '@' not in production.body:
                    for item in reversed(production.body):
                        stack.push(item)
        x = stack.peek()


    if not error:
        print "\nSuccess"
    else:
        print "\nError"



def look_parse_table(parse_table, x, input_token, grammar):
    index_x = grammar.non_terminals.index(x)

    if input_token == '$':
        index_input_token = len(grammar.terminals)
    elif input_token in grammar.terminals:
        index_input_token = grammar.terminals.index(input_token)
    else:
        index_input_token=-1
    if index_x != -1 and index_input_token != -1:
         return parse_table[index_x][index_input_token]

    return ERROR


def build_parse_table(grammar):
    size_terminals = len(grammar.terminals)
    size_non_terminals = len(grammar.non_terminals)
    parse_table = [[ERROR for i in range(size_terminals + 1)] for j in range(size_non_terminals)]

    for production in grammar.productions:
        index_production = grammar.productions.index(production)
        index_non_terminal = grammar.non_terminals.index(production.name)
        for terminal in production.first_set:
            if terminal is not '@':
                index_terminal = grammar.terminals.index(terminal)
                insert_on_parse_table(parse_table, index_non_terminal, index_terminal, index_production)

        if '@' in production.first_set:
            for terminal in production.follow_set:
                if terminal is '$':
                    index_terminal = size_terminals
                else:
                    index_terminal = grammar.terminals.index(terminal)
                insert_on_parse_table(parse_table, index_non_terminal, index_terminal, index_production)

    return parse_table


def insert_on_parse_table(parse_table, index_nt, index_t, index_p):

    if parse_table[index_nt][index_t] != ERROR or parse_table[index_nt][index_t] is list:
        list_tmp = []
        list_tmp.append(parse_table[index_nt][index_t])
        list_tmp.append(index_p)
        parse_table[index_nt][index_t] = list_tmp
    else:
        parse_table[index_nt][index_t] = index_p


def print_parse_table(parse_table, grammar):
    table = Texttable()
    header = [' ']
    header.extend(grammar.terminals)
    header.append('$')
    numbers_columns = len(grammar.terminals) + 2
    table.header(header)
    table.set_cols_align(['c' for i in range(numbers_columns)])
    table.set_cols_width([12 for i in range(numbers_columns)])
    is_ambiguous = False
    index_row_tmp = 0
    for non_terminal in grammar.non_terminals:
        row = []
        row.append(non_terminal)
        row_parse_table = parse_table[index_row_tmp]
        index_column_tmp = 0
        for column in row_parse_table:
            if column is SYNC:
                row.append('synch')
            elif column is ERROR:
                row.append('err')
            else:
                production = grammar.productions[index_column_tmp]

                if isinstance(column, list):
                    is_ambiguous = True
                    string_productions = ""
                    for index in column:
                        string_productions += grammar.productions[index].get_object_as_string() + "\n"
                    row.append(string_productions)
                else:
                    row.append(production.get_object_as_string())
            index_column_tmp+=1

        index_row_tmp += 1
        table.add_row(row)

    s = table.draw()
    print s
    return is_ambiguous


def print_table_first_follow_set(grammar):
    table = Texttable()
    table.header([' ', 'First', 'Follow'])
    table.set_cols_align(['c','c','c'])
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
