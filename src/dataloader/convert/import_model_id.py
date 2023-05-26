from datetime import datetime
from typing import Dict

from ..models import Leaderboard


def update_entry(entry, reg_obj):
    """ Update data for an individual entry from the registry """
    entry.publication.authors = reg_obj.get("authors", "")
    entry.publication.paper_title = reg_obj.get("paper_title", "")
    entry.publication.bib_ref = reg_obj.get("bib_ref", "")
    entry.publication.paper_url = reg_obj.get("paper_url", "")
    entry.publication.pub_year = reg_obj.get("pub_date", "")

    if not entry.publication.paper_ref:
        entry.publication.paper_ref = f"{entry.publication.authors} ({entry.publication.pub_year}) {entry.publication.paper_title}"

    if not entry.publication.open_science and not entry.publication.code:
        entry.publication.open_science = False
    else:
        entry.publication.open_science = True

    if entry.publication.DOI:
        entry.submission_id = entry.publication.DOI


def add_external_info(leaderboard: Leaderboard, model_registry: Dict):
    for entry in leaderboard.data:
        reg_obj = model_registry.get(entry.model_id, None)
        if reg_obj is None:
            print(f"No registry data found for {entry.model_id}")
        else:
            update_entry(entry, reg_obj)

    leaderboard.last_modified = datetime.now()
