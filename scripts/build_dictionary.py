import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCE = ROOT / "dictionary.txt"
OUTPUT = ROOT / "data" / "dictionary.json"

IPA_MAP = {
    "â̈": "æː",
    "ô̈": "œː",
    "û̈": "ʏː",
    "â": "aː",
    "î": "iː",
    "û": "uː",
    "ê": "eː",
    "ô": "oː",
    "ä": "æ",
    "ö": "œ",
    "ü": "ʏ",
    "a": "a",
    "b": "b",
    "c": "t͡ʃ",
    "d": "d",
    "e": "e",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "i",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o",
    "p": "p",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "d͡ʒ",
    "z": "z"
}

TYPE_MAP = {
    "a": "Prefix",
    "i": "Infix",
    "u": "Suffix"
}

TOKENS = sorted(IPA_MAP, key=len, reverse=True)


def convert_ipa(word):
    word = unicodedata.normalize("NFC", word)
    result = []
    i = 0

    while i < len(word):
        for token in TOKENS:
            if word.startswith(token, i):
                result.append(IPA_MAP[token])
                i += len(token)
                break
        else:
            raise ValueError(f"Unknown character: {word[i]}")

    return "".join(result)


def main():
    entries = []
    seen = set()

    for line_number, line in enumerate(
        SOURCE.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip() or line.startswith("#"):
            continue

        parts = line.split(maxsplit=1)

        if len(parts) != 2:
            raise ValueError(f"Invalid line: {line_number}")

        affix = unicodedata.normalize("NFC", parts[0])
        meaning = parts[1].strip()

        if affix in seen:
            raise ValueError(f"Duplicate affix: {affix}")

        seen.add(affix)

        final_vowel = affix[-1]

        if final_vowel not in TYPE_MAP:
            raise ValueError(f"Invalid affix ending: {affix}")

        entries.append({
            "affix": affix,
            "type": TYPE_MAP[final_vowel],
            "ipa": convert_ipa(affix),
            "meaning": meaning
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()