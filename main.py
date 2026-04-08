import time
from typing import Dict, Tuple

# ==========================================
# TURING MACHINE CONFIGURATION
# ==========================================

# Initial content on the tape
INITIAL_TAPE = "101010"
# Starting state of the machine
INITIAL_STATE = "q0"
# State that signifies the machine has finished its work
HALT_STATE = "qf"
# Character used for empty tape cells
BLANK_SYMBOL = "#"

# Transition rules dictionary: 'current_state current_char': 'next_state next_char movement'
# This example implements bit inversion: 0 becomes 1, and 1 becomes 0.
# Movements: R (Right), L (Left), N (No movement)
TRANSITION_RULES = {

    # ищем первый символ слева
    'q0 0': 'q1 # R',
    'q0 1': 'q2 # R',
    'q0 #': 'qf # N',

    # идём вправо до конца если был 0
    'q1 0': 'q1 0 R',
    'q1 1': 'q1 1 R',
    'q1 #': 'q3 # L',

    # идём вправо до конца если был 1
    'q2 0': 'q2 0 R',
    'q2 1': 'q2 1 R',
    'q2 #': 'q4 # L',

    # проверяем справа 0
    'q3 0': 'q5 # L',

    # проверяем справа 1
    'q4 1': 'q5 # L',

    # возвращаемся в начало
    'q5 0': 'q5 0 L',
    'q5 1': 'q5 1 L',
    'q5 #': 'q0 # R'
}


class TuringMachine:
    """
    A class representing a 1D Turing Machine.
    """

    def __init__(self, tape_str: str, initial_state: str, halt_state: str, blank: str, rules: Dict[str, str]):
        # Represent tape as a dictionary for infinite-like behavior (index: character)
        self.tape = {i: char for i, char in enumerate(tape_str)}
        self.state = initial_state
        self.halt_state = halt_state
        self.blank = blank
        self.rules = rules
        self.head_position = 0
        self.step_count = 0

    def display(self):
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
        Returns True if the machine should continue, False if it has halted or crashed.
        """
        current_char = self.tape.get(self.head_position, self.blank)
        lookup_key = f"{self.state} {current_char}"

        if lookup_key not in self.rules:
            print(f"CRITICAL ERROR: No transition rule found for state '{self.state}' and character '{current_char}'")
            return False

        # Parse transition: [next_state, next_char, movement]
        action = self.rules[lookup_key].split()
        if len(action) != 3:
            print(f"CRITICAL ERROR: Invalid rule format for '{lookup_key}'")
            return False

        next_state, next_char, movement = action

        # Update tape and state
        self.tape[self.head_position] = next_char
        self.state = next_state

        # Move the head
        if movement == 'R':
            self.head_position += 1
        elif movement == 'L':
            self.head_position -= 1
        elif movement == 'N':
            pass
        else:
            print(f"CRITICAL ERROR: Invalid movement command '{movement}'")
            return False

        self.step_count += 1
        return True

    def run(self, delay: float = 0.4):
        """
        Runs the Turing machine until it reaches the halt state or encounters an error.
        """
        print(">>> INITIALIZING TURING MACHINE <<<")
        self.display()

        while self.state != self.halt_state:
            if not self.step():
                break
            
            time.sleep(delay)
            self.display()

        if self.state == self.halt_state:
            print(">>> EXECUTION COMPLETED SUCCESSFULLY <<<")


def main():
    """
    Main entry point for the Turing Machine simulation.
    """
    tm = TuringMachine(
        tape_str=INITIAL_TAPE,
        initial_state=INITIAL_STATE,
        halt_state=HALT_STATE,
        blank=BLANK_SYMBOL,
        rules=TRANSITION_RULES
    )
    tm.run()


if __name__ == "__main__":
    main()
