import dataclasses
import enum
import re

symbols_pattern = re.compile(r"[+=]")
delimiter = re.compile(r"[\s\t]")


class TokenType(enum.Enum):
    TOK_IDENTIFIER = 1
    TOK_DIGIT = 2
    TOK_SYMBOL = 3

    TOK_PRINT = 100


@dataclasses.dataclass
class Token:
    token_type: TokenType
    token_string: str
    number: int
    line: int

    @classmethod
    def init_from_string(cls, token_string: str, line: int):
        token_string = token_string
        number = None
        token_type = TokenType.TOK_IDENTIFIER

        if token_string == "print":
            token_type = TokenType.TOK_PRINT
        elif token_string.isdigit():
            number = int(token_string)
            token_type = TokenType.TOK_DIGIT
        elif token_string.isalnum():
            token_type = TokenType.TOK_IDENTIFIER
        if symbols_pattern.match(token_string):
            token_type = TokenType.TOK_SYMBOL

        return Token(token_type, token_string, number, line)


class TokenStream:
    tokens: list = []
    current_index: int = 0

    def __repr__(self):
        return f"index: {self.current_index} tokens: {self.tokens}"
