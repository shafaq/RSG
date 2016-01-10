import sys
import re
from random import randint
import utility


class CFG(object):
    """ Datastructure for holding the grammar and generating expansions.

    Class CFG has an internal datastructure for context free grammar.
    It gets initialized with a grammar passed to it in __init__ method.
    On generate() it generates a random expansion of the grammar.

    """
    
    def __init__(self, nonterminal_start, nonterminal_end, cfgGrammar):
        """ Inititalize the CFG instance. 

        The method takes three arguments:
        nonterminal_start -- the starting delimiter of the non terminal
        nonterminal_end -- the ending delimiter of the non terminal
        cfgGrammar -- recieves a grammar as dictionary object. Program exits 
        if not not provided
        """
        if not cfgGrammar:
            print "Grammar not provided."
            sys.exit(0) 
        self.grammar = cfgGrammar
        self.nonterminal_start = nonterminal_start
        self.nonterminal_end = nonterminal_end
        utility.debug_print(self.grammar, "grammar")
    
    def __str__(self):
        """ Return the string representation of the grammar."""

        string_representation = ""
        for k in sorted(self.grammar.keys()):
            string_representation += "{0} : {1}\n".format(k, self.grammar[k])
        return string_representation
    
    def generate(self):
        """ Generate the expansion of the context free grammar.

        Under the hood it starts from the <start> nonterminal and returns the
        expansion. A production is chosen randomly from the multiproduction
        non terminal. 
        """

        utility.debug_print(self.grammar["start"][0], "start=")
        return self.__rgenerate(self.get_random_production("start"))
    
    def __rgenerate(self, production):
        pattern_string = (self.nonterminal_start +
                         '(?P<nonterminal>\\b.+?\\b)' +
                         self.nonterminal_end)
        utility.debug_print(pattern_string, "pattern")
        pattern_nt = re.compile(pattern_string)
        #find a match for a not terminal in the given production
        match = pattern_nt.search(production)
        matched_nonterminal = match.group('nonterminal')
        utility.debug_print(match.group('nonterminal'),
                           "matched non terminal = ")
        #get a random production for the matched non terminal
        substitution = self. get_random_production(matched_nonterminal)
        utility.debug_print(substitution, "substitution")
        #split the string around found non terminal
        lst = pattern_nt.split(production, 1)
        # substitute the random production for non terminal
        new_production = lst[0] + substitution + lst[2]
        utility.debug_print(new_production, "new_production")
        # if new production still has more non terminals
        if not pattern_nt.search(new_production):
            return new_production
        return self.__rgenerate(new_production)
    
    def get_random_production(self, key):
        """ Return a random production of the nonterminal passed.

        key -- nonterminal of which production one is chosen randomly
        """

        try:
            prod_lst_len = len(self.grammar[key])
        except KeyError:
            print "Could not find a non terminal in CFG. Exiting application"
            sys.exit(1)
        else:
            random_num = randint(0, prod_lst_len - 1)
            return self.grammar[key][random_num]


