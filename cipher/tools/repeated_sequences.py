import string
from collections import defaultdict


class RepeatedSequences:
    @staticmethod
    def normalize(text):
        return "".join(
            c.upper() for c in text if c.upper() in string.ascii_uppercase
        )

    @staticmethod
    def find_sequences(text, sequence_length=3):
        text = RepeatedSequences.normalize(text)

        sequences = defaultdict(list)

        for i in range(len(text) - sequence_length + 1):
            seq = text[i:i + sequence_length]
            sequences[seq].append(i)

        repeated = {
            seq: positions
            for seq, positions in sequences.items()
            if len(positions) > 1
        }

        result = []

        for seq, positions in repeated.items():
            distances = []

            for i in range(len(positions) - 1):
                distances.append(positions[i + 1] - positions[i])

            result.append({
                "sequence": seq,
                "count": len(positions),
                "distances": distances,
            })

        result.sort(key=lambda x: x["count"], reverse=True)

        return result[:20]  # limit output