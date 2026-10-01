"""Helpers for assembling the E6 decision file."""
import json

D = {}      # key -> decision
ORDER = []  # insertion order


def _put(d):
    k = d["key"]
    if k in D:
        raise SystemExit(f"duplicate decision for {k!r}")
    D[k] = d
    ORDER.append(k)


def acc(key, label, cls="organisation", kind=None, gloss=None, merges=(), **kw):
    """Accept (organisation) or reclass (other class) + merge variants into it."""
    d = {"key": key, "action": "accept" if cls == "organisation" else "reclass", "label": label, "class": cls}
    if kind:
        d["kind"] = kind
    if gloss:
        d["gloss_en"] = gloss
    for k, v in kw.items():
        if v is not None:
            d[k] = v
    _put(d)
    for m in merges:
        mrg(m, key)


def mrg(key, into):
    _put({"key": key, "action": "merge", "into": into})


def rej(key, reason):
    _put({"key": key, "action": "reject", "reason": reason})


def concept(key, label, kind, gloss, merges=(), **kw):
    acc(key, label, "concept", kind, gloss, merges, **kw)


def place(key, label, kind, gloss, merges=(), **kw):
    acc(key, label, "place", kind, gloss, merges, **kw)


def person(key, label, kind, gloss, merges=(), **kw):
    acc(key, label, "person", kind, gloss, merges, **kw)
