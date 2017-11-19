import re
import sys

compiled = []

ignored_chars = ['\n', '\r', '\t', ' ']

letters = 'abcdefhijklmnopqrstuvwxyzABCDEFGIHKJKLMNOPQRSTUVXYZ'
digits = '0123456789'

t = {
    'int'           : 2,
    'float'         : 3,
    'char'          : 4,
    'cin'           : 5,
    'cout'          : 6,
    'if'            : 7,
    'while'         : 8,
    'else'          : 9,
    '/'             : 12,
    '*'             : 13,
    '<'             : 14,
    '>'             : 15,
    '<='            : 16,
    '>='            : 17,
    '='             : 18,
    '=='            : 19,
    '!='            : 20,
    '{'             : 21,
    '}'             : 22,
    ';'             : 23,
    '.'             : 24,
    '('             : 25,
    ')'             : 26,
    '>>'            : 27,
    '<<'            : 28,
    'struct'        : 29,
    'main'          : 30,
    '<iostream.h>'  : 31,
    'return'        : 32,
    '#include'      : 33,
    'using'         : 34,
    'namespace'     : 35,
    'std'           : 36,
    'const'         : 37,
}

t_names = [
    'identifier',
    'constant',
    'int',
    'float',
    'char' ,
    'cin' ,
    'cout',
    'if',
    'while',
    'else',
    '+',
    '-',
    '/',
    '*',
    '<',
    '>',
    '<=',
    '>=',
    '=',
    '==',
    '!=',
    '{',
    '}',
    ';',
    '.',
    '(',
    ')',
    '>>',
    '<<',
    'struct',
    'function',
    'directive',
    'return',
    'include',
    'using',
    'namespace',
    'std',
    'const',
]

special_t = {
    '+'             : 10,
    '-'             : 11,
}


class SymbolTable:
    '''
    The symbol table
    '''
    def __init__(self):
        """
        Initialization of the symbol table
        """
        self._table = []


    def insert(self, var_name):
        """
        Inserts and sorts the table, parameters: var_name - identifier or constant
        """
        if self.exists(var_name):
            return
        self._table.append(str(var_name))
        self._table = sorted(self._table)


    def exists(self, var_name):
        """
        Checks wheter an identifier or a constant already exists in the symbol table
        Returns true if it exists or false if not
        """
        try:
            self._table.index(var_name)
            return True
        except ValueError:
            return False


    def get_table(self):
        """
        Get the table list
        """
        return self._table


    def get_position(self, value):
        """
        Get the position in the table of an identifier or a constant.
        Used for matching in pif
        """
        return self._table.index(value)


