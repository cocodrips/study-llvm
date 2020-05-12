from src._token import *


def main(filepath):
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
                    if not token_string:
                        continue
                    token = Token.init_from_string(token_string, line_num)
                    stream.tokens.append(token)
                    token_string = ""
                else:
                    raise Exception(f"Unsupported character: {c}")

            # Last token
            if token_string:
                token = Token.init_from_string(token_string, line_num)
                stream.tokens.append(token)

    for token in stream.tokens:
        print(token)


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) < 2:
        print("no input")
    else:
        main(args[1])
