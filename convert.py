#!/usr/bin/env python
""" Script that extracts entries from a zerospeech leaderboard into individual entries """

import argparse
from ast import arg
from datetime import datetime
from pathlib import Path
import json
import sys
from typing import List, Dict, Union

try:
    import yaml
except ImportError:
    raise ImportError(
        "\n\tPyYAML library not found within current python installation."
        "\n\tYAML files not be supported."
        "\n\tplease run: pip --user install PyYAML\n"
    )


def yaml2json(in_file: Path, out_file: Path):
    with in_file.open() as fp:
        obj = yaml.load(fp, Loader=yaml.FullLoader)

    with out_file.open('w') as fp:
        json.dump(obj, fp, indent=4)


def json2yaml(in_file: Path, out_file: Path):
    with in_file.open() as fp:
        obj = json.load(fp)

    with out_file.open('w') as fp:
        yaml.dump(obj, fp)

    
def arguments():
    """ command line arguments """
    parser = argparse.ArgumentParser(
        "Extract each entry of a leaderboard into individual entries"
    )
    parser.add_argument('action', choices=['json2yaml', 'yaml2json'])
    parser.add_argument('entry_file')
    parser.add_argument('-o', '--output', help="output file (default: same as entry)")

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    entry_file = Path(args.entry_file)

    if not entry_file.is_file():
        raise ValueError(f'File {entry_file} does not exist')

    if args.output:
        output_file = Path(args.output)
    else:
        output_file = entry_file

    if args.action == 'json2yaml':
        json2yaml(entry_file, output_file.with_suffix('.yaml'))

    elif args.action == 'yaml2json':
        yaml2json(entry_file, output_file.with_suffix('.json'))
    
    else:
        raise ValueError('Unknown action !!!')