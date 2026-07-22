"""General-purpose Turing Machine simulator with built-in example machines.

Run `python main.py --list-machines` to see the available examples,
or `python main.py --machine inverter --tape 1100` to run one.
"""

import argparse
import time
from typing import Dict

DEFAULT_DELAY = 0.4

# Each example machine: transition rules, default tape, and a short description.
# Rule format — 'current_state current_char': 'next_state write_char movement'
# Movements: R (Right), L (Left), N (No movement)
EXAMPLE_MACHINES = {
    "palindrome": {
        "description": (
            "Accepts binary palindromes by erasing matched characters "
            "from both ends until the tape is empty."
        ),
        "tape": "101101",
        "rules": {
            # look for the first character from the left
            "q0 0": "q1 # R",
            "q0 1": "q2 # R",
            "q0 #": "qf # N",
            # go right to the end if it was 0
            "q1 0": "q1 0 R",
            "q1 1": "q1 1 R",
            "q1 #": "q3 # L",
            # go right to the end if it was 1
            "q2 0": "q2 0 R",
            "q2 1": "q2 1 R",
            "q2 #": "q4 # L",
            # the rightmost character must match the erased leftmost one
            "q3 0": "q5 # L",
            "q3 #": "qf # N",
            "q4 1": "q5 # L",
            "q4 #": "qf # N",
            # return to the beginning
            "q5 0": "q5 0 L",
            "q5 1": "q5 1 L",
            "q5 #": "q0 # R",
        },
    },
    "inverter": {
        "description": "Flips every bit on the tape: 0 becomes 1, 1 becomes 0.",
        "tape": "101010",
        "rules": {
            "q0 0": "q0 1 R",
            "q0 1": "q0 0 R",
            "q0 #": "qf # N",
        },
    },
}

INITIAL_STATE = "q0"
HALT_STATE = "qf"
BLANK_SYMBOL = "#"


class TuringMachine:
    """
    A class representing a 1D Turing Machine.
    """

    def __init__(
        self,
        tape_str: str,
        initial_state: str,
        halt_state: str,
        blank: str,
        rules: Dict[str, str],
    ):
        # Represent tape as a dictionary for infinite-like behavior (index: character)
        self.tape = {i: char for i, char in enumerate(tape_str)}
        self.state = initial_state
        self.halt_state = halt_state
        self.blank = blank
        self.rules = rules
        self.head_position = 0
        self.step_count = 0

    def tape_str(self) -> str:
        """Return the current tape contents with leading/trailing blanks stripped."""
        if not self.tape:
            return ""
        cells = range(min(self.tape), max(self.tape) + 1)
        return "".join(self.tape.get(i, self.blank) for i in cells).strip(self.blank)

    def display(self) -> None:
        """
        Renders the current state of the tape and head position to the console.
        """
        keys = self.tape.keys()
        if not keys:
            min_index, max_index = self.head_position - 1, self.head_position + 1
        else:
            # Determine boundaries with a bit of padding for visual clarity
            min_index = min(min(keys), self.head_position) - 1
            max_index = max(max(keys), self.head_position) + 1

        tape_line = ""
        head_pointer = ""

        for i in range(min_index, max_index + 1):
            char = self.tape.get(i, self.blank)
            if i == self.head_position:
                tape_line += f"[{char}]"
                head_pointer += " ^ "
            else:
                tape_line += f" {char} "
                head_pointer += "   "

        print(f"Step: {self.step_count} | Current State: {self.state}")
        print(tape_line)
        print(head_pointer)
        print("-" * 40)

    def step(self) -> bool:
        """
        Executes a single step of the Turing machine.
        Returns True if the machine should continue, False if it has halted.

        A missing transition rule is a normal halt (the input is rejected),
        not an error — recognizer machines rely on this to reject input.
        """
        current_char = self.tape.get(self.head_position, self.blank)
        lookup_key = f"{self.state} {current_char}"

        if lookup_key not in self.rules:
            print(
                f"No transition for state '{self.state}' and character "
                f"'{current_char}' — machine halts."
            )
            return False

        # Parse transition: [next_state, next_char, movement]
        action = self.rules[lookup_key].split()
        if len(action) != 3:
            raise ValueError(f"Invalid rule format for '{lookup_key}'")

        next_state, next_char, movement = action

        # Update tape and state
        self.tape[self.head_position] = next_char
        self.state = next_state

        # Move the head
        if movement == "R":
            self.head_position += 1
        elif movement == "L":
            self.head_position -= 1
        elif movement != "N":
            raise ValueError(f"Invalid movement command '{movement}'")

        self.step_count += 1
        return True

    def run(self, delay: float = DEFAULT_DELAY) -> bool:
        """
        Runs the machine until it reaches the halt state or gets stuck.
        Returns True if the halt (accepting) state was reached.
        """
        print(">>> INITIALIZING TURING MACHINE <<<")
        self.display()

        while self.state != self.halt_state:
            if not self.step():
                break

            if delay:
                time.sleep(delay)
            self.display()

        accepted = self.state == self.halt_state
        if accepted:
            print(">>> EXECUTION COMPLETED: HALT STATE REACHED <<<")
        else:
            print(">>> EXECUTION STOPPED: INPUT REJECTED <<<")
        print(f"Final tape: '{self.tape_str()}' after {self.step_count} steps")
        return accepted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-m",
        "--machine",
        choices=sorted(EXAMPLE_MACHINES),
        default="palindrome",
        help="example machine to run (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--tape",
        help="initial tape content (default: the chosen machine's example tape)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help="seconds between steps, 0 to run at full speed (default: %(default)s)",
    )
    parser.add_argument(
        "--list-machines",
        action="store_true",
        help="list the available example machines and exit",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the Turing Machine simulation.
    """
    args = parse_args()

    if args.list_machines:
        for name, machine in sorted(EXAMPLE_MACHINES.items()):
            print(f"{name:12} {machine['description']}")
        return

    machine = EXAMPLE_MACHINES[args.machine]
    tm = TuringMachine(
        tape_str=args.tape if args.tape is not None else machine["tape"],
        initial_state=INITIAL_STATE,
        halt_state=HALT_STATE,
        blank=BLANK_SYMBOL,
        rules=machine["rules"],
    )
    tm.run(delay=args.delay)


if __name__ == "__main__":
    main()
