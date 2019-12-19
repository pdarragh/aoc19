def compute_possibilities(lo: int, hi: int) -> int:
    nums = range(max(lo, 100_000), min(hi + 1, 999_999))
    count = 0
    for num in nums:
        s = str(num)
        valid = True     # Used for breaking.
        doubles = False  # Whether an exact double has been found.
        repeating = 0    # Counts sequential repetitions of a digit.
        for lc, rc in zip(s[:-1], s[1:]):
            if rc < lc:
                # Digits must never decrease.
                valid = False
                break
            elif lc == rc:
                # We're in a repetition.
                repeating += 1
            else:
                # If the digit was repeated exactly once, there is a double.
                if repeating == 1:
                    doubles = True
                # Mr. Gaeta, restart the clock!
                repeating = 0
        # Check whether the last pair of digits formed a double.
        if repeating == 1:
            doubles = True
        # Count only valid numbers.
        if valid & doubles:
            count += 1
    return count

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('lo', type=int, nargs='?', default=100_000, help="the low end of the range")
    parser.add_argument('hi', type=int, nargs='?', default=999_999, help="the high end of the range")
    args = parser.parse_args()
    possibilities = compute_possibilities(args.lo, args.hi)
    print(f"There are {possibilities} possible passwords on the interval [{args.lo}, {args.hi}].")
