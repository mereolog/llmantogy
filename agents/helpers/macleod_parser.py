# This code is an adaptation of https://github.com/thahmann/macleod/


import logging
import re

import ply.lex as lex
import ply.yacc as yacc

from fol_logic.objects.atomic_formula import AtomicFormula
from fol_logic.objects.conjunction import Conjunction
from fol_logic.objects.disjunction import Disjunction
from fol_logic.objects.equivalence import Equivalence
from fol_logic.objects.implication import Implication
from fol_logic.objects.negation import Negation
from fol_logic.objects.predicate import Predicate
from fol_logic.objects.quantifying_formula import QuantifyingFormula, Quantifier
from fol_logic.objects.term import Term

LOGGER = logging.getLogger(__name__)

global parser


class ParseError(Exception):
    pass


tokens = [
    "LPAREN",
    "RPAREN",
    "URI",
    "NONLOGICAL",
    "COMMENT",
    "QUOTED_STRING",
    "NAME_STRING"
]

# Adding new CL keywords, but all with colons are not yet processed
reserved = {
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'exists': 'EXISTS',
    'forall': 'FORALL',
    'iff': 'IFF',
    'if': 'IF',
    "=": 'SET'
}

tokens += reserved.values()

precedence = [['left', 'IFF'],
              ['left', 'IF']]

t_COMMENT = r'\/\*["\w\W\d*]+?\*\/'
t_QUOTED_STRING = r"'[\w\s.\-\+\*:,\(\)<=>;]+?'"
t_NAME_STRING = r"\"[\w\s.\-\+\*:,\(\)<=>;]+?\""
t_ignore = ' \t\r\n\f\v'

literals = ['(', ')']


def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'  # Set token type to the expected literal
    return t


def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'  # Set token type to the expected literal
    return t


def t_URI(t):
    r"http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\=\?\/\%\-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return t


def t_NONLOGICAL(t):
    r'[<>=\w\-\:\+_=]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Unknown character \"{}\"".format(t.value[0]))
    t.lexer.skip(1)


def p_statement(p):
    """
    statement : axiom statement
    statement : axiom
    """
    
    if len(p) == 3:
        
        statements = [p[1]]
        
        if isinstance(p[2], list):
            statements += p[2]
        else:
            statements.append(p[2])
        
        p[0] = statements
    
    else:
        
        p[0] = [p[1]]


def p_axiom(p):
    """
    axiom : negation
          | universal
          | existential
          | conjunction
          | disjunction
          | implication
          | biconditional
          | predicate
    """
    
    p[0] = p[1]


def p_base_axiom(p):
    """
    base_axiom : negation
        | universal
        | existential
        | conjunction
        | disjunction
        | implication
        | biconditional
        | predicate
    """
    
    p[0] = p[1]


def p_negation(p):
    """
    negation : LPAREN NOT axiom RPAREN
    """
    
    p[0] = Negation(arguments=[p[3]])


def p_conjunction(p):
    """
    conjunction : LPAREN AND axiom_list RPAREN
    """
    
    p[0] = Conjunction(p[3])


def p_conjunction_error(p):
    """
    conjunction : LPAREN AND error
    """
    
    raise TypeError("Error in conjunction: bad formula")


def p_disjunction(p):
    """
    disjunction : LPAREN OR axiom_list RPAREN
    """
    
    p[0] = Disjunction(p[3])


def p_disjunction_error(p):
    """
    disjunction : LPAREN OR error
    """
    
    raise TypeError("Error in disjunction: bad formula")


def p_axiom_list(p):
    """
    axiom_list : axiom axiom_list
    axiom_list : axiom
    """
    
    if len(p) == 3:
        
        axioms = [p[1]]
        
        if isinstance(p[2], list):
            axioms += p[2]
        else:
            axioms.append(p[2])
        
        p[0] = axioms
    
    else:
        
        p[0] = [p[1]]


def p_implication(p):
    """
    implication : LPAREN IF axiom axiom RPAREN
    """
    
    p[0] = Implication([p[3], p[4]])

def p_implication_error(p):
    """
    implication : LPAREN IF error
    implication : LPAREN IF axiom error
    """
    
    if is_error(p.slice[3]):
        raise TypeError("Error in implication: bad first formula")
    
    raise TypeError("Error in implication: bad second formula")


def p_biconditional(p):
    """
    biconditional : LPAREN IFF axiom axiom RPAREN
    """
    
    if (len(p) == 7):
        p[0] = Equivalence([p[4], p[5]])
    else:
        p[0] = Equivalence([p[3], p[4]])


def p_biconditional_error(p):
    """
    biconditional : LPAREN IFF error
    biconditional : LPAREN IFF axiom error
    """
    
    if is_error(p.slice[3]):
        raise TypeError("Error in biconditional: bad first formula")
    
    raise TypeError("Error in biconditional: bad second formula")


def p_existential(p):
    """
    existential : LPAREN EXISTS LPAREN nonlogicals RPAREN axiom RPAREN
    """
    
    p[0] = QuantifyingFormula(variables=p[4], quantified_formula=p[6], quantifier=Quantifier.EXISTENTIAL)


def p_existential_error(p):
    """
    existential : LPAREN EXISTS LPAREN error
    existential : LPAREN EXISTS LPAREN nonlogicals RPAREN error
    """
    
    if is_error(p.slice[4]):
        raise TypeError("Error in existential: bad nested formula " + p.slice[4])
    
    raise TypeError("Error in existential: bad formula")


