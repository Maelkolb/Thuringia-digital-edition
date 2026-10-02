"""Parsing of the trade tables pp. 258-260."""
import re
import sys
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\data\analyses\_work\A10")
from common import *

DISTRICTS = ["Gera", "Schleiz", "Lobenstein-Ebersdorf"]
# canonical order / names / English
TRADES = [
    ("Colonial- und Materialhändler", "Colonial and general-goods dealers"),
    ("Victualienhändler", "Provisions dealers"),
    ("Getreidehändler", "Grain dealers"),
    ("Viehhändler", "Cattle dealers"),
    ("Lederhändler", "Leather dealers"),
    ("Schnitt-, Putz- und Modewaarenhändler", "Drapers, millinery and fashion dealers"),
    ("Strumpf- und Zwirnhändler", "Hosiery and thread dealers"),
    ("Galanteriewaarenhändler", "Fancy-goods dealers"),
    ("Holzhändler", "Timber dealers"),
    ("Buch-, Kunst- und Musikalienhändler", "Book, art and music dealers"),
    ("Banquiers", "Bankers"),
    ("Agenten, Spediteurs, Mäkler und Commissionäre", "Agents, forwarders, brokers and commission merchants"),
    ("Schenk- und Gastwirthe", "Innkeepers and publicans"),
    ("Miethkutscher und Frachtfuhrleute", "Hackney coachmen and carriers"),
    ("Sonstige Händler", "Other dealers"),
]
KEYS = [
    "Colon", "Victual", "Getreide", "Vieh", "Leder", "Schnitt", "Strumpf", "Galanterie", "Holz", "Buch", "Banqu", "Agenten", "Schenk", "Miethk", "Sonstige",
]


def key_of(name):
    for i, k in enumerate(KEYS):
        if name.strip().startswith(k):
            return i
    return None


def vals_of(r):
    out = []
    for x in r[1:13]:
        x = re.sub(r"\*+\)", "", x)
        out.append(num(x))
    return out


def parse_block(label, bid, rows_range):
    out = {}
    g = grid(label, bid)
    for i in rows_range:
        r = g[i - 1]
        k = key_of(r[0])
        assert k is not None, (label, i, r[0])
        out[k] = (vals_of(r), f"S. {label} {bid} r{i}", r[1:13])
    return out


def load():
    gera = parse_block("258", "b4", range(3, 18))
    schl = parse_block("259", "b1", range(4, 19))
    lob = parse_block("259", "b1", range(21, 36))
    fst = parse_block("260", "b1", range(3, 18))
    return {"Gera": gera, "Schleiz": schl, "Lobenstein-Ebersdorf": lob, "Fürstenthum": fst}


def sum_rows():
    g258 = grid("258", "b4"); g259 = grid("259", "b1"); g260 = grid("260", "b1")
    return {"Gera": vals_of(g258[17]), "Schleiz": vals_of(g259[18]), "Lobenstein-Ebersdorf": vals_of(g259[35]), "Fürstenthum": vals_of(g260[17])}


if __name__ == "__main__":
    D = load()
    z = lambda x: x or 0
    for dn in DISTRICTS + ["Fürstenthum"]:
        for k in range(15):
            v = D[dn][k][0]
            for c in range(4):
                if z(v[c]) + z(v[4 + c]) != z(v[8 + c]):
                    print("St+Pl != Summe", dn, TRADES[k][0], "SGDF"[c], v[c], v[4 + c], v[8 + c], D[dn][k][1])
    for k in range(15):
        for c in range(12):
            comp = sum(z(D[dn][k][0][c]) for dn in DISTRICTS)
            if comp != z(D["Fürstenthum"][k][0][c]):
                print("Fst != districts", TRADES[k][0], ["St", "Pl", "Sum"][c // 4], "SGDF"[c % 4], comp, D["Fürstenthum"][k][0][c], D["Fürstenthum"][k][1])
    S = sum_rows()
    for dn in DISTRICTS + ["Fürstenthum"]:
        for c in range(12):
            comp = sum(z(D[dn][k][0][c]) for k in range(15))
            if comp != z(S[dn][c]):
                print("Summe row mismatch", dn, ["St", "Pl", "Sum"][c // 4], "SGDF"[c % 4], comp, S[dn][c])
