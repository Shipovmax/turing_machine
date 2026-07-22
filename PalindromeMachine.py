"""Two-pointer palindrome checker with step-by-step console visualisation.

Run `python PalindromeMachine.py --tape 10101` to check your own input.
"""

import argparse
import time

DEFAULT_TAPE = "1001"
DEFAULT_DELAY = 0.4


class PalindromeMachine:

    def __init__(self, tape: str) -> None:
        self.tape: str = tape
        self.left: int = 0
        self.right: int = len(tape) - 1
        self.step_count: int = 0

    def display(self) -> None:
        print(f"Step: {self.step_count}")
        print(self.tape)
        print(" " * self.left + "^" + " " * (self.right - self.left - 1) + "^")
        print("-" * 40)

    def step(self) -> str:
        if self.left >= self.right:
            return "ACCEPT"

        if self.tape[self.left] != self.tape[self.right]:
            return "REJECT"

        self.left += 1
        self.right -= 1
        self.step_count += 1

        return "CONTINUE"

    def run(self, delay: float = DEFAULT_DELAY) -> bool:
        """Run to completion; return True if the tape is a palindrome."""
        print("--- PALINDROME CHECK STARTED ---")
        self.display()

        while True:
            result = self.step()

            if result == "ACCEPT":
                print("--- IT IS A PALINDROME ---")
                return True

            if result == "REJECT":
                print("--- IT IS NOT A PALINDROME ---")
                return False

            if delay:
                time.sleep(delay)
            self.display()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-t",
        "--tape",
        default=DEFAULT_TAPE,
        help="string to check (default: %(default)s)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help="seconds between steps, 0 to run at full speed (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    machine = PalindromeMachine(args.tape)
    machine.run(delay=args.delay)


if __name__ == "__main__":
    main()
