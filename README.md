# pn-cho

[![PyPI - Version](https://img.shields.io/pypi/v/pn-cho)](https://pypi.org/project/pn-cho/)
[![GitHub License](https://img.shields.io/github/license/pokeghosst/pn-cho)](/COPYING.LESSER)
[![GitHub Release](https://img.shields.io/github/v/release/pokeghosst/pn-cho)](https://github.com/pokeghosst/pn-cho/releases)

> A Python library for testing pseudo-noise sequences

## Install

```bash
pip install pn-cho
```

## Developing

```bash
poetry install
eval $(poetry env activate)
python

# Inside REPL
import pn_sequence
pn_sequence.is_first_postulate_true("011001000111101") # etc.
```

## Testing

```bash
poetry run pytest
```

For coverage:

```bash
poetry run pytest --cov=pn_sequence tests/
```

## Contributing

Contributions are welcome. Please fork the project and use feature a feature branch. For bugs and suggestions, please open an issue.

## License

The project is licensed under the GNU Lesser General Public License. See [LICENSE](/LICENSE) for full terms.

## Golomb's randomness postulates

Golomb's randomness postulates describe properties that can be found in a random sequence. A periodic binary sequence that satisfies all three postulates is a pseudo-noise (PN) or pseudo-random sequence -- it has noise-like properties and appears random, even though it was generated deterministically. PN sequences can be used for various applications, including signal synchronization, navigation, radar ranging, random number generation, spread-spectrum communications, and cryptography (Helleseth and Kumar, 1999).

E.g.: Take sequence `0011101`.

### Postulate 1

_In the cycle s^N of s, the number of 1's differs from the number of 0's by at most 1 (Menezes, Van Oorschot and Vanstone, 2018)_

Count 1's and 0's:

```
N_0 = 3
N_1 = 4
```

Find the difference:

```
|N_0 - N_1| = |3 - 4| = 1
```

The first postulate is satisfied.

### Postulate 2

_In the cycle, at least half the runs have length 1, at least one-fourth have length 2, at least one-eighth have length 3, etc., as long as the number of runs so indicated exceeds 1. (Menezes, Van Oorschot and Vanstone, 2018)_

Mark and count runs:

```
00 | 111 | 0 | 1
```

Calculate run lengths:

```
Run   | Length
---------------
00    |  2
111   |  3
0     |  1
1     |  1
```

For a sequence with 4 runs, the the required number of runs is as follows:

```
Run length | Number of runs
---------------------------
1          |  4 / 2 = 2
2          |  4 / 4 = 1
3          |  4 / 8 = 0.5
```

We have 2 runs of length 1, 1 run of length 2, and 1 run of length 3. Now compare actual number of runs with required:

```
Length | Actual | Required
--------------------------
  1    |   2    |   2.00
  2    |   1    |   1.00
  3    |   1    |   0.50
```

All runs pass the requirement. The second postulate is satisfied.

### Postulate 3

_The autocorrelation function C(t) is two-valued. (Menezes, Van Oorschot and Vanstone, 2018)_

In other words, when the sequence is compared with shifted versions of itself, it either correlates perfectly (at zero shift) or maintains a constant correlation at all other shifts.

```
Shift 0:  0|0|1|1|1|0|1
          0|0|1|1|1|0|1
          -------------
Difference:       = 0 bits

Shift 1:  0|0|1|1|1|0|1
          1|1|1|0|1|0|0
          ^ ^   ^     ^
Difference:       = 4 bits

Shift 2:  0|1|1|1|0|1|0
          1|1|1|0|1|0|0
          ^     ^ ^ ^
Difference:       = 4 bits

Shift 3:  1|1|1|0|1|0|0
          1|1|0|1|0|0|1
              ^ ^ ^   ^
Difference:       = 4 bits

Shift 4:  1|1|0|1|0|0|1
          1|0|1|0|0|1|1
            ^ ^ ^   ^
Difference:       = 4 bits

Shift 5:  1|0|1|0|0|1|1
          0|1|0|0|1|1|1
          ^ ^ ^   ^
Difference:       = 4 bits

Shift 6:  0|1|0|0|1|1|1
          1|0|0|1|1|1|0
          ^ ^   ^     ^
Difference:       = 4 bits
```

Constant Hamming distance for all non-zero shifts means the second value of the autocorrelation function is constant as well. Thus, the third postulate is satisfied.

## References

1. Menezes, A.J., Van Oorschot, P.C. and Vanstone, S.A. (2018) Handbook of Applied Cryptography. 1st edn. CRC Press. Available at: https://doi.org/10.1201/9780429466335.
2. Pinaki, M. (no date) ‘Golomb’s Randomness Postulates’. Available at: https://www.iitg.ac.in/pinaki/Golomb.pdf.
3. Helleseth, T., Kumar, P.V. (1999) “Pseudonoise Sequences” Mobile Communications Handbook Ed. Suthan S. Suthersan Boca Raton: CRC Press LLC
