def get_word_pattern(word):
    """
    Convert a word into a reusable letter pattern.

    Examples:
    HELLO -> 0.1.2.2.3
    KHOOR -> 0.1.2.2.3
    TEST -> 0.1.2.0
    """
    word = word.upper()

    next_number = 0
    letter_numbers = {}
    pattern = []

    for letter in word:
        if letter not in letter_numbers:
            letter_numbers[letter] = str(next_number)
            next_number += 1

        pattern.append(letter_numbers[letter])

    return ".".join(pattern)