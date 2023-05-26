import itertools
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from ..misc import StrParser
from ..models import Benchmark
from ..models.tde import TDE15Entry, TDE15, TDE17Entry, TDE17

# data parser
p = StrParser()


def modernize_tde15_entry(entry: Path) -> TDE15Entry:
    data = p.load(entry)
    mdata = data['metadata']
    mscores = data['scores']

    if "DOI" in mdata.keys():
        n_doi = p.doi2(v=mdata["DOI"].strip())
        if n_doi[0]:
            doi = f"10.5281/zenodo.{n_doi[2]}"
        else:
            doi = None
    else:
        doi = None

    if "team" in mdata.keys():
        team = mdata['team']
    else:
        team = ""

    publication = dict(
        author_short=mdata['author'],
        institution=team,
        open_science=False,
        DOI=doi
    )

    details = dict(
        benchmarks=[Benchmark.TDE_15],
        parameters={}
    )

    scores = dict(
        english=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_prec_english']),
                recall=p.float(v=mscores['grouping_rec_english']),
                fscore=p.float(v=mscores['grouping_F_english'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_prec_english']),
                recall=p.float(v=mscores['token_rec_english']),
                fscore=p.float(v=mscores['token_F_english'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_prec_english']),
                recall=p.float(v=mscores['type_rec_english']),
                fscore=p.float(v=mscores['type_F_english'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_prec_english']),
                recall=p.float(v=mscores['boundary_rec_english']),
                fscore=p.float(v=mscores['boundary_F_english'])
            ),
            matching=dict(
                precision=p.float(v=mscores['matching_prec_english']),
                recall=p.float(v=mscores['matching_rec_english']),
                fscore=p.float(v=mscores['matching_F_english'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['NED_english']),
                coverage=p.float(v=mscores['cov_english']),
            )
        ),
        xitsonga=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_prec_xitsonga']),
                recall=p.float(v=mscores['grouping_rec_xitsonga']),
                fscore=p.float(v=mscores['grouping_F_xitsonga'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_prec_xitsonga']),
                recall=p.float(v=mscores['token_rec_xitsonga']),
                fscore=p.float(v=mscores['token_F_xitsonga'])
            ),
            type=dict(
                precision=p.float(v=mscores['token_prec_xitsonga']),
                recall=p.float(v=mscores['token_rec_xitsonga']),
                fscore=p.float(v=mscores['type_F_xitsonga'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_prec_xitsonga']),
                recall=p.float(v=mscores['boundary_rec_xitsonga']),
                fscore=p.float(v=mscores['boundary_F_xitsonga'])
            ),
            matching=dict(
                precision=p.float(v=mscores['matching_prec_xitsonga']),
                recall=p.float(v=mscores['matching_rec_xitsonga']),
                fscore=p.float(v=mscores['matching_F_xitsonga'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['NED_xitsonga']),
                coverage=p.float(v=mscores['cov_xitsonga']),
            )
        )
    )

    return TDE15Entry(**dict(
        description="",
        model_id="",
        index=0,
        submission_id="",
        scores=scores,
        publication=publication,
        details=details,
    ))


def modernize_tde15(location: Path, file_type='.yaml') -> TDE15:
    data = []

    for item in location.rglob(f"*{file_type}"):
        try:
            data.append(modernize_tde15_entry(item))
        except (ValueError, ValidationError, KeyError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
            continue

    return TDE15(
        last_modified=datetime.now(),
        data=data
    )


def modernize_tde17_entry(entry: Path) -> TDE17Entry:
    data = p.load(entry)
    mdata = data['metadata']
    mscores = data['scores']

    if "DOI" in mdata.keys():
        n_doi = p.doi2(v=mdata["DOI"].strip())
        if n_doi[0]:
            doi = f"10.5281/zenodo.{n_doi[2]}"
        else:
            doi = None
    else:
        doi = None

    if "team" in mdata.keys():
        team = mdata['team']
    else:
        team = ""

    publication = dict(
        author_short=mdata['author'],
        institution=team,
        open_science=False,
        DOI=doi
    )

    details = dict(
        benchmarks=[Benchmark.TDE_17],
        parameters={}
    )

    scores = dict(
        english=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_precision_english']),
                recall=p.float(v=mscores['grouping_recall_english']),
                fscore=p.float(v=mscores['grouping_fscore_english'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_precision_english']),
                recall=p.float(v=mscores['token_recall_english']),
                fscore=p.float(v=mscores['token_fscore_english'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_precision_english']),
                recall=p.float(v=mscores['type_recall_english']),
                fscore=p.float(v=mscores['type_fscore_english'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_precision_english']),
                recall=p.float(v=mscores['boundary_recall_english']),
                fscore=p.float(v=mscores['boundary_fscore_english'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['ned_english']),
                coverage=p.float(v=mscores['coverage_english']),
                nwords=p.float(v=mscores['n_words_english']),
                npairs=p.float(v=mscores['n_pairs_english']),
            )
        ),
        french=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_precision_french']),
                recall=p.float(v=mscores['grouping_recall_french']),
                fscore=p.float(v=mscores['grouping_fscore_french'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_precision_french']),
                recall=p.float(v=mscores['token_recall_french']),
                fscore=p.float(v=mscores['type_fscore_french'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_precision_french']),
                recall=p.float(v=mscores['type_recall_french']),
                fscore=p.float(v=mscores['type_fscore_french'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_precision_french']),
                recall=p.float(v=mscores['boundary_recall_french']),
                fscore=p.float(v=mscores['boundary_fscore_french'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['ned_french']),
                coverage=p.float(v=mscores['coverage_french']),
                nwords=p.float(v=mscores['n_words_french']),
                npairs=p.float(v=mscores['n_pairs_french']),
            )
        ),
        mandarin=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_precision_mandarin']),
                recall=p.float(v=mscores['grouping_recall_mandarin']),
                fscore=p.float(v=mscores['grouping_fscore_mandarin'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_precision_mandarin']),
                recall=p.float(v=mscores['token_recall_mandarin']),
                fscore=p.float(v=mscores['token_fscore_mandarin'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_precision_mandarin']),
                recall=p.float(v=mscores['type_recall_mandarin']),
                fscore=p.float(v=mscores['type_fscore_mandarin'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_precision_mandarin']),
                recall=p.float(v=mscores['boundary_recall_mandarin']),
                fscore=p.float(v=mscores['boundary_fscore_mandarin'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['ned_mandarin']),
                coverage=p.float(v=mscores['coverage_mandarin']),
                nwords=p.float(v=mscores['n_words_mandarin']),
                npairs=p.float(v=mscores['n_pairs_mandarin']),
            )
        ),
        german=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_precision_LANG1']),
                recall=p.float(v=mscores['grouping_recall_LANG1']),
                fscore=p.float(v=mscores['grouping_fscore_LANG1'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_precision_LANG1']),
                recall=p.float(v=mscores['token_recall_LANG1']),
                fscore=p.float(v=mscores['token_fscore_LANG1'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_precision_LANG1']),
                recall=p.float(v=mscores['type_recall_LANG1']),
                fscore=p.float(v=mscores['type_fscore_LANG1'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_precision_LANG1']),
                recall=p.float(v=mscores['boundary_recall_LANG1']),
                fscore=p.float(v=mscores['boundary_fscore_LANG1'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['ned_LANG1']),
                coverage=p.float(v=mscores['coverage_LANG1']),
                nwords=p.float(v=mscores['n_words_LANG1']),
                npairs=p.float(v=mscores['n_pairs_LANG1']),
            )
        ),
        wolof=dict(
            grouping=dict(
                precision=p.float(v=mscores['grouping_precision_LANG2']),
                recall=p.float(v=mscores['grouping_recall_LANG2']),
                fscore=p.float(v=mscores['grouping_fscore_LANG2'])
            ),
            token=dict(
                precision=p.float(v=mscores['token_precision_LANG2']),
                recall=p.float(v=mscores['token_recall_LANG2']),
                fscore=p.float(v=mscores['token_fscore_LANG2'])
            ),
            type=dict(
                precision=p.float(v=mscores['type_precision_LANG2']),
                recall=p.float(v=mscores['type_recall_LANG2']),
                fscore=p.float(v=mscores['type_fscore_LANG2'])
            ),
            boundary=dict(
                precision=p.float(v=mscores['boundary_precision_LANG2']),
                recall=p.float(v=mscores['boundary_recall_LANG2']),
                fscore=p.float(v=mscores['boundary_fscore_LANG2'])
            ),
            nlp=dict(
                ned=p.float(v=mscores['ned_LANG2']),
                coverage=p.float(v=mscores['coverage_LANG2']),
                nwords=p.float(v=mscores['n_words_LANG2']),
                npairs=p.float(v=mscores['n_pairs_LANG2']),
            )
        )
    )

    return TDE17Entry(**dict(
        description="",
        model_id="",
        index=0,
        submission_id="",
        scores=scores,
        publication=publication,
        details=details
    ))


def extract_tde17_from_2020(entry: Path) -> TDE17Entry:
    data = p.load(entry)
    entry_data = data['track2_2017']
    mdata = data['metadata']

    publication = dict(
        author=mdata["author"],
        author_short=mdata['author'],
        institution=mdata['affiliation'],
        open_science=p.bool(v=mdata['open_source']),
    )

    mdata2 = entry_data['metadata']
    details = dict(
        benchmarks=[Benchmark.TDE_17],
        parameters=dict(
            hyperparameters=mdata2['hyperparameters']
        )
    )

    english_scores = entry_data['english']['scores']
    english_scores.update(entry_data['english']['details'])

    french_scores = dict(**entry_data['french']['scores'])
    french_scores.update(entry_data['french']['details'])

    mandarin_scores = dict(**entry_data['mandarin']['scores'])
    mandarin_scores.update(entry_data['mandarin']['details'])

    german_scores = dict(**entry_data['LANG1']['scores'])
    german_scores.update(entry_data['LANG1']['details'])

    wolof_scores = dict(**entry_data['LANG2']['scores'])
    wolof_scores.update(entry_data['LANG2']['details'])

    scores = dict(
        english=dict(
            grouping=dict(
                precision=p.float(v=english_scores['grouping_precision']),
                recall=p.float(v=english_scores['grouping_recall']),
                fscore=p.float(v=english_scores['grouping_fscore'])
            ),
            token=dict(
                precision=p.float(v=english_scores['token_precision']),
                recall=p.float(v=english_scores['token_recall']),
                fscore=p.float(v=english_scores['token_fscore'])
            ),
            type=dict(
                precision=p.float(v=english_scores['type_precision']),
                recall=p.float(v=english_scores['type_recall']),
                fscore=p.float(v=english_scores['type_fscore'])
            ),
            boundary=dict(
                precision=p.float(v=english_scores['boundary_precision']),
                recall=p.float(v=english_scores['boundary_recall']),
                fscore=p.float(v=english_scores['boundary_fscore'])
            ),
            nlp=dict(
                ned=p.float(v=english_scores['ned']),
                coverage=p.float(v=english_scores['coverage']),
                nwords=p.float(v=english_scores['words']),
                npairs=p.float(v=english_scores['pairs']),
            )
        ),
        french=dict(
            grouping=dict(
                precision=p.float(v=french_scores['grouping_precision']),
                recall=p.float(v=french_scores['grouping_recall']),
                fscore=p.float(v=french_scores['grouping_fscore'])
            ),
            token=dict(
                precision=p.float(v=french_scores['token_precision']),
                recall=p.float(v=french_scores['token_recall']),
                fscore=p.float(v=french_scores['token_fscore'])
            ),
            type=dict(
                precision=p.float(v=french_scores['type_precision']),
                recall=p.float(v=french_scores['type_recall']),
                fscore=p.float(v=french_scores['type_fscore'])
            ),
            boundary=dict(
                precision=p.float(v=french_scores['boundary_precision']),
                recall=p.float(v=french_scores['boundary_recall']),
                fscore=p.float(v=french_scores['boundary_fscore'])
            ),
            nlp=dict(
                ned=p.float(v=french_scores['ned']),
                coverage=p.float(v=french_scores['coverage']),
                nwords=p.float(v=french_scores['words']),
                npairs=p.float(v=french_scores['pairs']),
            )
        ),
        mandarin=dict(
            grouping=dict(
                precision=p.float(v=mandarin_scores['grouping_precision']),
                recall=p.float(v=mandarin_scores['grouping_recall']),
                fscore=p.float(v=mandarin_scores['grouping_fscore'])
            ),
            token=dict(
                precision=p.float(v=mandarin_scores['token_precision']),
                recall=p.float(v=mandarin_scores['token_recall']),
                fscore=p.float(v=mandarin_scores['token_fscore'])
            ),
            type=dict(
                precision=p.float(v=mandarin_scores['type_precision']),
                recall=p.float(v=mandarin_scores['type_recall']),
                fscore=p.float(v=mandarin_scores['type_fscore'])
            ),
            boundary=dict(
                precision=p.float(v=mandarin_scores['boundary_precision']),
                recall=p.float(v=mandarin_scores['boundary_recall']),
                fscore=p.float(v=mandarin_scores['boundary_fscore'])
            ),
            nlp=dict(
                ned=p.float(v=mandarin_scores['ned']),
                coverage=p.float(v=mandarin_scores['coverage']),
                nwords=p.float(v=mandarin_scores['words']),
                npairs=p.float(v=mandarin_scores['pairs']),
            )
        ),
        german=dict(
            grouping=dict(
                precision=p.float(v=german_scores['grouping_precision']),
                recall=p.float(v=german_scores['grouping_recall']),
                fscore=p.float(v=german_scores['grouping_fscore'])
            ),
            token=dict(
                precision=p.float(v=german_scores['token_precision']),
                recall=p.float(v=german_scores['token_recall']),
                fscore=p.float(v=german_scores['token_fscore'])
            ),
            type=dict(
                precision=p.float(v=german_scores['type_precision']),
                recall=p.float(v=german_scores['type_recall']),
                fscore=p.float(v=german_scores['type_fscore'])
            ),
            boundary=dict(
                precision=p.float(v=german_scores['boundary_precision']),
                recall=p.float(v=german_scores['boundary_recall']),
                fscore=p.float(v=german_scores['boundary_fscore'])
            ),
            nlp=dict(
                ned=p.float(v=german_scores['ned']),
                coverage=p.float(v=german_scores['coverage']),
                nwords=p.float(v=german_scores['words']),
                npairs=p.float(v=german_scores['pairs']),
            )
        ),
        wolof=dict(
            grouping=dict(
                precision=p.float(v=wolof_scores['grouping_precision']),
                recall=p.float(v=wolof_scores['grouping_recall']),
                fscore=p.float(v=wolof_scores['grouping_fscore'])
            ),
            token=dict(
                precision=p.float(v=wolof_scores['token_precision']),
                recall=p.float(v=wolof_scores['token_recall']),
                fscore=p.float(v=wolof_scores['token_fscore'])
            ),
            type=dict(
                precision=p.float(v=wolof_scores['type_precision']),
                recall=p.float(v=wolof_scores['type_recall']),
                fscore=p.float(v=wolof_scores['type_fscore'])
            ),
            boundary=dict(
                precision=p.float(v=wolof_scores['boundary_precision']),
                recall=p.float(v=wolof_scores['boundary_recall']),
                fscore=p.float(v=wolof_scores['boundary_fscore'])
            ),
            nlp=dict(
                ned=p.float(v=wolof_scores['ned']),
                coverage=p.float(v=wolof_scores['coverage']),
                nwords=p.float(v=wolof_scores['words']),
                npairs=p.float(v=wolof_scores['pairs']),
            )
        )
    )

    return TDE17Entry(**dict(
        submission_date=p.datetime(v=mdata['submitted_at']),
        submitted_by=mdata['submitted_by'],
        description=mdata2['system_description'],
        model_id="",
        index=p.int(v=mdata['submission_index']),
        submission_id=p.suid(v=mdata['directory']),
        scores=scores,
        publication=publication,
        details=details
    ))


def modernize_tde17(location: Path,  include_2020: Optional[Path] = None, file_type='.yaml') -> TDE17:
    data = []

    item_list = location.rglob(f"*{file_type}")
    for item in item_list:
        try:
            data.append(modernize_tde17_entry(item))
        except (ValueError, ValidationError, KeyError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
            continue

    if include_2020:
        item_list = include_2020.rglob(f"*{file_type}")
        for item in item_list:
            try:
                data.append(extract_tde17_from_2020(item))
            except (ValueError, ValidationError, KeyError) as _:
                print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
                continue

    return TDE17(
        last_modified=datetime.now(),
        data=data
    )
