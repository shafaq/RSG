import unittest
from rsg import GrammarParser


class GrammarParserTest(unittest.TestCase):


    def test_prepare_expansion(self):

        parsing_grammar = { "nonterminal_start": r'<',
                        "nonterminal_end"   : r'>',
                        "production_end"   : r';' 
                        }

        p = GrammarParser(parsing_grammar)

        nt = [ "<verb>","dance    ;", "cry;", "code   ;"]
        
        self.assertEqual(p.prepare_expansion(nt),{"verb":["dance", "cry" , "code"]})                    
    
    def test_load_grammar_poem(self):

        poem = """ The poem grammar. This is the same simple grammar discussed in the assignment handout.  It is a good one to test one since it is so small.

        {
        <start>
        The   <object>   <verb>   tonight.  ;
        }

        There can be any amount of white space in between the words in a production and before and after the terminating semi-colon.  Be sure you skip over extra white space.
        {
        <object>
        waves   ;             
        big    yellow       flowers ;          
        slugs   ;
        }

        {
        <verb>
        sigh <adverb>   ;
        portend like <object>   ;
        die <adverb>    ;        
        }

        Outside of the braces, there can be any kind of text; for comments, diagrams, etc.  You should skip over all this junk and just get on to reading the next nonterminal definition.

        {
        <adverb>
        warily  ;
        grumpily    ;
        }
        """
        parsing_grammar = { "expansion_start"  : r'^{',
                            "expansion_end"    : r'}$',
                            "nonterminal_start": r'<',
                            "nonterminal_end"   : r'>',
                            "nonterminal"      : r'<.+>', 
                            "production"       : r'.*;$',
                            "text"             : r'.+',
                            "production_end"   : r';' 
                            }
        parser = GrammarParser(parsing_grammar, grammar_string= poem)                    
        result = {"start":["The <object> <verb> tonight."],
                 "object":["waves","big yellow flowers", "slugs"],
                 "verb": ["sigh <adverb>" ,"portend like <object>", "die <adverb>"],
                 "adverb": ["warily", "grumpily"]
                  }

        self.assertEqual(parser.load_grammar(),result)
    

if __name__ == "__main__":
    unittest.main()

