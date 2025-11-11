import json
import argparse
from toon_converter import encode

def main():
    parser = argparse.ArgumentParser(description="Convert JSON file to TOON format")
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument("-o", "--output", help="Output TOON file path (stdout if omitted)")
    parser.add_argument("--indent", type=int, default=2, help="Indentation spaces per level")
    parser.add_argument("--delimiter", default=",", help="Delimiter for inline/tabular arrays")
    parser.add_argument("--length-marker", action="store_true", help="Use length marker '#' in arrays")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    toon_str = encode(data, indent_size=args.indent, delimiter=args.delimiter, length_marker=args.length_marker)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(toon_str)
    else:
        print(toon_str)

if __name__ == "__main__":
    main()