#!/usr/bin/env python
""" Script that packs individual entries from a zerospeech leaderboard into a single leaderboard object """
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
        "Pack a list of leaderboard entries into a single leaderboard file"
    )
    parser.add_argument('entries_location')
    parser.add_argument('-o', '--output-file', help="Location of output file", default='leaderboard.json')
    parser.add_argument('-t', '--file-type', choices=['yaml', 'json'], default="json",
                        help="type of output (default: yaml)")
    return parser.parse_args()


def load_from_entries(_location: Path):
    entries = []
    
    def sort_key(x):
        try:
            return int(x)
        except ValueError:
            return x

    if yaml is None:
        print("PyYAML not found skipping *.yaml files!!")
    else:
        yaml_items = list(_location.rglob("*.yaml"))
        for entry in sorted(yaml_items, key=lambda x: sort_key(x.stem)):
            with entry.open() as f:
                entries.append(yaml.load(f, Loader=yaml.FullLoader))

    json_items = list(_location.rglob("*.json"))
    for entry in sorted(json_items, key=lambda x: sort_key(x.stem)):
        with entry.open() as f:
            entries.append(json.load(f))

    return dict(
        updatedOn=datetime.now().isoformat(),
        data=entries
    )


if __name__ == '__main__':
    args = arguments()
    entries_location = Path(args.entries_location)
    output_leaderboard = Path(args.output_file)

    if not entries_location.is_dir():
        raise ValueError(f'File {entries_location} does not exist')

    leaderboard_data = load_from_entries(entries_location)
    output_leaderboard = output_leaderboard.with_suffix(f'.{args.file_type}')

    with output_leaderboard.open('w') as fp:
        if args.file_type == 'yaml' and yaml is not None:
            yaml.dump(leaderboard_data, fp)
        elif args.file_type == 'json':
            json.dump(leaderboard_data, fp, indent=4)
        else:
            raise ValueError('Unknown export type (or yaml not installed !!)')
