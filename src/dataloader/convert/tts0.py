import itertools
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from ..misc import StrParser
from ..models import Benchmark
from ..models.tts0 import TTS019Entry, TTS019


# data parser
p = StrParser()


def modernize_tts019_entry(entry: Path) -> TTS019Entry:
    data = p.load(entry)
    mdata = data['metadata']
    mscores = data['scores']
    mscores_details = dict(
        audio_samples=data['audio_samples'],
        details_abx=data['details_abx'],
        details_bitrate=data['details_bitrate'],
    )

    scores = dict(
        english=dict(
            mos=p.float(v=mscores["english_mos"]),
            cer=p.float(v=mscores["english_cer"]),
            similarity=p.float(v=mscores["english_similarity"]),
            abx=p.float(v=mscores["english_abx"]),
            bitrate=p.float(v=mscores["english_bitrate"])
        ),
        austronesian=dict(
            mos=p.float(v=mscores["surprise_mos"]),
            cer=p.float(v=mscores["surprise_cer"]),
            similarity=p.float(v=mscores["surprise_similarity"]),
            abx=p.float(v=mscores["surprise_abx"]),
            bitrate=p.float(v=mscores["surprise_bitrate"])
        )
    )

    extras = dict(
        audio_samples=dict(
            english=dict(
                sample_1=mscores_details["audio_samples"]["english_1"],
                sample_2=mscores_details["audio_samples"]["english_2"]
            ),
            austronesian=dict(
                sample_1=mscores_details["audio_samples"]["surprise_1"],
                sample_2=mscores_details["audio_samples"]["surprise_2"]
            )
        ),
        detailed_scores=dict(
            abx=dict(
                english=dict(
                    auxiliary1_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary1_abx_dtw_cosine"]),
                    auxiliary1_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary1_abx_dtw_kl"]),
                    auxiliary1_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary1_abx_levenshtein"]),
                    auxiliary2_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary2_abx_dtw_cosine"]),
                    auxiliary2_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary2_abx_dtw_kl"]),
                    auxiliary2_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["english_auxiliary2_abx_levenshtein"]),
                    test_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["english_test_abx_dtw_cosine"]),
                    test_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["english_test_abx_dtw_kl"]),
                    test_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["english_test_abx_levenshtein"])
                ),
                austronesian=dict(
                    auxiliary1_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary1_abx_dtw_cosine"]),
                    auxiliary1_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary1_abx_dtw_kl"]),
                    auxiliary1_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary1_abx_levenshtein"]),
                    auxiliary2_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary2_abx_dtw_cosine"]),
                    auxiliary2_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary2_abx_dtw_kl"]),
                    auxiliary2_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["surprise_auxiliary2_abx_levenshtein"]),
                    test_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx"]["surprise_test_abx_dtw_cosine"]),
                    test_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx"]["surprise_test_abx_dtw_kl"]),
                    test_abx_levenshtein=p.float(
                        v=mscores_details["details_abx"]["surprise_test_abx_levenshtein"])
                )
            ),
            bitrate=dict(
                english=dict(
                    auxiliary1_bitrate=p.float(v=mscores_details["details_bitrate"]["english_auxiliary1_bitrate"]),
                    auxiliary2_bitrate=p.float(v=mscores_details["details_bitrate"]["english_auxiliary2_bitrate"]),
                    test_bitrate=p.float(v=mscores_details["details_bitrate"]["english_test_bitrate"])
                ),
                austronesian=dict(
                    auxiliary1_bitrate=p.float(v=mscores_details["details_bitrate"]["surprise_auxiliary1_bitrate"]),
                    auxiliary2_bitrate=p.float(v=mscores_details["details_bitrate"]["surprise_auxiliary2_bitrate"]),
                    test_bitrate=p.float(v=mscores_details["details_bitrate"]["surprise_test_bitrate"])
                )
            )
        ),
        extra_description=tuple([
            mdata["auxiliary1_description"],
            mdata["auxiliary2_description"]
        ])
    )

    details = dict(
        benchmarks=[Benchmark.TTS0_19],
        parameters=dict(
            abx_distance=mdata["abx_distance"],
            external_data=p.bool(v=mdata["using_external_data"]),
            parallel_train=p.bool(v=mdata["using_parallel_train"])
        )
    )

    publication = dict(
        open_science=p.bool(v=mdata['open_source']),
        author_short=mdata['author_short'],
        author=mdata['author'],
        institution=mdata['affiliation']
    )

    return TTS019Entry(**dict(
        submission_date=p.datetime(v=mdata["submitted_at"]),
        model_id="",
        index=mdata['submission_index'],
        submission_id=p.suid(v=mdata["directory"]),
        submitted_by=mdata['submitted_by'],
        description=mdata['system_description'].replace('<br>', ' '),
        publication=publication,
        details=details,
        scores=scores,
        extras=extras
    ))


