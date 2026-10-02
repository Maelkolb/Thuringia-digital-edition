import math


class Panel:
    """Mercator panel as Vega draws it: centre lon/lat at (w/2, h/2), scale in px per radian."""

    def __init__(self, lon_range, lat_range, scale, width=None, height=None):
        self.scale = scale
        self.lon0 = (lon_range[0] + lon_range[1]) / 2
        mid_y = (self._my(lat_range[0]) + self._my(lat_range[1])) / 2
        self.lat0 = self._inv_my(mid_y)
        self.w = width or round(abs(math.radians(lon_range[1] - lon_range[0])) * scale)
        self.h = height or round((self._my(lat_range[1]) - self._my(lat_range[0])) * scale)

    @staticmethod
    def _my(lat):
        return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

    @staticmethod
    def _inv_my(y):
        return math.degrees(2 * math.atan(math.exp(y)) - math.pi / 2)

    def xy(self, lon, lat):
        x = self.w / 2 + self.scale * math.radians(lon - self.lon0)
        y = self.h / 2 - self.scale * (self._my(lat) - self._my(self.lat0))
        return x, y

    def lonlat(self, x, y):
        lon = self.lon0 + math.degrees((x - self.w / 2) / self.scale)
        lat = self._inv_my(self._my(self.lat0) - (y - self.h / 2) / self.scale)
        return lon, lat

    def bounds(self, margin_px=0):
        lo1, la1 = self.lonlat(-margin_px, self.h + margin_px)
        lo2, la2 = self.lonlat(self.w + margin_px, -margin_px)
        return (lo1, lo2), (la1, la2)

    def projection(self):
        return {"type": "mercator", "center": [round(self.lon0, 5), round(self.lat0, 5)], "scale": self.scale, "translate": [self.w / 2, self.h / 2]}

    def inside_expr(self, margin_px=0):
        (lo1, lo2), (la1, la2) = self.bounds(margin_px)
        return f"datum.lon >= {lo1:.5f} && datum.lon <= {lo2:.5f} && datum.lat >= {la1:.5f} && datum.lat <= {la2:.5f}"


def place_labels(panel, items, char_px=6.0, line_px=12.5, radius_of=lambda it: 7, pad=2):
    """items: list of dict(key, lon, lat, lines). Returns key -> (align, dx, dy_first_line, penalty).

    Vega text with several lines puts the FIRST line at the anchor (baseline middle), later lines below it."""
    markers = {}
    for it in items:
        x, y = panel.xy(it["lon"], it["lat"])
        markers[it["key"]] = (x, y, radius_of(it))
    placed = []
    out = {}
    order = sorted(items, key=lambda it: (-len(it["lines"]), -max(len(l) for l in it["lines"]), it["key"]))
    for it in order:
        x, y, r = markers[it["key"]]
        n = len(it["lines"])
        w = max(len(l) for l in it["lines"]) * char_px
        h = n * line_px
        g = r + 3
        cands = []

        def add(align, dx, y0, pref):
            x0 = x + dx if align == "left" else (x + dx - w if align == "right" else x + dx - w / 2)
            cands.append((align, dx, y0 + line_px / 2 - y, (x0, y0, x0 + w, y0 + h), pref))

        add("left", g, y - h / 2, 0)
        add("left", g, y - line_px / 2, 0.5)
        add("right", -g, y - h / 2, 0.2)
        add("right", -g, y - line_px / 2, 0.7)
        add("center", 0, y - r - 2 - h, 1.0)
        add("center", 0, y + r + 2, 1.2)
        add("left", g * 0.75, y - r * 0.4 - h, 1.5)
        add("left", g * 0.75, y + r * 0.4, 1.6)
        add("right", -g * 0.75, y - r * 0.4 - h, 1.7)
        add("right", -g * 0.75, y + r * 0.4, 1.8)
        for gap, pr in ((8, 2.0), (14, 2.5), (20, 3.0)):
            add("center", 0, y + r + gap, pr)
            add("center", 0, y - r - gap - h, pr + 0.1)
            add("left", g * 0.5, y + r + gap, pr + 0.2)
            add("right", -g * 0.5, y + r + gap, pr + 0.3)
            add("left", g * 0.5, y - r - gap - h, pr + 0.4)
            add("right", -g * 0.5, y - r - gap - h, pr + 0.5)
        for dxx in (14, 22, 30):
            add("left", g + dxx, y - h / 2, 3.5)
            add("right", -g - dxx, y - h / 2, 3.6)
        best = None
        for align, dx, dy, rect, pref in cands:
            hit = 0
            for k, (mx, my, mr) in markers.items():
                if rect[0] < mx + mr and rect[2] > mx - mr and rect[1] < my + mr and rect[3] > my - mr:
                    hit += 1
            for o in placed:
                if rect[0] < o[2] + pad and rect[2] > o[0] - pad and rect[1] < o[3] + pad and rect[3] > o[1] - pad:
                    hit += 1
            off = rect[0] < 0 or rect[2] > panel.w or rect[1] < 0 or rect[3] > panel.h
            score = hit * 10 + (50 if off else 0) + pref
            if best is None or score < best[0]:
                best = (score, align, dx, dy, rect)
        out[it["key"]] = (best[1], round(best[2], 1), round(best[3], 1), int(best[0] // 10))
        placed.append(best[4])
    return out
