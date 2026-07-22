"""Tests for the general Turing Machine and the two-pointer palindrome checker."""

import pytest

from main import (
    BLANK_SYMBOL,
    EXAMPLE_MACHINES,
    HALT_STATE,
    INITIAL_STATE,
    TuringMachine,
)
from PalindromeMachine import PalindromeMachine


def build_machine(name: str, tape: str) -> TuringMachine:
    return TuringMachine(
        tape_str=tape,
        initial_state=INITIAL_STATE,
        halt_state=HALT_STATE,
        blank=BLANK_SYMBOL,
        rules=EXAMPLE_MACHINES[name]["rules"],
    )


class TestInverter:
    @pytest.mark.parametrize(
        "tape, expected",
        [
            ("101010", "010101"),
            ("0000", "1111"),
            ("1", "0"),
        ],
    )
    def test_inverts_every_bit(self, tape, expected):
        machine = build_machine("inverter", tape)
        assert machine.run(delay=0) is True
        assert machine.tape_str() == expected


class TestPalindromeRules:
    @pytest.mark.parametrize("tape", ["101101", "1001", "11", "101", "1", ""])
    def test_accepts_palindromes(self, tape):
        machine = build_machine("palindrome", tape)
        assert machine.run(delay=0) is True

    @pytest.mark.parametrize("tape", ["10", "100", "101100"])
    def test_rejects_non_palindromes(self, tape):
        machine = build_machine("palindrome", tape)
        assert machine.run(delay=0) is False

    def test_erases_tape_while_accepting(self):
        machine = build_machine("palindrome", "1001")
        machine.run(delay=0)
        assert machine.tape_str() == ""


class TestTuringMachineCore:
    def test_missing_rule_halts_without_reaching_halt_state(self):
        machine = TuringMachine(
            tape_str="1",
            initial_state=INITIAL_STATE,
            halt_state=HALT_STATE,
            blank=BLANK_SYMBOL,
            rules={},
        )
        assert machine.run(delay=0) is False
        assert machine.state != HALT_STATE

    def test_malformed_rule_raises(self):
        machine = TuringMachine(
            tape_str="1",
            initial_state=INITIAL_STATE,
            halt_state=HALT_STATE,
            blank=BLANK_SYMBOL,
            rules={"q0 1": "qf 0"},
        )
        with pytest.raises(ValueError):
            machine.step()

    def test_invalid_movement_raises(self):
        machine = TuringMachine(
            tape_str="1",
            initial_state=INITIAL_STATE,
            halt_state=HALT_STATE,
            blank=BLANK_SYMBOL,
            rules={"q0 1": "qf 0 X"},
        )
        with pytest.raises(ValueError):
            machine.step()


class TestTwoPointerChecker:
    @pytest.mark.parametrize("tape", ["1001", "10101", "7", "aa"])
    def test_accepts_palindromes(self, tape):
        assert PalindromeMachine(tape).run(delay=0) is True

    @pytest.mark.parametrize("tape", ["10", "abca"])
    def test_rejects_non_palindromes(self, tape):
        assert PalindromeMachine(tape).run(delay=0) is False
