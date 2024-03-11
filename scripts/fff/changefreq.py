"""
Script to change the frequency of the Flipper SubGhz file.

Example usage: python3 changefreq.py -f tesla.sub -o tesla_new.sub -r 433.92
"""

import sys
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
	"""Parse arguments."""
	parser = argparse.ArgumentParser(description="Change the frequency of the SubGhz FFF file.")
	args = None if sys.argv[1:] else ["-h"]
	parser.add_argument(
		"-f", "--file",
		dest="fin",
		required=True,
		help="input file"
	)
	parser.add_argument(
		"-o", "--outfile",
		dest="fout",
		required=True,
		help="output file"
	)
	parser.add_argument(
		"-r", "--newfreq",
		dest="newfreq",
		required=True,
		help="new frequency, can be decimal or whole: 433.92, 315, etc."
	)
	return parser.parse_args(args)


def check_file(filename: str) -> bool:
	"""Check if input file exists."""
	check = Path(filename).is_file()
	if not check:
		print(f"File not found: {filename}")
	return check


def frfr2wn(newfreq: str) -> str:
	"""Convert the fractional frequency to a whole number.

	E.g.: 433.92 becomes 433920000.
	"""
	if "." in newfreq:
		freq_bits = newfreq.split(".")
		newnewfreq = freq_bits[0] + freq_bits[1] + ("0" * (6 - len(freq_bits[1])))
	else:
		newnewfreq = newfreq + ("0" * 6)
	return newnewfreq


def write_file(file_input: Path, file_output: Path, newfreq: str) -> None:
	"""Read file and copy it to the new one."""
	input_data = ""
	with open(file_input, "r", encoding="utf-8") as f:
		input_data = f.read()
	with open(file_output, "w", encoding="utf-8") as f:
		for line in input_data.splitlines():
			# if the line contains frequency, replace it with the correct one
			w_line = f"Frequency: {newfreq}" if "Frequency" in line else line
			f.write(f"{w_line}\n")
	print("Successfully wrote file", file_output)


def main(args: argparse.Namespace) -> None:
	print("\n", end="")
	if not check_file(args.fin):
		sys.exit(1)
	write_file(Path(args.fin), Path(args.fout), frfr2wn(args.newfreq))


if __name__ == "__main__":
	main(parse_args())
