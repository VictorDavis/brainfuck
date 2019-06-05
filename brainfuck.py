# bloody dependencies
import sys

# defaults (NOTE: x & 255 == x % 256)
CELLMAX = 255
PTRMAX = 32767
ALPHABET = "><+-.,[]"
MAXFLOPS = 8192

class Monitor:

    def __init__(self, maxflops: int):
        self.flops = 0
        self.maxflops = maxflops

    def ping(self) -> bool:
        self.flops += 1
        ok = self.flops < self.maxflops
        return ok

def match_brackets(code: str) -> dict:
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
            assert len(mem) > 0, f"Unmatched close bracket ] at position {ptr}"
            opener = mem.pop()
            closer = ptr
            brackets[opener] = closer
            brackets[closer] = opener

    # unmatched open
    assert len(mem) == 0, f"Unmatched open bracket(s) [ at position(s) " + ",".join(map(str, mem))

    # return dictionary
    return brackets


def load(fname: str) -> str:
    """Opens a file and returns the contents."""
    with open(fname, "r") as f:
        code = f.read()
        f.close()
    return code

def run(code: str, input: str = "") -> str:
    """
    Runs brainfuck code.
    :param code: (string) Brainfuck code
    :param input: (string, optional) Code input
    :returns output: (string) Code output
    """

    # clean
    code = "".join([ char for char in code if char in ALPHABET ])

    # initialize
    cells = [0] * (PTRMAX + 1)
    ptr, inptr, readr = 0, 0, 0
    brackets = match_brackets(code)
    output = ""

    # monitor
    monitor = Monitor(maxflops = MAXFLOPS)

    # loop
    L = len(code)
    while readr < L:

        # monitor
        assert monitor.ping(), f"Error: Flops exceeded {monitor.maxflops}."

        # command
        cmd = code[readr]
        readr += 1

        # increment the data pointer (to point to the next cell to the right).
        if cmd == ">":
            ptr = (ptr+1) & PTRMAX
            continue

        # decrement the data pointer (to point to the next cell to the left).
        if cmd == "<":
            ptr = (ptr-1) & PTRMAX
            continue

        # increment (increase by one) the byte at the data pointer.
        if cmd == "+":
            cells[ptr] = (cells[ptr]+1) & CELLMAX
            continue

        # decrement (decrease by one) the byte at the data pointer.
        if cmd == "-":
            cells[ptr] = (cells[ptr]-1) & CELLMAX
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
                # terminate program if run out of input
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

    # return
    return output


def main():
    L = len(sys.argv)
    if L in [2, 3]:

        # (required) file name
        fname = sys.argv[1]
        code = load(fname)

        # (optional) input
        input = ""
        if L > 2:
            input = sys.argv[2]

        # zoomzoom!
        output = run(code, input)
        print(output)

    else:
        print("Usage:", sys.argv[0], "<filename> (<input>)")


if __name__ == "__main__": main()
