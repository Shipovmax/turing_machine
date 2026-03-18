# Turing Machine Simulator

A clean, object-oriented implementation of a 1D Turing Machine in Python. This project simulates the fundamental computational model, allowing users to define their own states, transition rules, and initial tape configurations.

## Features

- **Object-Oriented Design**: Encapsulates the Turing Machine logic within a dedicated `TuringMachine` class.
- **Dynamic Tape**: Uses a dictionary-based tape implementation, allowing for theoretically infinite expansion in both directions.
- **Visual Feedback**: Provides a step-by-step console visualization of the tape, head position, and current state.
- **Configurable Rules**: Easily define custom transition rules using a simple string-based format.

## Requirements

- Python 3.6+

## Getting Started

### Installation

No external dependencies are required. Simply clone the repository or download the `main.py` file.

```bash
git clone https://github.com/your-username/turing-machine.git
cd turing-machine
```

### Running the Simulator

Execute the main script to start the simulation:

```bash
python main.py
```

## Configuration

You can customize the machine's behavior by modifying the constants at the top of `main.py`:

- `INITIAL_TAPE`: The starting string on the tape.
- `INITIAL_STATE`: The entry point for the machine (e.g., `"q0"`).
- `HALT_STATE`: The state that signals successful completion (e.g., `"qf"`).
- `BLANK_SYMBOL`: The character representing an empty cell (e.g., `"#"`).
- `TRANSITION_RULES`: A dictionary where keys are `"state char"` and values are `"next_state next_char movement"`.
    - **Movement options**: `R` (Right), `L` (Left), `N` (None).

### Example Transition Rule

```python
TRANSITION_RULES = {
    'q0 0': 'q0 1 R', # If state is q0 and char is 0, write 1, stay in q0, move Right
    'q0 1': 'q0 0 R', # If state is q0 and char is 1, write 0, stay in q0, move Right
    'q0 #': 'qf # N'  # If state is q0 and char is blank, halt
}
```

## How It Works

1. **Initialization**: The machine starts at `head_position = 0` with the `INITIAL_STATE`.
2. **Lookup**: For each step, it looks up the rule corresponding to the current state and the character under the head.
3. **Action**: It writes a new character, transitions to a new state, and moves the head.
4. **Halt**: The process repeats until the `HALT_STATE` is reached or no valid rule is found (error).

## Code Quality Standards

This project follows:
- **PEP 8**: Python style guidelines.
- **Type Hinting**: Improved code clarity and IDE support.
- **Docstrings**: Clear documentation for all classes and methods.
