#!/usr/bin/env python
""" Script that extracts entries from a zerospeech leaderboard into individual entries """

import argparse
from datetime import datetime
from pathlib import Path
import json
import sys
from typing import List, Dict, Union

try:
    import yaml
except ImportError:
    print(f"WARNING::{__file__}: "
          "\n\tPyYAML library not found within current python installation."
          "\n\tYAML files will not be supported."
          "\n\tplease run: pip --user install PyYAML\n",
          file=sys.stderr,
          )
    yaml = None


def arguments():
    """ command line arguments """
    parser = argparse.ArgumentParser(
        "Extract each entry of a leaderboard into individual entries"
    )
    parser.add_argument('leaderboard_file')
    parser.add_argument('-o', '--output', help="output location (default: .)")
    parser.add_argument('-t', '--file-type', choices=['yaml', 'json'], default="yaml",
                        help="type of output (default: yaml)")
    return parser.parse_args()


def open_dict(location: Path) -> Union[Dict, List]:
    if location.suffix in ('.yaml', '.yml'):
        if yaml is None:
            raise ValueError('a yaml file was given as input '
                             'but the PyYAML module was not found')

        with leaderboard_file.open() as _fp:
            return yaml.load(_fp, Loader=yaml.FullLoader)

    elif location.suffix in ('.json',):
        with leaderboard_file.open() as _fp:
            return json.load(_fp)

    else:
        raise ValueError('input type not known use [yaml|json]')


def export(_leaderboard: List, _location: Path, export_type: str = 'yaml'):
    if export_type == 'yaml':
        if yaml is None:
            raise ValueError('a yaml file was expected as output '
                             'but the PyYAML module was not found !!')

        for index, entry in enumerate(_leaderboard):
            with (_location / f"{index}.yaml").open('w') as f:
                yaml.dump(entry, f)

    elif export_type == 'json':
        for index, entry in enumerate(_leaderboard):
            with (_location / f"{index}.json").open('w') as f:
                json.dump(entry, f, indent=4)

    else:
        raise ValueError('output type not known use [yaml|json]')


if __name__ == '__main__':
    args = arguments()
    leaderboard_file = Path(args.leaderboard_file)
    output_location = Path(args.output)

    if not leaderboard_file.is_file():
        raise ValueError(f'File {leaderboard_file} does not exist')

    if not output_location.is_dir():
        output_location.mkdir(exist_ok=True, parents=True)

    leaderboard = open_dict(leaderboard_file)

    if 'data' in leaderboard:
        export(leaderboard['data'], output_location, export_type=args.file_type)
    else:
        raise ValueError('input file has no data section not a valid leaderboard')

    if 'updatedOn' in leaderboard:
        updatedOn = leaderboard['updatedOn']
    else:
        updatedOn = datetime.now().isoformat()

    # write updatedOn file
    with (output_location / 'updated_on.txt').open('w') as fp:
        fp.write(f"{updatedOn}\n")
