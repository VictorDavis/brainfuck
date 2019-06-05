# bloody dependencies
import inspect
import unittest

from ..brainfuck import load, run, match_brackets


# unit tests
class BrainfuckTest(unittest.TestCase):

    # https://en.wikipedia.org/wiki/Brainfuck#Hello_World!
    def test_hello(self):
        code = load('data/hello.bf')
        output = run(code)
        assert output == "Hello World!\n"

    # https://en.wikipedia.org/wiki/Brainfuck#Adding_two_values
    def test_add(self):
        code = load('data/add.bf')
        output = run(code)
        assert output == "7"

    # https://en.wikipedia.org/wiki/Brainfuck#ROT13
    def test_rot13(self):

        # jokes: https://en.wikipedia.org/wiki/ROT13#Description
        jokes = {
            "Jul qvq gur puvpxra pebff gur ebnq?": "Why did the chicken cross the road?",
            "Gb trg gb gur bgure fvqr!": "To get to the other side!"
        }

        # run
        code = load('data/rot13.bf')
        output = run(code)
        for joke, answer in jokes.items():
            output = run(code, joke)
            assert output == answer

    # http://esoteric.sange.fi/brainfuck/bf-source/prog/fibonacci.txt
    def test_fibonacci(self):
        code = load('data/fibonacci.bf')
        output = run(code)
        assert output == "1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89"

    # http://esoteric.sange.fi/brainfuck/bf-source/prog/fibonacci.txt
    def test_cellsize(self):
        code = load('data/cellsize.bf')
        output = run(code)
        assert output == "8 bit cells\n"

    # https://esolangs.org/wiki/Brainfuck#Memory_and_wrapping
    def test_cellsize2(self):
        # NOTE: will work only if CELLMAX = 255 (8-bit)
        output = run('+[[->]-[-<]>-]>.>>>>.<<<<-.>>-.>.<<.>>>>-.<<<<<++.>>++.')
        assert output == "brainfuck"

    # https://sange.fi/esoteric/brainfuck/bf-source/prog/tests.b
    def test_brackets(self):

        # unmatched open
        with self.assertRaises(AssertionError) as context:
            brackets = match_brackets("+++++[>+++++++>++<<-]>.>.[")
            assert "Unmatched open" in context

        # unmatched close
        with self.assertRaises(AssertionError) as context:
            brackets = match_brackets("+++++[>+++++++>++<<-]>.>.][")
            assert "Unmatched close" in context

        # okay
        brackets = match_brackets("[[]]")
        assert brackets == {0:3, 3:0, 1:2, 2:1}
