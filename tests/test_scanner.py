import unittest

from lox.scanner import Scanner, Token, TokenType

class TestToken(unittest.TestCase):
    def test_should_correctly_store_information(self):
        token = Token(TokenType.LEFT_PAREN, '(', None, 1)
        self.assertEqual(str(token), "Token(LEFT_PAREN, (, None, 1)")

class TestScanner(unittest.TestCase):

    def runScanner(self, source):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        return [token.lexeme for token in tokens]

    def test_should_return_single_character_lexemes(self):
        sources = '(){},.-+;/*'
        for source in sources:
            self.assertEqual(self.runScanner(source), [source])

    def test_should_return_one_or_two_character_lexemes(self):
        sources = '!=<>'
        for source in sources:
            self.assertEqual(self.runScanner(source), [source])

        sources = ['!=', '==', '<=', '>=']
        for source in sources:
            self.assertEqual(self.runScanner(source),
                             [source])

    def test_should_ignore_comment_until_the_end_of_line(self):
        source = '// this is a comment'
        self.assertEqual(self.runScanner(source), [])

        source = '''// this is a comment
                 { }    !=
        '''
        self.assertEqual(self.runScanner(source), ['{', '}', '!='])

    def test_should_ignore_whitespace(self):
        source = '(          )'
        self.assertEqual(self.runScanner(source), ['(', ')'])

    def test_should_handle_free_form_code(self):
        source = '// this is a comment'
        self.assertEqual(self.runScanner(source), [])

        source = '(( )){} // grouping stuff'
        self.assertEqual(self.runScanner(source),
                         ['(', '(', ')', ')', '{', '}'])

        source = '!*+-/=<> <= == // operators'
        self.assertEqual(self.runScanner(source),
                         ['!', '*', '+', '-', '/', '=',
                          '<', '>', '<=', '=='])

    def test_should_return_string_literal(self):
        source = '"hello world"'
        tokens = Scanner(source).scanTokens()
        literals = [token.literal for token in tokens]
        self.assertEqual(literals,
                         ['hello world'])

    def test_should_return_integer_literal(self):
        source = '123'
        self.assertEqual(self.runScanner(source), ['123'])

    def test_should_return_float_literal(self):
        source = '123.456'
        self.assertEqual(self.runScanner(source), ['123.456'])

    def test_should_return_identifier(self):
        source = 'x'
        tokens = Scanner(source).scanTokens()
        types = [token.type for token in tokens]
        self.assertEqual(types, [TokenType.IDENTIFIER])

    def test_should_recognize_keyword(self):
        source = 'for'
        tokens = Scanner(source).scanTokens()
        types = [token.type for token in tokens]
        self.assertEqual(types, [TokenType.FOR])

    def test_should_return_correct_tokens_for_class(self):
        source = '''
            class Breakfast {
                init(meat, bread) {
                    this.meat = meat
                    this.bread = bread
                }
            }

            class Brunch < Breakfast {
                drink() {
                    print "How about a Bloody Mary?";
                }
            }
        '''

        tokens = Scanner(source).scanTokens()
        self.assertEqual(len(tokens), 36)
        self.assertEqual(sum(1 for token in tokens
                             if token.type == TokenType.IDENTIFIER),
                         11)
        self.assertEqual(sum(1 for token in tokens
                             if token.lexeme in ['{', '}']),
                         8)

    def test_should_return_correct_tokens_for_if(self):
        source = '''
            if (a > 1) {
                print "yes";
            } else {
                print "no";
            }
        '''

        tokens = Scanner(source).scanTokens()
        self.assertEqual(len(tokens), 17)
        self.assertEqual(sum(1 for token in tokens
                             if token.lexeme in ['if', 'else']),
                         2)

    def test_should_return_correct_tokens_for_for(self):
        source = '''
            for (var a = 1; a < 10; a = a + 1) {
                print a;
            }
        '''

        tokens = Scanner(source).scanTokens()
        self.assertEqual(len(tokens), 22)

    def test_should_return_correct_tokens_for_fun(self):
        source = '''
            fun nthfib(n) {
                if (n == 0 or n == 1) {
                    return n;
                }

                var a = 0;
                var b = 1;

                for (var i = 0; i < n; i = i + 1) {
                    var t = a;
                    a = b;
                    b = a + t;
                }

                return a;
            }
        '''

        tokens = Scanner(source).scanTokens()
        self.assertEqual(len(tokens), 69)
