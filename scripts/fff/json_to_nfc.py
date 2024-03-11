"""
Script to convert proxmark JSON output to Flipper Mifare Classic NFC File Format.

Example usage: python3 json_to_nfc.py -i proxmark.json -o flipper.nfc
"""

import sys
import json
import argparse
from pathlib import Path
from textwrap import dedent


def parse_args() -> argparse.Namespace:
	"""Parse arguments."""
	parser = argparse.ArgumentParser(
		description="Convert proxmark JSON output to Flipper Mifare classic NFC File Format."
	)
	args = None if sys.argv[1:] else ["-h"]
	parser.add_argument(
		"-i", "--input",
		dest="fin",
		required=True,
		help="input file"
	)
	parser.add_argument(
		"-o", "--output",
		dest="fout",
		required=True,
		help="output file"
	)
	parser.add_argument(
		"-k", "--keys-only",
		action="store_true",
		help="only output keys"
	)
	return parser.parse_args(args)


def add_spaces_to_hex(in_str: str) -> str:
	"""Converts something like 'AB00BA' to 'AB 00 BA'."""
	out_str = ""
	for i in range(0, len(in_str), 2):
		out_str += in_str[i:i+2] + " "
	return out_str.strip()


def guess_mifare_size_by_sak(SAK: str) -> str | None:
	"""Guess Mifare size by the SAK value."""
	match SAK:
		case "18":
			r = "4K"
		case "08":
			r = "1K"
		case _:
			r = None
	return r


def convert(fin: str, fout: str, keys_only: bool) -> None:
	"""Do the conversion from .json to .nfc file."""
	data = ""
	with open(Path(fin), "r", encoding="utf-8") as f:
		data = json.load(f)
	if keys_only:
		# just output the keys to a file
		with open(Path(fout), "w") as f:
			for sector in data["SectorKeys"]:
				f.write(data)
	else:
		with open(Path(fout), "w") as f:
			# determine Mifare size and blocks
			m_size = guess_mifare_size_by_sak(data["Card"]["SAK"])
			if not m_size:
				print("Could not determine Mifare size, exiting..")
				sys.exit(1)
			m_blocks = []
			for block in range(0, len(data["blocks"])):
				m_blocks.append("Block " + str(block) + ": " + add_spaces_to_hex(data["blocks"][str(block)]))
			# form Mifare data to be written
			m_data = """\
				Filetype: Flipper NFC device
				Version: 2
				# Nfc device type can be UID, Mifare Ultralight, Mifare Classic, Bank card
				Device type: Mifare Classic
				# UID, ATQA and SAK are common for all formats
				UID: {}
				ATQA: {}
				SAK: {}
				# Mifare Classic specific data
				Mifare Classic type: {}
				# Mifare Classic blocks
				{}
			""".format(
				add_spaces_to_hex(data["Card"]["UID"]),
				add_spaces_to_hex(data["Card"]["ATQA"]),
				add_spaces_to_hex(data["Card"]["SAK"]),
				m_size,
				# 4 tabs are artificially indented here so that
				# `dedent()` can properly format this part
				# with the data piece above
				# (each line in the above part also uses 4 tabs for indents)
				"\n\t\t\t\t".join(m_blocks)
			)
			# write the formatted data
			f.write(dedent(m_data))


def main(args: argparse.Namespace) -> None:
	print("\n", end="")
	convert(**vars(args))


if __name__ == "__main__":
	main(parse_args())