def extract_tts019_from_2020(entry: Path) -> TTS019Entry:
    data = p.load(entry)
    entry2019 = data['2019']
    mdata = data['metadata']
    mscores = dict(
        english=entry2019['english']['scores'],
        surprise=entry2019['surprise']['scores']
    )

    mscores_details = dict(
        audio_samples=entry2019['audio_samples'],
        details_abx_english=entry2019['english']['details_abx'],
        details_abx_surprise=entry2019['surprise']['details_abx'],
        details_bitrate_english=entry2019['english']['details_bitrate'],
        details_bitrate_surprise=entry2019['surprise']['details_bitrate'],
        mdata=entry2019["metadata"]
    )

    scores = dict(
        english=dict(
            mos=p.float(v=mscores['english']["mos"]),
            cer=p.float(v=mscores['english']["cer"]),
            similarity=p.float(v=mscores['english']["similarity"]),
            abx=p.float(v=mscores['english']["abx"]),
            bitrate=p.float(v=mscores['english']["bitrate"])
        ),
        austronesian=dict(
            mos=p.float(v=mscores['surprise']["mos"]),
            cer=p.float(v=mscores['surprise']["cer"]),
            similarity=p.float(v=mscores['surprise']["similarity"]),
            abx=p.float(v=mscores['surprise']["abx"]),
            bitrate=p.float(v=mscores['surprise']["bitrate"])
        )
    )

    extras = dict(
        audio_samples=dict(
            english=dict(
                sample_1=mscores_details["audio_samples"]["english_1"],
                sample_2=mscores_details["audio_samples"]["english_2"]
            ),
            austronesian=dict(
                sample_1=mscores_details["audio_samples"]["surprise_1"],
                sample_2=mscores_details["audio_samples"]["surprise_2"]
            )
        ),
        detailed_scores=dict(
            abx=dict(
                english=dict(
                    auxiliary1_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding1"]["cosine"]),
                    auxiliary1_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding1"]["KL"]),
                    auxiliary1_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding1"]["levenshtein"]),
                    auxiliary2_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding2"]["cosine"]),
                    auxiliary2_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding2"]["KL"]),
                    auxiliary2_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_english"]["auxiliary_embedding2"]["levenshtein"]),
                    test_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_english"]["test"]["cosine"]),
                    test_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_english"]["test"]["KL"]),
                    test_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_english"]["test"]["levenshtein"])
                ),
                austronesian=dict(
                    auxiliary1_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding1"]["cosine"]),
                    auxiliary1_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding1"]["KL"]),
                    auxiliary1_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding1"]["levenshtein"]),
                    auxiliary2_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding2"]["cosine"]),
                    auxiliary2_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding2"]["KL"]),
                    auxiliary2_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_surprise"]["auxiliary_embedding2"]["levenshtein"]),
                    test_abx_dtw_cosine=p.float(
                        v=mscores_details["details_abx_surprise"]["test"]["cosine"]),
                    test_abx_dtw_kl=p.float(
                        v=mscores_details["details_abx_surprise"]["test"]["KL"]),
                    test_abx_levenshtein=p.float(
                        v=mscores_details["details_abx_surprise"]["test"]["levenshtein"])
                )
            ),
            bitrate=dict(
                english=dict(
                    auxiliary1_bitrate=p.float(v=mscores_details["details_bitrate_english"]["auxiliary_embedding1"]),
                    auxiliary2_bitrate=p.float(v=mscores_details["details_bitrate_english"]["auxiliary_embedding2"]),
                    test_bitrate=p.float(v=mscores_details["details_bitrate_english"]["test"])
                ),
                austronesian=dict(
                    auxiliary1_bitrate=p.float(v=mscores_details["details_bitrate_surprise"]["auxiliary_embedding1"]),
                    auxiliary2_bitrate=p.float(v=mscores_details["details_bitrate_surprise"]["auxiliary_embedding2"]),
                    test_bitrate=p.float(v=mscores_details["details_bitrate_surprise"]["test"])
                )
            )
        ),
        extra_description=tuple([
            mscores_details['mdata'].get("auxiliary1_description", ""),
            mscores_details['mdata'].get("auxiliary2_description", "")
        ])
    )

    details = dict(
        benchmarks=[Benchmark.TTS0_19],
        parameters=dict(
            abx_distance=mscores_details['mdata']["abx_distance"],
            external_data=p.bool(v=mscores_details['mdata']["using_external_data"]),
            parallel_train=p.bool(v=mscores_details['mdata']["using_parallel_train"]),
            hyperparameters=mscores_details['mdata'].get("hyperparameters", "")
        )
    )

    publication = dict(
        open_science=p.bool(v=mdata['open_source']),
        author_short=mdata['author_short'],
        author=mdata['author'],
        institution=mdata['affiliation']
    )

    return TTS019Entry(**dict(
        submission_date=p.datetime(v=mdata["submitted_at"]),
        model_id="",
        index=mdata['submission_index'],
        submission_id=p.suid(v=mdata["directory"]),
        submitted_by=mdata['submitted_by'],
        description=mscores_details['mdata']["system description"].replace('<br>', ' '),
        publication=publication,
        details=details,
        scores=scores,
        extras=extras
    ))


def modernize_tts019(location: Path, include_2020: Optional[Path] = None, file_type='.yaml') -> TTS019:
    data = []
    item_list = location.rglob(f"*{file_type}")
    for item in item_list:
        try:
            data.append(modernize_tts019_entry(item))
        except (ValueError, ValidationError, KeyError) as _:
            print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
            continue

    if include_2020:
        item_list = include_2020.rglob(f"*{file_type}")
        for item in item_list:
            try:
                data.append(extract_tts019_from_2020(item))
            except (ValueError, ValidationError, KeyError) as _:
                print(f"ERROR ({traceback.format_exc()}): failed for entry: {item}", file=sys.stderr)
                continue

    return TTS019(
        last_modified=datetime.now(),
        data=data
    )
