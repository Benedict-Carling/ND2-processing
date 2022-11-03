import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input nd2 file path to process", type=str)
parser.parse_args()

args = parser.parse_args()
print(args.input)
