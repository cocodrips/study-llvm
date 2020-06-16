from src._token import *


def lexical_analysis(filepath) -> TokenStream:
    print("Target file", filepath)

    stream = TokenStream()
    with open(filepath, 'r') as f:

        for line_num, line in enumerate(f):
            iscomment = False
            token_string = ""

            for c in line:
                if iscomment:
                    raise NotImplementedError()

                elif c.isalnum() or symbols_pattern.match(c):
                    token_string = token_string + c

                elif delimiter.match(c):
                    if token_string:
                        token = Token.init_from_string(token_string, line_num)
                        stream.tokens.append(token)
                        token_string = ""
                    if c == "\n":
                        stream.tokens.append(Token.init_from_string("\n", line_num))

                else:
                    raise Exception(f"Unsupported character: {c}")

            # Last token
            if token_string:
                token = Token.init_from_string(token_string, line_num)
                stream.tokens.append(token)
        stream.tokens.append(Token(token_type=TokenType.TOK_EOF))

    return stream


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) < 2:
        print("no input")
    else:
        lexical_analysis(args[1])
