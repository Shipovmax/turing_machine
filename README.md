# TuringPy

A clean, object-oriented Turing Machine simulator in Python.  
Define any transition table, watch the machine step through the tape in real time, and experiment with classical computability problems.

---

## What's Included

Two independent machines in one repo:

**`main.py` — General-purpose Turing Machine**  
Fully configurable via constants at the top of the file. Ships with a palindrome-checker transition table as the default example (erases matched characters from both ends until the tape is empty or a mismatch is found).

**`PalindromeMachine.py` — Dedicated palindrome checker**  
A simpler two-pointer implementation that walks inward from both ends of the tape. Accepts or rejects in O(n/2) steps with clear console output.

---

## Features

- **Dictionary-based tape** — theoretically infinite in both directions; cells outside the initial string default to the blank symbol
- **Step-by-step console visualisation** — tape content, head position (`^`), current state, and step counter on every transition
- **Configurable delay** — adjust `delay` in `run()` or the `DELAY` constant to slow down or speed up the animation
- **Error reporting** — halts with a `CRITICAL ERROR` message if no transition rule is found for the current `(state, char)` pair
- **No external dependencies** — stdlib only (`time`, `typing`)

---

## Requirements

Python 3.6+

---

## Usage

```bash
git clone https://github.com/Shipovmax/turing-machine
cd turing-machine

python main.py               # general Turing Machine
python PalindromeMachine.py  # two-pointer palindrome checker
```

---

## Configuration (`main.py`)

| Constant | Default | Description |
|----------|---------|-------------|
| `INITIAL_TAPE` | `"101010"` | Starting tape content |
| `INITIAL_STATE` | `"q0"` | Entry state |
| `HALT_STATE` | `"qf"` | Accepting/halting state |
| `BLANK_SYMBOL` | `"#"` | Empty cell character |
| `TRANSITION_RULES` | see below | Transition table |

### Transition Rule Format

```python
TRANSITION_RULES = {
    # 'current_state char': 'next_state write_char movement'
    'q0 0': 'q0 1 R',   # read 0 → write 1, move right, stay in q0
    'q0 1': 'q0 0 R',   # read 1 → write 0, move right, stay in q0
    'q0 #': 'qf # N',   # blank → halt
}
```

Movement options: `R` (right), `L` (left), `N` (no move).

### Example — Bit Inverter

```python
INITIAL_TAPE = "1100"

TRANSITION_RULES = {
    'q0 0': 'q0 1 R',
    'q0 1': 'q0 0 R',
    'q0 #': 'qf # N',
}
```

---

## How It Works

```
Init: tape dict {0:'1', 1:'0', 2:'1', ...}, head=0, state=q0

Each step:
  1. Read  tape[head_position]  (blank if key missing)
  2. Look up  (state, char)  in TRANSITION_RULES
  3. Write new char, update state, move head
  4. Repeat until state == HALT_STATE
```

The tape is stored as `Dict[int, str]` so the head can move arbitrarily far left (negative indices) or right without pre-allocating memory.

---

## Code Standards

- PEP 8 formatting
- Type hints on all public methods
- Docstrings on `TuringMachine` class and every method
