import csv, os
from decimal import Decimal, InvalidOperation

DATE_FMTS = ("%Y-%m-%d", "%d/%m/%Y")


def _money(s):
    # bank exports put commas in thousands and sometimes a trailing CR
    s = s.replace(",", "").strip()
    neg = s.endswith("CR")
    if neg: s = s[:-2].strip()
    try:
        v = Decimal(s)
    except InvalidOperation:
        return None
    return -v if neg else v


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            amt = _money(r.get("Amount", ""))
            if amt is None:
                continue  # summary junk at the bottom of HDFC exports
            yield {"date": r.get("Date", "").strip(),
                   "desc": r.get("Narration") or r.get("Description", ""),
                   "amt": amt,
                   "cat": (r.get("Category") or "uncategorised").strip().lower()}


def write_rows(path, rows):
    # TODO this clobbers; fine for now, we always regenerate from the bank file
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "desc", "amt", "cat"])
        for r in rows:
            w.writerow([r["date"], r["desc"], r["amt"], r["cat"]])
    os.replace(tmp, path)