def p_universal(p):
    """
    universal : LPAREN FORALL LPAREN nonlogicals RPAREN axiom RPAREN
    """
    
    p[0] = QuantifyingFormula(variables=p[4], quantified_formula=p[6], quantifier=Quantifier.UNIVERSAL)


def p_universal_error(p):
    """
    universal : LPAREN FORALL LPAREN nonlogicals RPAREN error axiom RPAREN
              | LPAREN FORALL LPAREN nonlogicals RPAREN error RPAREN
              | LPAREN FORALL LPAREN nonlogicals RPAREN axiom error RPAREN
              | LPAREN FORALL error LPAREN nonlogicals RPAREN error axiom RPAREN
    """
    
    raise ParseError("Error parsing term in Universal")



def p_predicate(p):
    """
    predicate : LPAREN NONLOGICAL parameter RPAREN
    predicate : LPAREN NAME_STRING parameter RPAREN
    predicate : LPAREN SET parameter RPAREN
    """

    p[0] = AtomicFormula(Predicate(origin_value=p[2], arity=len(p[3])), arguments=p[3])


def p_predicate_error(p):
    """
    predicate : LPAREN NONLOGICAL error RPAREN
    """
    
    raise TypeError("Error in predicate: bad term (variable or functional term) inside")


def p_parameter(p):
    """
    parameter : function parameter
    parameter : nonlogicals parameter
    parameter : function
    parameter : nonlogicals
    """
    
    if len(p) == 3:
        if isinstance(p[1], list):
            parameters = [Term(origin_value=parameter) for parameter in p[1]]
            if isinstance(p[2], list):
                parameters += [Term(origin_value=parameter) for parameter in p[2]]
            else:
                parameters.append(Term(origin_value=p[2]))
        else:
            parameters = [Term(origin_value=p[1])]
            if isinstance(p[2], list):
                parameters += [Term(origin_value=parameter) for parameter in p[2]]
            else:
                parameters.append(Term(origin_value=p[2]))
        
        p[0] = parameters
    
    else:
        
        if isinstance(p[1], list):
            p[0] = [Term(origin_value=parameter) for parameter in p[1]]
        else:
            p[0] = [Term(origin_value=p[1])]


def p_function(p):
    """
    function : LPAREN NONLOGICAL parameter RPAREN
    """
    
    p[0] = AtomicFormula(predicate=Predicate(origin_value=p[2], arity=len(p[3])), arguments=p[3])


def p_function_error(p):
    """
    function : LPAREN NONLOGICAL error RPAREN
    """
    
    raise TypeError("Error in function: bad nested term")


def p_nonlogicals(p):
    """
    nonlogicals : NONLOGICAL nonlogicals
    nonlogicals : NONLOGICAL
    """
    
    if len(p) == 3:
        
        nonlogicals = [p[1]]
        
        if isinstance(p[2], list):
            nonlogicals += p[2]
        else:
            nonlogicals.append(p[2])
        
        p[0] = nonlogicals
    
    else:
        p[0] = [p[1]]


def p_error(p):
    global parser
    
    if p is None:
        raise TypeError("Unexpectedly reached end of file (EOF)")
    
    # Note the location of the error before trying to lookahead
    error_pos = p.lexpos
    
    # A little stack manipulation here to get everything we need
    stack = [symbol for symbol in parser.symstack][1:]
    
    index_current_axiom = next((stack.index(x) for x in stack[::-1] if x.type == 'axiom'), len(stack))
    current_axiom = stack[index_current_axiom:]
    current_axiom.append(p)
    
    # Use the brace level to figure out how many future tokens we need to complete the error token
    lparens = len([x for x in current_axiom if x.type == "LPAREN"])
    lookahead_tokens = []
    while lparens != 0:
        lookahead_token = parser.token()
        if lookahead_token is None:
            break
        else:
            lookahead_tokens.append(lookahead_token)
            if lookahead_token.type == "RPAREN":
                lparens -= 1
            elif lookahead_token.type == "LPAREN":
                lparens += 1
    
    # Put together a full list of tokens for the error token
    current_axiom += lookahead_tokens
    
    # String manipulation to "underbar" the error token
    axiom_string = []
    overbar_error = ''.join([x + '\u0332' for x in p.value])
    p.value = overbar_error
    
    for token in current_axiom:
        raw_token = token.value
        if isinstance(raw_token, str):
            axiom_string.append(raw_token + ' ')
        elif isinstance(raw_token, list):
            for sub_token in raw_token:
                axiom_string.append(sub_token + ' ')
    
    string_up_to_error = p.lexer.lexdata[:error_pos]
    types = [symbol.type for symbol in stack]
    # logging.getLogger(__name__).error()
    print("""Error at line {}! in: {}""".format(
        string_up_to_error.count("\n"),
        p.lexer.lexdata))
    
    print("""Unexpected Token: '{}' :: "{}"\n{}""".format(
        p.value,
        ''.join(axiom_string),
        ' '.join(types)))
    
    raise TypeError("Unexpected Token")


def parse_clif(clif_text: str):
    """
    This modifies parser.py file from macleod
    """
    global parser
    global conditionals
    
    lex.lex(reflags=re.UNICODE)
    parser = yacc.yacc()
    clif_axioms = yacc.parse(clif_text)
    for clif_axiom in clif_axioms:
        clif_axiom.is_self_standing = True
    return clif_axioms


def get_line_number(string, pos):
    return string[:pos].count('\n') + 1


def is_error(obj):
    return isinstance(obj, yacc.YaccSymbol) and obj.type == "error"


