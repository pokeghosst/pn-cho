"""
This file is part of pn-cho.

pn-cho is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

pn-cho is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with pn-cho.
If not, see <https://www.gnu.org/licenses/>.
"""


def is_first_postulate_true(sequence):
    """Tests whether the sequence satisfies the first postulate

    In the cycle s^N of s, the number of 1's differs from the number of 0's by at most 1.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the first postulate
    """
    z = sequence.count("0")
    o = sequence.count("1")

    if abs(z - o) > 1:
        return False

    return True


def is_second_postulate_true(sequence):
    """Tests whether the sequence satisfies the second postulate

    In the cycle, at least half the runs have length 1, at least one-fourth have length 2,
    at least one-eighth have length 3, etc., as long as the number of runs so indicated exceeds 1.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the second postulate
    """
    streaks = __get_streaks(sequence)
    if not streaks:
        return False

    total_runs = sum(len(indices) for indices in streaks.values())
    if total_runs < 2:
        return False

    streak_lengths = sorted(streaks.keys())

    for i, length in enumerate(streak_lengths):
        expected_min_frequency = total_runs / (2**length)
        actual_frequency = len(streaks[length])

        if expected_min_frequency < 1:
            break

        if actual_frequency < expected_min_frequency:
            return False

    return True


def is_third_postulate_true(sequence):
    """Tests whether the sequence satisfies the second postulate

    The autocorrelation function C(t) is two-valued.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the third postulate
    """
    sequence2 = sequence[1:] + sequence[:1]
    shift1_distance = _hamming_distance(sequence, sequence2)

    for shift in range(2, len(sequence)):
        shifted_seq = sequence[shift:] + sequence[:shift]
        distance = _hamming_distance(sequence, shifted_seq)

        if distance != shift1_distance:
            return False

    return True


def is_pn_sequence(sequence):
    """A shorthand method to test if the sequence is a pseudo-noise sequence,
    satisfying all three postulates.

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence is a pseudo-noise (pn) sequence.

    """
    if not all(char in '01' for char in sequence):
        raise ValueError("Input is not a binary sequence")

    if is_first_postulate_true(sequence) and is_second_postulate_true(sequence) and is_third_postulate_true(sequence):
        return True

    return False


def __get_streaks(sequence):
    streaks = {}
    normalized_seq = sequence

    rotation_index = 0
    while rotation_index < len(sequence):
        if normalized_seq[0] != normalized_seq[-1]:
            break

        normalized_seq = normalized_seq[1:] + normalized_seq[0]
        rotation_index += 1
        if rotation_index >= len(sequence):
            return {}

    normalized_seq += '1' if normalized_seq[0] == '0' else '0'

    current_streak = 1
    for i in range(0, len(normalized_seq)):
        if normalized_seq[i] == normalized_seq[i - 1]:
            current_streak += 1
        else:
            if current_streak not in streaks:
                streaks[current_streak] = []
            streaks[current_streak].append(i - 1)
            current_streak = 1

    return streaks


def _hamming_distance(s1, s2):
    distance = 0
    for i, j in zip(s1, s2):
        if i != j:
            distance += 1

    return distance