class GrammarParser(object):
    """ Parser the file/string to load grammar from it"""
    
    def __init__(self, parsing_rules,
                 grammar_filename=None,
                 grammar_string=None):
        """ Initialize a parser object with parsing rules, file/string to parse.

        parsing_rules -- a dictionary that describes how a file/string is to 
        be interpreted
        grammar_filename -- filename that contains the grammar as text
        grammar_string -- a string (mainly provided for testing) containing the grammar 
        """

        if not(grammar_filename or grammar_string):
            print "A filename or string containing grammar should be passed."
            sys.exit(1)

        self.parsing_rules = {x: re.compile(parsing_rules[x])
                            for x in parsing_rules.keys()}
        self.grammar_filename = grammar_filename
        self.grammar_string = grammar_string
    
    def remove_character(self, parsing_key, string):
        """ clean a string based on parsing rules.
        parsing_key -- a key into the parsing_rules to look for the regex
        string -- string to remove parsing key from

        """

        return self.parsing_rules[parsing_key].sub("", string)

    @staticmethod
    def remove_spaces(string):
        """ Remove extra spaces between words, at the end and start."""

        extra_spaces = re.compile(r'\s{2,}')
        end_space = re.compile(r'\s+[.!?]')
        end_space.sub("", string)
        return extra_spaces.sub(" ", string).strip()
    
    def load_grammar(self):
        """load the internal datasturcture (dict) for grammar from the
        file/string based on rules. Return the dict.
        """
        
        grammar = {}
        processing_expansion = False
        add_as_key = True
        nt = []
        prod = ""
        for l in self.read_next_line():
            #utility.debug_print(l , "line read")
            if not l: #empty line
                #utility.debug_print(l, "empty line")
                continue
            if self.parsing_rules["expansion_start"].match(l):
                #utility.debug_print(l, "expansion start matched")
                processing_expansion = True
                add_as_key = True
                continue
            if (self.parsing_rules["expansion_end"].match(l) and
               processing_expansion):
                #utility.debug_print(l, "expansion end matched")
                processing_expansion = False
                grammar.update(self.prepare_expansion(nt))
                nt = []
                continue
            if (self.parsing_rules["nonterminal"].match(l) and
                processing_expansion):
                if add_as_key:
                    #utility.debug_print(l, "not terminal matched as key")
                    add_as_key = False
                    nt.append(l)
                else:
                    prod = prod + l + " "
                    if  self.parsing_rules["production"].match(l):
                        #utility.debug_print(l, "production matched")
                        nt.append(prod.strip())
                        prod = ""
                continue
            if self.parsing_rules["text"].match(l) and processing_expansion:
                #utility.debug_print(l, "text matched")
                prod = prod + l + " "
                if  self.parsing_rules["production"].match(l):
                    #utility.debug_print(l, "production matched")
                    nt.append(prod.strip())
                    prod = ""
        return grammar
    
    def prepare_expansion(self, terminal_expansions):
        """ Take the nonterminal and its productions, cleanse and prepare
        the production as a dictionary key/value parsing_rules.

        terminal_expansion -- a list that gives the non terminal and its productions
        as read from the file/string to a dictionary key/value pair

        """
        nt_expansion = {}
        # remove '<'
        nonterminal_name = terminal_expansions[0]
        clean_terminal_name = self.remove_character("nonterminal_start",
                                                    nonterminal_name)
                                                            
        #remove '>'
        clean_terminal_name = self.remove_character("nonterminal_end",
                                                    clean_terminal_name)
        #remove extra white spaces and trailing spaces and ';'
        nt_expansion[clean_terminal_name] = [GrammarParser.remove_spaces(
                                            self.remove_character("production_end",
                                                                  e))
                                              for e in terminal_expansions[1:]
                                            ]
        return nt_expansion
    
    def read_next_line(self):
        """ Read a line from the file(preferably) or string"""

        if self.grammar_filename:
            with open(self.grammar_filename) as fd:
                for line in fd:
                    line = line.strip()
                    yield line
        else:
            for line in self.grammar_string.splitlines():
                yield line.strip()


def main(filename):
    parsing_grammar = {"expansion_start"  :r'^{',
                       "expansion_end"    :r'}$',
                       "nonterminal_start":r'<',
                       "nonterminal_end"   :r'>',
                       "nonterminal"      :r'<.+>',
                       "production"       :r'.*;$',
                       "text"             :r'.+',
                       "production_end"   :r';'}
    parser = GrammarParser(parsing_grammar, grammar_filename=filename)
    grammar = parser.load_grammar()
    cfg = CFG(parsing_grammar["nonterminal_start"],
           parsing_grammar["nonterminal_end"], grammar)
    generated_string = cfg.generate()
    print '\n\n' + utility.wrapped_text(generated_string) + '\n'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Grammar File Name not provided"
        print "usage:python rsg.py <grammar-file>"
        sys.exit(1)
    main(sys.argv[1])
