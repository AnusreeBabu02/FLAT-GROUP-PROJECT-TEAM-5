"""Single-tape Turing Machine that turns a binary string into its 2's complement.

Usage:  python tm_simulator.py 101100        # run with a step-by-step trace
        python tm_simulator.py --verify      # check all strings up to length 12
"""
import sys
from itertools import product

BLANK = '#'
# DELTA[(state, symbol)] = (next state, written symbol, head move)
DELTA = {
    ('q0', '0'): ('q0', '0', 'R'), ('q0', '1'): ('q0', '1', 'R'), ('q0', BLANK): ('q1', BLANK, 'L'),
    ('q1', '0'): ('q1', '0', 'L'), ('q1', '1'): ('q2', '1', 'L'), ('q1', BLANK): ('q3', BLANK, 'R'),
    ('q2', '0'): ('q2', '1', 'L'), ('q2', '1'): ('q2', '0', 'L'), ('q2', BLANK): ('q3', BLANK, 'R'),
}


def run(w):
    """Return (output, steps, configurations) for input string w."""
    tape, head, state, steps = list(BLANK + w + BLANK), 1, 'q0', 0
    configs = []

    def snapshot():
        configs.append(''.join(tape[:head]) + '[' + state + ']' + ''.join(tape[head:]))

    snapshot()
    while state != 'q3':
        state, symbol, move = DELTA[(state, tape[head])]
        tape[head] = symbol
        head += 1 if move == 'R' else -1
        steps += 1
        snapshot()
    return ''.join(tape).strip(BLANK), steps, configs


def twos_complement(w):
    """Reference answer: (2^n - value) mod 2^n written in n bits."""
    n = len(w)
    return '' if n == 0 else format((-int(w, 2)) % (1 << n), '0%db' % n)


def verify(max_len=12):
    count = 0
    for n in range(max_len + 1):
        for bits in product('01', repeat=n):
            w = ''.join(bits)
            out, steps, _ = run(w)
            assert out == twos_complement(w), w
            assert steps == 2 * n + 2, w
            count += 1
    print(f'All {count} strings up to length {max_len} verified.')


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else '101100'
    if arg == '--verify':
        verify()
    else:
        if set(arg) - {'0', '1'}:
            sys.exit('Input must contain only 0 and 1.')
        out, steps, configs = run(arg)
        print('\n'.join(configs))
        print(f'Output: {out}  ({steps} steps)')
