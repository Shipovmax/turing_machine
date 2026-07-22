# TuringPy

A clean, object-oriented Turing Machine simulator in Python.  
Define any transition table, watch the machine step through the tape in real time, and experiment with classical computability problems.

---

## What's Included

Two independent machines in one repo:

**`main.py` — General-purpose Turing Machine**  
A configurable simulator with a registry of built-in example machines, selectable from the command line:

| Machine | What it does |
|---------|--------------|
| `palindrome` *(default)* | Accepts binary palindromes by erasing matched characters from both ends until the tape is empty |
| `inverter` | Flips every bit on the tape: `0` ↔ `1` |

**`PalindromeMachine.py` — Dedicated palindrome checker**  
A simpler two-pointer implementation that walks inward from both ends of the tape. Accepts or rejects in O(n/2) steps with clear console output.

---

## Features

- **Dictionary-based tape** — theoretically infinite in both directions; cells outside the initial string default to the blank symbol
- **Step-by-step console visualisation** — tape content, head position (`^`), current state, and step counter on every transition
- **Command-line interface** — pick a machine, supply your own tape, control the animation speed
- **Proper reject semantics** — a missing transition rule is a normal halt (input rejected), not a crash; malformed rules still raise `ValueError`
- **Tested** — pytest suite covering acceptance, rejection, tape output, and error handling
- **No external dependencies** — stdlib only (`argparse`, `time`, `typing`)

---

## Requirements

Python 3.7+ (pytest is only needed to run the tests)

---

## Usage

```bash
git clone https://github.com/Shipovmax/TuringPy
cd TuringPy

python main.py                              # palindrome machine, example tape
python main.py --list-machines              # see available example machines
python main.py -m inverter -t 1100          # invert your own tape
python main.py -m palindrome -t 10101 -d 0  # run at full speed (no animation)

python PalindromeMachine.py -t 10101        # two-pointer palindrome checker
```

| Flag | Description |
|------|-------------|
| `-m, --machine` | Example machine to run (`palindrome`, `inverter`) |
| `-t, --tape` | Initial tape content |
| `-d, --delay` | Seconds between steps; `0` disables the animation |
| `--list-machines` | List available example machines and exit |

---

## Defining Your Own Machine

Add an entry to `EXAMPLE_MACHINES` in `main.py`:

```python
EXAMPLE_MACHINES["my-machine"] = {
    "description": "What it does.",
    "tape": "1100",
    "rules": {
        # 'current_state char': 'next_state write_char movement'
        "q0 0": "q0 1 R",   # read 0 -> write 1, move right, stay in q0
        "q0 1": "q0 0 R",   # read 1 -> write 0, move right, stay in q0
        "q0 #": "qf # N",   # blank -> halt
    },
}
```

Movement options: `R` (right), `L` (left), `N` (no move).  
The machine **accepts** when it reaches the halt state `qf` and **rejects** when no rule matches the current `(state, char)` pair.

---

## How It Works

```
Init: tape dict {0:'1', 1:'0', 2:'1', ...}, head=0, state=q0

Each step:
  1. Read  tape[head_position]  (blank if key missing)
  2. Look up  (state, char)  in the transition rules
  3. Write new char, update state, move head
  4. Repeat until state == HALT_STATE or no rule matches
```

The tape is stored as `Dict[int, str]` so the head can move arbitrarily far left (negative indices) or right without pre-allocating memory.

---

## Tests

```bash
pip install pytest
pytest
```

The suite covers both machines: palindrome acceptance/rejection (including odd-length and empty tapes), bit inversion results, tape erasure, and error handling for malformed rules.

---

## Code Standards

- PEP 8 formatting
- Type hints on all public methods
- Docstrings on `TuringMachine` class and every method

---

## License

This project is licensed under the [MIT License](LICENSE).