class Scanner:
    def __init__(self, constants_automata, identifiers_automata):
        self.symbol_table = SymbolTable()
        self.constants_automata = constants_automata
        self.identifiers_automata = identifiers_automata

    def get_next_important_char(self, text, pos):
        """
        Checks the input from a position and searches for the next meaningful character
        params: text - the text to search in
        pos - the current position to start from
        returns: the position of the next meaningful character
        """
        while pos < len(text) and text[pos] in ignored_chars:
            pos += 1
        return pos


    def print_error(self, text, pos, message):
        """
        Prints the error and exists the program
        params: text - the input text
        pos - the position where the error starts
        message - the error message to print
        """
        bg_line = pos
        ed_line = pos
        tabs = 0
        while bg_line >= 0 and text[bg_line] != '\n':
            if text[bg_line] == '\t':
                tabs += 1
            bg_line -= 1
        while ed_line < len(text) and text[ed_line] != '\n':
            ed_line += 1
        err =  'Error: on line\n%s\n' % text[bg_line + 1 : ed_line]
        err += '\t' * tabs  + ' ' * (pos - bg_line - 1 - tabs) + '^\n'
        err += '%s' % message
        print err
        sys.exit(-1)


    def is_identifier(self, text, pos):
        """
        Checks whether the text starting from a position is an identifier or not
        params: text - the input text
        pos - the position to start searching
        returns: a tuple
        if it is an identifer: (the identifier detected, True)
        if it is not :         (False, error_message)
        """
        pos_init = pos
        validated_text, raw_text = self.identifiers_automata.longest_prefix(text, pos)
        if validated_text == '':
            return False, 'Invalid character'
        if len(validated_text) >= 250:
            return False, 'Identifier is too long'
        return validated_text, True



    def is_constant(self, text, pos, binary):
        """
        Checks whether a constant is located starting from a position in the input text
        params: text - the input text
        pos - the position to start searching
        returns: a tuple
        if it is a constant: (the constant detected, True)
        if not a constant: (False, error message)
        """


        if text[pos] == '\'' and text[pos+1] in letters + digits and text[pos + 2] == '\'':
            return text[pos: pos + 3], True
        elif text[pos] not in digits and text[pos] not in '+-':
            return False, 'Does not look like a constant'
        init_pos = pos
        if not binary and text[pos] in '+-' and text[pos+1] not in digits:
            return False, 'After unary operator only digits are allowed'
        if text[pos] in '+-' and text[pos+1] in digits and binary:
            return False, 'Not a unary operator'
        if text[pos] == '0' and text[pos+1] in digits:
            return False, 'Cannot have 0 and then another digit after it'
        validated_text, raw_text = self.constants_automata.longest_prefix(text, pos)
        if text[pos + len(validated_text)] in letters:
            return False, 'Cannot have letters at the end of a constant'
        if validated_text == '':
            return False, 'No constant identified'
        return validated_text, True


    def lexical_validation(self, text):
        """
        Checks the input text and checks it for lexical errors
        params: text - the input text

        returns:
        fixed_tokens -> the tokens identified, if a token is an identifier or a constant, then the position in the symbol table will also be provided
        sym_table -> the symbol table
        str_tokens -> the tokens in a more readable way
        """

        pos = self.get_next_important_char(text, 0)
        pif = []
        tokens = []

        sorted_tokens = sorted(t.items(), key=lambda v: len(v[0]), reverse=True)

        while pos < len(text):
            found_token = False
            for crt_token in sorted_tokens:
                if text[pos : pos + len(crt_token[0])] == crt_token[0]:
                    tokens += [crt_token[1]]
                    pos += len(crt_token[0])
                    found_token = True
                    break
            if found_token:
                pos = self.get_next_important_char(text, pos)
                continue
            else:
                identifier = self.is_identifier(text, pos)
                binary = True if isinstance(tokens[-1], tuple) and tokens[-1][0] in [0, 1] else False
                constant = self.is_constant(text, pos, binary)
                if not identifier[0] and not constant[0]:
                    if binary and text[pos] in '+-':
                        tokens += [special_t[text[pos]]]
                        pos += 1
                    else:
                        if text[pos] in digits + '-+':
                            self.print_error(text, pos, constant[1])
                        elif text[pos] in letters:
                            self.print_error(text, pos, identifier[1])
                        else:
                            self.print_error(text, pos, identifier[1])
                elif identifier[0]:
                    self.symbol_table.insert(identifier[0])
                    pos += len(identifier[0])
                    tokens += [(0, identifier[0])]
                elif constant[0]:
                    if len(constant[0]):
                        self.symbol_table.insert(constant[0])
                    else:
                        self.print_error(text, pos, 'Invalid constant!')
                    pos += len(constant[0])
                    tokens += [(1, constant[0])]
                pos = self.get_next_important_char(text, pos)

        fixed_tokens = []
        str_tokens = []
        for token in tokens:
            if isinstance(token, tuple):
                fixed_tokens.append((token[0], self.symbol_table.get_position(token[1])))
                str_tokens.append(str(t_names[token[0]]) + '->' + str(fixed_tokens[-1][1]))
            else:
                fixed_tokens.append(token)
                str_tokens.append(t_names[token])

        return fixed_tokens, self.symbol_table.get_table(), str_tokens




