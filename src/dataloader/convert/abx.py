import sys
import traceback
from datetime import datetime
from pathlib import Path
from ..misc import StrParser
from ..models import ABX15, Benchmark, ABX17
from ..models.abx import ABX15Entry, ABX17Entry, ABXLS, ABXLSEntry

from pydantic import create_model, AnyHttpUrl, ValidationError

# data parser
p = StrParser()


def modernize_abx15_entry(entry: Path) -> ABX15Entry:
    data = p.load(entry)
    mdata = data["metadata"]
    sdata = data["scores"]

    main_idea = mdata.get('main_idea', '')

    scores = dict(
        english=dict(within=p.float(v=sdata['english_within']),
                     across=p.float(v=sdata['english_across'])),
        xitsonga=dict(within=p.float(v=sdata['xitsonga_across']),
                      across=p.float(v=sdata['xitsonga_within']))
    )

    paper_url = p.doi(v=mdata["bib"].strip())[0]
    try:
        fake_model = create_model('DynamicFoobarModel', url=(AnyHttpUrl, ...))
        fake_model(url=paper_url) # noqa : its made to test typing
    except ValidationError:
        paper_url = None

    publication = dict(
        author_short=mdata['author'],
        paper_ref=mdata['reference'],
        paper_url=paper_url,
        institution=mdata["team"],
        open_science=False
    )

    supervision = p.bool(v=mdata['supervision'])
    if supervision:
        main_idea = f"{main_idea}. Supervised with {mdata['supervision'].replace('yes,','').strip()}."

    details = dict(
        benchmarks=[Benchmark.ABX_15],
        parameters=dict(
            supervision=supervision,
            binary=p.bool(v=mdata['binary'])
        )
    )

    return ABX15Entry(**dict(
        model_id="",
        index=0,
        submission_id="",
        description=main_idea,
        scores=scores,
        publication=publication,
        details=details
    ))


def modernize_abx15(location: Path, file_type=".yaml"):
    data = []
    for item in location.rglob(f"*{file_type}"):
        try:
            data.append(modernize_abx15_entry(item))
        except (ValueError, ValidationError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}",
                  file=sys.stderr)
            continue

    return ABX15(
        last_modified=datetime.now(),
        data=data
    )


def modernize_abx17_entry(across: Path, within: Path) -> ABX17Entry:
    across_data = p.load(across)
    mdata = across_data["metadata"]
    across_sdata = across_data["scores"]
    within_data = p.load(within)
    _ = within_data["metadata"]
    within_sdata = within_data["scores"]

    n_doi = p.doi2(v=mdata["DOI"].strip())
    if n_doi[0]:
        doi = f"10.5281/zenodo.{n_doi[1]}"
    else:
        doi = None

    publication = dict(
        author_short=mdata['author'],
        institution=mdata["affiliation"],
        open_science=False,
        DOI=doi
    )

    details = dict(
        benchmarks=[Benchmark.ABX_17],
        parameters=dict(
            supervision=p.bool(v=mdata["supervision"])
        )
    )

    scores = dict(
        english=dict(
            t_1s=dict(
                across=p.float(v=across_sdata["english_1s"]),
                within=p.float(v=within_sdata["english_1s"])
            ),
            t_10s=dict(
                across=p.float(v=across_sdata["english_10s"]),
                within=p.float(v=within_sdata["english_10s"])
            ),
            t_120s=dict(
                across=p.float(v=across_sdata["english_120s"]),
                within=p.float(v=within_sdata["english_120s"])
            ),
        ),
        french=dict(
            t_1s=dict(
                across=p.float(v=across_sdata["french_1s"]),
                within=p.float(v=within_sdata["french_1s"])
            ),
            t_10s=dict(
                across=p.float(v=across_sdata["french_10s"]),
                within=p.float(v=within_sdata["french_10s"])
            ),
            t_120s=dict(
                across=p.float(v=across_sdata["french_120s"]),
                within=p.float(v=within_sdata["french_120s"])
            ),
        ),
        mandarin=dict(
            t_1s=dict(
                across=p.float(v=across_sdata["mandarin_1s"]),
                within=p.float(v=within_sdata["mandarin_1s"])
            ),
            t_10s=dict(
                across=p.float(v=across_sdata["mandarin_10s"]),
                within=p.float(v=within_sdata["mandarin_10s"])
            ),
            t_120s=dict(
                across=p.float(v=across_sdata["mandarin_120s"]),
                within=p.float(v=within_sdata["mandarin_120s"])
            ),
        ),
        german=dict(
            t_1s=dict(
                across=p.float(v=across_sdata["LANG1_1s"]),
                within=p.float(v=within_sdata["LANG1_1s"])
            ),
            t_10s=dict(
                across=p.float(v=across_sdata["LANG1_10s"]),
                within=p.float(v=within_sdata["LANG1_10s"])
            ),
            t_120s=dict(
                across=p.float(v=across_sdata["LANG1_120s"]),
                within=p.float(v=within_sdata["LANG1_120s"])
            ),
        ),
        wolof=dict(
            t_1s=dict(
                across=p.float(v=across_sdata["LANG2_1s"]),
                within=p.float(v=within_sdata["LANG2_1s"])
            ),
            t_10s=dict(
                across=p.float(v=across_sdata["LANG2_10s"]),
                within=p.float(v=within_sdata["LANG2_10s"])
            ),
            t_120s=dict(
                across=p.float(v=across_sdata["LANG2_120s"]),
                within=p.float(v=within_sdata["LANG2_120s"])
            ),
        )
    )

    return ABX17Entry(**dict(
        model_id="",
        submission_id="",
        description="",
        index=0,
        scores=scores,
        publication=publication,
        details=details
    ))


