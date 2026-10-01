# helpers for G4 build
def S(page, block):
    return {"page": str(page), "block": block}

def HF(*items):
    """items: 'Form' or ('Form', year)"""
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append({"form": it[0], "year": it[1]})
        else:
            out.append({"form": it, "year": None})
    return out

def LOC(verbatim, rel=None, d=None, dr=None):
    o = {"verbatim": verbatim}
    if rel: o["relative_to"] = rel
    if d is not None: o["distance_hours"] = d
    if dr: o["direction"] = dr
    return o

def EV(*items):
    return [{"year": y, "event_de": de, "event_en": en} for (y, de, en) in items]

def SP(name, kind, page, note=None):
    o = {"name": name, "kind": kind, "page": str(page)}
    if note: o["note"] = note
    return o

def base(id, name, start, end, typ, type_verbatim, wuest=False):
    return {"id": id, "name": name, "start": start, "end": end, "landestheil": "Schleiz",
            "type_verbatim": type_verbatim, "type": typ, "wuestung": wuest}
