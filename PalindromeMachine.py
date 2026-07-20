import time

INITIAL_TAPE = "1001"

DELAY = 0.4


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

    def run(self) -> None:
        print("--- PALINDROME CHECK STARTED ---")
        self.display()

        while True:
            result = self.step()

            if result == "ACCEPT":
                print("--- IT IS PALINDROME ---")
                break

            if result == "REJECT":
                print("--- IT IS NOT PALINDROME ---")
                break

            time.sleep(DELAY)
            self.display()


def main() -> None:
    machine = PalindromeMachine(INITIAL_TAPE)
    machine.run()


if __name__ == "__main__":
    main()
