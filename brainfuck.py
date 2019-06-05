# bloody dependencies
import sys

# defaults
VERBOSE = False
SAFETYON, MAXLOOP = True, 999999
CELLSIZE = 256
NUMCELLS = 32768

def match_brackets(code) -> dict:
    """Calculates dictionary of matching brackets."""

    # build map
    brackets = {}
    mem = []
    L = len(code)
    _range = range(L)
    for ptr in _range:
        if code[ptr] == "[":
            mem.append(ptr)
            continue
        if code[ptr] == "]":
            if len(mem) == 0:
                raise UserWarning("Unmatched close bracket at position", ptr)
            opener = mem.pop()
            closer = ptr
            brackets[opener] = closer
            brackets[closer] = opener

    # unmatched open
    if len(mem) > 0:
        raise UserWarning("Unmatched open bracket(s) at position(s)", mem)

    # return dictionary
    return brackets


def load(fname: str):
    """Opens a file and returns the contents."""
    with open(fname, "r") as f:
        code = f.read()
        f.close()
    return code

def loadrun(fname: str, input: str = ""):
    """Opens a file and runs the contents."""
    code = load(fname)
    output = run(code, input)
    return output

def run(code: str, input: str = ""):
    """
    Runs brainfuck code.
    :param code: (string) Brainfuck code
    :param input: (string, optional) Code input
    """

    # clean
    ALPHABET = "><+-.,[]"
    code = "".join([ char for char in code if char in ALPHABET ])

    # recap
    if VERBOSE:
        print("Code:", code)
    L = len(code)

    # initialize
    cells = [0] * NUMCELLS
    ptr, maxptr, inptr, readr = 0, 0, 0, 0
    brackets = match_brackets(code)
    if VERBOSE:
        print("Brackets:", brackets)
    output = ""

    # cheat
    ctr = 0

    # loop
    while readr < L:

        # counter
        ctr += 1
        if ptr > maxptr:
            maxptr = ptr

        # safety: cap iterations
        if SAFETYON:
            if ctr > MAXLOOP:
                break

        # command
        cmd = code[readr]
        readr += 1

        # logging
        if VERBOSE:
            print(code[:readr])
            print(cells[:maxptr], ptr, cells[ptr], cmd, output)

        # increment the data pointer (to point to the next cell to the right).
        if cmd == ">":
            # ptr = (ptr+1) % NUMCELLS
            if ptr < NUMCELLS:
                ptr += 1
            else:
                ptr = 0
            continue

        # decrement the data pointer (to point to the next cell to the left).
        if cmd == "<":
            # ptr = (ptr+1) % NUMCELLS
            if ptr > 0:
                ptr -= 1
            else:
                ptr = NUMCELLS - 1
            continue

        # increment (increase by one) the byte at the data pointer.
        if cmd == "+":
            # cells[ptr] = (cells[ptr]+1) % CELLSIZE
            if cells[ptr] < CELLSIZE:
                cells[ptr] += 1
            else:
                cells[ptr] = 0
            continue

        # decrement (decrease by one) the byte at the data pointer.
        if cmd == "-":
            # cells[ptr] = (cells[ptr]-1) % CELLSIZE
            if cells[ptr] > 0:
                cells[ptr] -= 1
            else:
                cells[ptr] = CELLSIZE - 1
            continue

        # output the byte at the data pointer.
        if cmd == ".":
            output += chr(cells[ptr])
            continue

        # accept one byte of input, storing its value in the byte at the data pointer.
        if cmd == ",":
            if inptr < len(input):
                inchar = input[inptr]
                inptr += 1
                cells[ptr] = ord(inchar)
            else:
                break
            continue

        # if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
        if cmd == "[":
            if cells[ptr] == 0:
                readr = brackets[readr-1]
            continue

        # if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.
        if cmd == "]":
            if cells[ptr] > 0:
                readr = brackets[readr-1]
            continue

    # done
    print("Iterations:", ctr)
    print("Memory cells utilized:", maxptr)
    print("\nOutput:", output)

    # return
    return output


def main():
    if len(sys.argv) == 2:
        loadrun(sys.argv[1])
    else:
        if len(sys.argv) == 3:
            loadrun(sys.argv[1], sys.argv[2])
        else:
            print("Usage:", sys.argv[0], "<filename> (<input>)")

if __name__ == "__main__": main()
