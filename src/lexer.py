from src._token import *

def main(filepath):
    print("Target file", filepath)

    stream = TokenStream()
    with open(filepath, 'r') as f:
        for line in f:
            for c in line:
                print(c)


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) < 2:
        print("no input")
    else:
        main(args[1])
