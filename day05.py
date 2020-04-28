from enum import Enum, unique
from pathlib import Path
from typing import Iterable, List, Tuple


Position = int
Tape = List[Position]


MAX_VALUE = 99  # The maximum value for a noun or verb.


@unique
class Opcode(Enum):
    ADD = 1
    MULT = 2
    EXIT = 99


def process_tape(tape: Tape, noun: int, verb: int) -> int:
    # Install the noun and verb.
    tape[1] = noun
    tape[2] = verb
    # Run the tape!
    pos = 0
    while True:
        try:
            opcode = Opcode(tape[pos])
        except ValueError:
            raise RuntimeError(f"Invalid opcode at position {pos}: {tape[pos]}")
        # Process the opcode.
        if opcode in (Opcode.ADD, Opcode.MULT):
            if len(tape) < pos + 3 + 1:
                raise RuntimeError(f"Out-of-bounds tape access from position {pos}")
            # Read positions.
            in1_pos = tape[pos + 1]
            in2_pos = tape[pos + 2]
            out_pos = tape[pos + 3]
            # Calculate result.
            in1 = tape[in1_pos]
            in2 = tape[in2_pos]
            if opcode is Opcode.ADD:
                res = in1 + in2
            elif opcode is Opcode.MULT:
                res = in1 * in2
            else:
                raise RuntimeError(f"Unexpected mathematical opcode: {opcode}")
            # Modify tape in-place to store result.
            tape[out_pos] = res
            pos += 4
        elif opcode is Opcode.EXIT:
            # Nothing more to do!
            break
        else:
            raise RuntimeError(f"Unhandled opcode: {opcode}")
    return tape[0]


def solve_tape(tape: Tape, noun_range: Iterable[int],
               verb_range: Iterable[int], desired_output: int
              ) -> List[Tuple[int, int]]:
    results = []
    for noun in noun_range:
        for verb in verb_range:
            tape_copy = tape.copy()
            output = process_tape(tape_copy, noun, verb)
            if output == desired_output:
                result = (noun, verb)
                results.append(result)
    if not results:
        # No matching noun/verb combination was found.
        raise RuntimeError(f"No matching noun/verb combination found")
    else:
        return results


def read_tape_from_text(text: str) -> Tape:
    return [int(s.strip()) for s in text.split(',')]


def read_tape_from_file(filename: Path) -> Tape:
    with open(filename) as f:
        text = f.read()
    tape = read_tape_from_text(text)
    return tape


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=Path, help="file to read tape from; the tape should be a comma-separated "
                                                      "list of integers")
    parser.add_argument('--noun', type=int, help="the noun to use; leave blank to solve")
    parser.add_argument('--verb', type=int, help="the verb to use; leave blank to solve")
    parser.add_argument('--solve', type=int, help="the desired solution to solve for; leave blank to not solve")
    args = parser.parse_args()
    # Read the tape from file.
    tape = read_tape_from_file(args.input_file)
    # Run or solve tape, based on input.
    if args.solve is None:
        # Just run the tape with default noun/verb values if needed.
        noun = args.noun if args.noun is not None else 12
        verb = args.verb if args.verb is not None else 2
        print(f"Running tape with noun {args.noun} and verb {args.verb}...")
        result = process_tape(tape, noun, verb)
        print(f"Result: {result}")
    else:
        # Solve for the desired value. Identify noun/verb ranges to test.
        print(f"Solving tape...")
        noun_range = range(MAX_VALUE + 1) if args.noun is None else (args.noun, )
        verb_range = range(MAX_VALUE + 1) if args.verb is None else (args.verb, )
        results = solve_tape(tape, noun_range, verb_range, args.solve)
        if len(results) == 1:
            noun, verb = results[0]
            print(f"Noun: {noun}, Verb: {verb}")
        else:
            print("Found multiple potential solutions:")
            for noun, verb in results:
                print(f"  Noun: {noun}, Verb: {verb}")
