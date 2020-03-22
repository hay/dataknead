#!/usr/bin/env python3
from .knead import Knead
from argparse import ArgumentParser
from os.path import isfile
from pathlib import Path
import logging
import sys

def has_extension(path):
    suffix = Path(path).suffix
    return suffix != ""

def get_parser():
    parser = ArgumentParser(
        description = "Fluently process and convert data formats like JSON and CSV"
    )

    parser.add_argument("input", type=str, nargs="?", help="Input file")
    parser.add_argument("output", type=str, nargs="?", help="Output file")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help = "Show debug information"
    )
    parser.add_argument("--input-format", "-if", type=str, help="Input format")
    parser.add_argument("--output-format", "-of", type=str, help="Output format")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Take data from stdin (requires --input-format)",
    )

    return parser

def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # If there's no input *and* no --stdin, something is wrong
    if args.input == None and args.stdin == False:
        raise Exception("Need an input file or the --stdin argument")
    # Stdin, but no input format
    elif args.input == None and args.stdin == True and args.input_format == None:
        raise Exception("When using --stdin you need to provide --input-format as well")
    # Both stdin *and* a filename
    elif args.input != None and args.stdin == True:
        raise Exception("You can't use both stdin and give a filename")
    # Stdin with an input format, read from stdin
    elif args.input == None and args.stdin == True and args.input_format != None:
        k = Knead(sys.stdin.read(), parse_as=args.input_format)
    # Filename without input type
    elif args.input != None and args.input_format == None:
        # Check if this file has an extension, and if not, give an error
        if not has_extension(args.input):
            raise Exception(
                "Input files need a file extension or the --input-format argument"
            )
        # Does the file exist?
        elif not isfile(args.input):
            raise Exception("File does not exist: %s" % args.input)
        else:
            k = Knead(args.input)
    # Filename with an input type (that we'll use whatever the extension)
    elif args.input != None and args.input_format != None:
        # Does the file exist?
        if not isfile(args.input):
            raise Exception("File does not exist: %s" % args.input)
        else:
            k = Knead(args.input, parse_as=args.input_format)

    # Okay, now let's do some converting!
    # With no output, just print to stdout
    if not args.output:
        print(k)
    # Output file with output format, force that anyway
    elif args.output and args.output_format:
        k.write(args.output, write_as=args.output_format)
    elif args.output and args.output_format == None:
        # Do we have an extension? Otherwise, give error
        if has_extension(args.output):
            k.write(args.output)
        else:
            raise Exception(
                "Filenames without extension require the --output-format argument"
            )

def run():
    parser = get_parser()

    if len(sys.argv) == 1:
        # No arguments, just display help
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()
        main(args)