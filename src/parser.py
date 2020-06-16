from lexer import lexical_analysis
from _token import *
from ast import *
from typing import Optional, List


def reset_stream_if_not_match(func):
    def wrapper(self):
        if not isinstance(self, Parser):
            raise Exception("This function doesn't Parser")
        index = self.tokens.current_index
        rtn = func(self)
        if not rtn:
            self.tokens.current_index = index
        return rtn

    return wrapper




class Parser:
    def __init__(self, filename):
        self.tokens: TokenStream = lexical_analysis(filename)
        self.variable_table: List[str] = []
        self.unit: Optional[StatementListAST] = None

    @property
    def _symbol_pattern(self):
        return re.compile(r"[+-]")

    def parse(self):
        self.visit_transration_unit()
        self.semantic_analysis()

    def visit_transration_unit(self):
        unit = StatementListAST()

        while self.tokens.currentToken.token_type != TokenType.TOK_EOF:
            ast = self.visit_statement()
            if ast:
                unit.asts.append(ast)
        self.unit = unit
        return unit

    def visit_statement(self):
        token = self.tokens.currentToken

        def get_statement():
            if token.token_type == TokenType.TOK_IDENTIFIER:
                if binary_expr := self.visit_binary_expr():
                    return binary_expr

                if assign_expr := self.visit_assignment():
                    return assign_expr

            if token.token_type == TokenType.TOK_PRINT:
                if print_expr := self.visit_print_expr():
                    return print_expr

            return None

        ast = get_statement()
        token = self.tokens.nextToken()
        if ast and token.token_type > TokenType.TOK_END_STATEMENT:
            return ast
        return None

    @reset_stream_if_not_match
    def visit_assignment(self):
        token = self.tokens.currentToken

        if token.token_type != TokenType.TOK_IDENTIFIER:
            return None
        variable = VariableAST(name=token.token_string)

        token = self.tokens.nextToken()
        if token.token_string != "=":
            return None

        token = self.tokens.nextToken()

        value = self._get_id_or_digit(token)
        if value is None:
            return None

        return AssignmentAST(variable=variable, value=value)

    @reset_stream_if_not_match
    def visit_binary_expr(self) -> Optional[BinaryExprAST]:
        """
        BINARY_EXPR := <ID | DIGIT> <SYMBOL> <ID | DIGIT>
        """
        token = self.tokens.currentToken

        if (left := self._get_id_or_digit(token)) is None:
            return None

        token = self.tokens.nextToken()
        if ((token.token_type == TokenType.TOK_SYMBOL)
                and self._symbol_pattern.match(token.token_string)):
            op = token.token_string
        else:
            return None

        token = self.tokens.nextToken()
        if (right := self._get_id_or_digit(token)) is None:
            return None

        return BinaryExprAST(left=left, op=op, right=right)

    @reset_stream_if_not_match
    def visit_print_expr(self):
        """
        PRINT_EXPR := <PRINT> <BINARY_EXPR | ID | DIGIT>
        """
        token = self.tokens.currentToken

        if token.token_type != TokenType.TOK_PRINT:
            return None

        token = self.tokens.nextToken()
        if binary_expr := self.visit_binary_expr():
            return PrintAST(arg=binary_expr)

        if variable := self._get_id_or_digit(token):
            return PrintAST(arg=variable)
        return None


    def _get_id_or_digit(self, token):
        if token.token_type == TokenType.TOK_IDENTIFIER:
            return VariableAST(name=token.token_string)
        elif token.token_type == TokenType.TOK_DIGIT:
            return DigitAST(value=token.number)
        return None

    def semantic_analysis(self):
        if self.unit is None:
            raise Exception("Please visit_transration_unit first.")
        for ast in self.unit.asts:
            if isinstance(ast, AssignmentAST):
                self.variable_table.append(ast.variable.name)
            else:
                for ast in vars(ast).values():
                    if isinstance(ast, VariableAST):
                        if ast.name not in self.variable_table:
                            raise Exception(f"Parse error: {ast.name} is not declared.")




if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) < 2:
        print("no input")
    else:
        parser = Parser(args[1])
        parser.parse()
        print(parser.unit.asts, parser.variable_table)
