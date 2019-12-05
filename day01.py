from pathlib import Path
from typing import List


def calculate_fuel_from_mass(mass: int) -> int:
    fuel = (mass // 3) - 2
    if fuel < 0:
        raise ValueError(f"Mass requires less-than-zero fuel: {mass}")
    return fuel


def calculate_fuel_from_masses(masses: List[int]) -> int:
    return sum(calculate_fuel_from_mass(mass) for mass in masses)


def read_masses_from_text(text: str) -> List[int]:
    return [int(line.strip()) for line in text.split('\n') if line]


def read_masses_from_file(filename: Path) -> List[int]:
    with open(filename) as f:
        text = f.read()
    masses = read_masses_from_text(text)
    return masses


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=Path, help="file to read masses from; each mass should be an integer on its own line")
    args = parser.parse_args()
    masses = read_masses_from_file(args.input_file)
    fuel = calculate_fuel_from_masses(masses)
    print(f"Total fuel required: {fuel}")
