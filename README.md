# JSON to TOON Converter

A Python script and module to convert JSON files into TOON format (Token-Oriented Object Notation).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/json-to-toon.git
cd json-to-toon
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies (if any, currently none needed):
```bash
pip install -r requirements.txt
```

## Usage

Convert a JSON file to TOON format:

```bash
python json_to_toon.py input.json -o output.toon
```

### Options

- `--indent` : Number of spaces per indentation level (default: 2)
- `--delimiter` : Delimiter for inline/tabular arrays (default: `,`)
- `--length-marker` : Add `#` prefix to array lengths

If the `-o` option is omitted, the TOON output will be printed to stdout.

## Example

```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ]
}
```

Running:

```bash
python json_to_toon.py example.json -o example.toon --length-marker
```

Outputs:

```
[#2]{id,name}:
  1,Alice
  2,Bob
```

## Notes

- Decoding TOON back to JSON is **not yet implemented**.
- Strings containing whitespace, delimiter, or special characters are automatically quoted.