def modernize_abx17(location: Path, file_type=".yaml"):
    data = []
    files = zip(
        sorted((location / 'across_speakers').rglob(f"*{file_type}"), key=lambda x: int(x.stem)),
        sorted((location / 'within_speakers').rglob(f"*{file_type}"), key=lambda x: int(x.stem))
    )
    for across, within in files:
        try:
            data.append(modernize_abx17_entry(across=across, within=within))
        except (ValueError, ValidationError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {across.stem}",
                  file=sys.stderr)
            continue

    return ABX17(
        last_modified=datetime.now(),
        data=data
    )


def modernize_abxls_entry(entry: Path) -> ABXLSEntry:
    data = p.load(entry)
    desc = data['more']['description']

    publication = dict(
        open_science=p.bool(v=desc['open_source']),
        author_short=p.str(v=data['author_label']),
        author=p.str(v=desc['author']),
        institution=p.str(v=desc['affiliation'])
    )

    details = dict(
        train_set=p.str(v=desc['train_set']),
        benchmarks=[Benchmark.sLM_21, Benchmark.ABX_LS],
        gpu_budget=p.int(v=desc['gpu_budget']),
        parameters=dict(
            visually_grounded=p.bool(v=desc.get('visually_grounded', 'false'))
        )
    )

    scores = dict(
        clean=dict(
            dev=dict(
                within=p.float(v=data['phonetic_clean_within'][0]),
                across=p.float(v=data['phonetic_clean_across'][0])
            ),
            test=dict(
                within=p.float(v=data['phonetic_clean_within'][1]),
                across=p.float(v=data['phonetic_clean_across'][1])
            )
        ),
        other=dict(
            dev=dict(
                within=p.float(v=data['phonetic_other_within'][0]),
                across=p.float(v=data['phonetic_other_across'][0])
            ),
            test=dict(
                within=p.float(v=data['phonetic_other_within'][0]),
                across=p.float(v=data['phonetic_other_across'][1])
            )
        )
    )

    return ABXLSEntry(**dict(
        submission_date=p.datetime(v=desc["submitted_at"]),
        model_id="",
        submission_id="",
        index=data['index'],
        description=desc["description"],
        publication=publication,
        details=details,
        scores=scores
    ))


def modernize_abxls(location: Path, file_type=".yaml") -> ABXLS:
    data = []
    for item in location.rglob(f"*{file_type}"):
        try:
            data.append(modernize_abxls_entry(item))
        except (ValueError, ValidationError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}",
                  file=sys.stderr)
            continue

    return ABXLS(
        last_modified=datetime.now(),
        data=data
    )
