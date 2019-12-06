from enum import Enum, unique
from pathlib import Path
from typing import List


Position = int
Tape = List[Position]


@unique
class Opcode(Enum):
    ADD = 1
    MULT = 2
    EXIT = 99


def process_tape(tape: Tape) -> int:
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
    args = parser.parse_args()
    tape = read_tape_from_file(args.input_file)
    # The instructions specify to first make these changes.
    tape[1] = 12
    tape[2] = 2
    result = process_tape(tape)
    print(f"Result from position 0: {result}")
