import sys
import traceback
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from ..misc import StrParser
from ..models import Benchmark
from ..models.sLM21 import SLM21, SLM21Entry

# data parser
p = StrParser()


def modernize_slm21_entry(entry: Path) -> SLM21Entry:
    data = p.load(entry)
    desc = data['more']['description']

    # leaderboard extras
    lexical_by_frequency = data['more'].get('lexical', {}).get('by_frequency', [])
    lexical_by_length = data['more'].get('lexical', {}).get('by_length', [])
    syntactic = data['more'].get('syntactic', [])
    semantic = data['more'].get('semantic', [])
    extras = dict(
        lexical=dict(
            by_frequency=[
                dict(
                    frequency=p.str(v=item['frequency']),
                    dev_score=p.float(v=item['score_dev']),
                    dev_std=p.float(v=item['std_dev']),
                    dev_n=p.float(v=item['n_dev']),
                    test_score=p.float(v=item['score_test']),
                    test_std=p.float(v=item['std_test']),
                    test_n=p.float(v=item['n_test'])
                )
                for item in lexical_by_frequency
            ],
            by_length=[
                dict(
                    length=p.int(v=item['length']),
                    dev_score=p.float(v=item['score_dev']),
                    dev_std=p.float(v=item['std_dev']),
                    dev_n=p.float(v=item['n_dev']),
                    test_score=p.float(v=item['score_test']),
                    test_std=p.float(v=item['std_test']),
                    test_n=p.float(v=item['n_test'])
                )
                for item in lexical_by_length
            ]
        ),
        syntactic=[
            dict(
                typeset=p.str(v=item['type']),
                dev_score=p.float(v=item['score_dev']),
                dev_std=p.float(v=item['std_dev']),
                dev_n=p.float(v=item['n_dev']),
                test_score=p.float(v=item['score_test']),
                test_std=p.float(v=item['std_test']),
                test_n=p.float(v=item['n_test'])
            )
            for item in syntactic
        ],
        semantic=[
            dict(
                set=p.str(v=item['set']),
                dataset=p.str(v=item['dataset']),
                librispeech=p.float(v=item['librispeech']),
                synthetic=p.float(v=item['synthetic'])
            )
            for item in semantic
        ]
    )

    # leaderboard scores
    scores = dict(
        lexical=dict(
            in_vocab=dict(
                dev=p.float(v=data['lexical_invocab'][0]),
                test=p.float(v=data['lexical_invocab'][1])
            ),
            all=dict(
                dev=p.float(v=data['lexical_all'][0]),
                test=p.float(v=data['lexical_all'][1])
            ),
        ),
        syntactic=dict(
            dev=p.float(v=data['syntactic'][0]),
            test=p.float(v=data['syntactic'][1])
        ),
        semantic=dict(
            normal=dict(
                synthetic=dict(
                    dev=p.float(v=data['semantic_synthetic'][0]),
                    test=p.float(v=data['semantic_synthetic'][1]),
                ),
                librispeech=dict(
                    dev=p.float(v=data['semantic_librispeech'][0]),
                    test=p.float(v=data['semantic_librispeech'][1]),
                )
            ),
            weighted=dict(
                synthetic=dict(
                    dev=p.float(v=data['weighted_semantic_synthetic'][0]),
                    test=p.float(v=data['weighted_semantic_synthetic'][1]),
                ),
                librispeech=dict(
                    dev=p.float(v=data['weighted_semantic_librispeech'][0]),
                    test=p.float(v=data['weighted_semantic_librispeech'][1]),
                )
            ),
        ),
    )

    # submission details
    params = desc.get('parameters', {})
    details = dict(
        train_set=p.str(v=desc['train_set']),
        benchmarks=[Benchmark.sLM_21, Benchmark.ABX_LS],
        gpu_budget=p.int(v=desc['gpu_budget']),
        parameters=dict(
            phonetic=dict(
                frame_shift=params.get('phonetic', {}).get('frame_shift', '-'),
                metric=params.get('phonetic', {}).get('metric', '-')
            ),
            semantic=dict(
                metric=params.get('semantic', {}).get('metric', '-'),
                pooling=params.get('semantic', {}).get('pooling', '-')
            ),
            visually_grounded=p.bool(v=desc.get('visually_grounded', 'false'))
        )
    )

    # publication details
    publication = dict(
        open_science=p.bool(v=desc['open_source']),
        author_short=p.str(v=data['author_label']),
        author=p.str(v=desc['author']),
        institution=p.str(v=desc['affiliation'])
    )

    return SLM21Entry(**dict(
        submission_date=p.datetime(v=desc["submitted_at"]),
        model_id="",
        submission_id="",
        index=data['index'],
        description=desc["description"],
        publication=publication,
        details=details,
        scores=scores,
        extras=extras,
    ))


def modernize_slm21(location: Path, file_type='.yaml') -> SLM21:
    data = []

    for item in location.rglob(f"*{file_type}"):
        try:
            data.append(modernize_slm21_entry(item))
        except (ValueError, ValidationError, KeyError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
            continue

    return SLM21(
        last_modified=datetime.now(),
        data=data
    )
