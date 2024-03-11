"""
Script that imports a FFF subghz file and draws a timing graph.

Example line:
RAW_Data: 379 -798 807 -404 377 -798 805 -802 405 -396 393 -396 397 -394 .
Where the numbers are the timings between changes from 0 to 1 and vice versa.
Positive numbers are rising edges, negative numbers are falling edges.
"""

import sys
import argparse
from pathlib import Path
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
	"""Parse arguments."""
	parser = argparse.ArgumentParser(description="Draw a subghz file.")
	args = None if sys.argv[1:] else ["-h"]
	parser.add_argument(
		"-f", "--file",
		dest="filename",
		required=True,
		help="subghz file to draw"
	)
	return parser.parse_args(args)


def draw_out(filename: str) -> None:
	"""Draw out the timing graph."""
	# read in the file
	with open(Path(filename), "r", encoding="utf-8") as f:
		lines = f.readlines()
	# trim the lines
	data = []
	for line in lines:
		if "RAW_Data:" in line:
			data.append(line.split("RAW_Data: ")[1].strip())
	# split the data into a list of individual timings
	timings = []
	for line in data:
		timings.extend((int(x) for x in line.split()))
	# convert timings to a stream of 0s and 1s
	stream = []
	for timing in timings:
		if timing > 0:
			for i in range(timing):
				stream.append(1)
		else:
			for i in range(abs(timing)):
				stream.append(0)
	# draw and show the graph
	plt.plot(stream)
	plt.show()


def main(args: argparse.Namespace) -> None:
	print("\n", end="")
	draw_out(args.filename)


if __name__ == "__main__":
	main(parse_args())
