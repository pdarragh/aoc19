from dataclasses import dataclass, field
from enum import Enum, unique
from pathlib import Path
from typing import Dict, List, Set, Tuple


@unique
class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


STR_TO_DIRECTION = {
    'U': Direction.UP,
    'D': Direction.DOWN,
    'L': Direction.LEFT,
    'R': Direction.RIGHT,
}


Coord = Tuple[int, int]
WireInstruction = Tuple[Direction, int]
Wire = List[Coord]


DISTANCE = 'distance'
STEPS = 'steps'
ORIGIN: Coord = (0, 0)


def add_coords(lhs: Coord, rhs: Coord) -> Coord:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


def find_wire_crossing_points(*wires: Wire, exclude: Set[Coord]=None) -> Set[Coord]:
    if exclude is None:
        exclude = {ORIGIN}
    return set.intersection(*[set(wire) for wire in wires]) - exclude


def distance_from_origin(coord: Coord) -> int:
    return abs(coord[0]) + abs(coord[1])


def distances_from_origin(coords: Set[Coord]) -> List[int]:
    return [distance_from_origin(coord) for coord in coords]


def steps_to_cross(crossing_points: Set[Coord], *wires) -> Dict[Coord, int]:
    points_to_steps = {}
    for point in crossing_points:
        points_to_steps[point] = [0] * len(wires)
    for wire_no, wire in enumerate(wires):
        steps = 0
        for coord in wire[1:]:  # We're counting steps between coordinates, not coordinates themselves.
            steps += 1
            # Only record the lowest step value for each wire.
            if coord in points_to_steps and points_to_steps[coord][wire_no] == 0:
                points_to_steps[coord][wire_no] = steps
    return {point: sum(points_to_steps[point]) for point in points_to_steps}


def str_to_instruction(text: str) -> WireInstruction:
    text = text.strip()
    direction = STR_TO_DIRECTION[text[0]]
    distance = int(text[1:])
    return (direction, distance)


def read_wire(text: str) -> Wire:
    instructions = [str_to_instruction(step) for step in text.strip().split(',')]
    coords = []
    curr = ORIGIN
    coords.append(curr)
    for direction, distance in instructions:
        for _ in range(distance):
            curr = add_coords(curr, direction.value)
            coords.append(curr)
    return coords


def read_wires_from_file(filename: Path) -> List[Wire]:
    with open(filename) as f:
        lines = f.readlines()
    return [read_wire(line) for line in lines if line.strip()]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=Path, help="file to read wires from; each wire should be on its own line")
    parser.add_argument('-m', '--mode', choices=[DISTANCE, STEPS], default='distance',
                        help="whether to identify crossing points by distance from origin or length of the wires")
    args = parser.parse_args()
    wires = read_wires_from_file(args.input_file)
    if len(wires) < 2:
        raise RuntimeError("Must have at least two wires defined in input file")
    crossing_points = find_wire_crossing_points(*wires)
    if not crossing_points:
        raise RuntimeError("No crossing points found")
    if args.mode == DISTANCE:
        distances = distances_from_origin(crossing_points)
        distances.sort()
        print(f"Nearest crossing point is {distances[0]} units from the origin.")
    elif args.mode == STEPS:
        steps = steps_to_cross(crossing_points, *wires)
        nearest_coord, fewest_steps = min(steps.items(), key=lambda p: p[1])
        print(f"Nearest crossing point is {nearest_coord}, which is {fewest_steps} total steps from the origin.")
    else:
        raise ValueError(f"Unknown mode: {args.mode}")
