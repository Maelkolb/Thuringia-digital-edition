"""Pages 527 and 739: Gemini refuses them (finish reason RECITATION) - that is
also why the original run stored them empty. They were transcribed from the
BSB facsimile by Claude Opus 5.5 on 2026-10-01 (same conventions as the rest:
modern umlauts, long s resolved, 1870 spelling, line-break hyphens joined) and
are annotated with the original NER prompt. Provenance is recorded per page.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source" / "hde_2026-03-03"))
from google import genai  # noqa: E402
from src.config import ENTITY_TYPES, MODEL_ID, THINKING_LEVEL  # noqa: E402
from src.ner import perform_ner  # noqa: E402
from src.pipeline import _build_ocr_text  # noqa: E402

PAGES = {
    539: {
        "page_number": 527,
        "structure": {
            "page_number_printed": "527",
            "header": "I. Der Landestheil oder Landrathsbezirk Gera.",
            "content_blocks": [
                {"block_type": "paragraph", "content": "Schulbesuch. Auf 9 eheliche Kinder 2 uneheliche. Die auf ziemlich humusreichem Lehmboden ruhende, in günstigen Jahren größtentheils ergiebige Flur umfaßt 1731 5/6 Morgen. Der mittelgute Acker steht zu 6 Thlr. Pacht. In der Flur 10 Teiche und ein Braunkohlenwerk, das seit 1821 in Betrieb war und viele Hände beschäftigte, aber seit 1864 wegen der nicht bewältigten Grubenwasser still liegt. Hauptflurstücke sind: Teichfeld, Schenkenfeld, Rohwiese, Schafwiese, Miethenfelder, Schleife, lange Beete, großes Gewende, Mittelgrund, Mittelstraße, Sandberg, Heide, Rödelfelder, Rödelgrund, Hartgraben, Himmelreich, Oertelsbach und Hain. Nach der Sage soll Kleinaga zwei hier einst gegründeten Nonnenklöstern seinen Ursprung verdanken. Worauf diese Sage beruht, wird wohl ein Räthsel bleiben, zumal über die früheste Geschichte des Ortes wenig bekannt ist. Im 30jährigen Kriege hat Kleinaga viel zu erdulden gehabt. Von dem Gutsherrn Adam Heinrich v. Metsch erwähnt das großagaer Kirchenbuch, daß er 1671 wegen seiner groben sinnlichen Vergehungen Kirchenbuße thun mußte. Den Ortstheil Froschweide trafen 1765 und 1811 zwei große Brände, dort mit 8, hier mit 9 Häusern. Dem Landesherrn gehörten die Obergerichte, dem Rittergute die Erbgerichte und die Lehn mit Ausnahme einiger dem zeitzer Kirchkasten zuständiger Lehen."},
                {"block_type": "paragraph", "content": "Die Wustung Rödel (Rödelsdorf) liegt 1/4 Stunde östlich von Kleinaga da, wo der Rödelgrund, die Rödelfelder und das Rödelholz getroffen werden. Der Ort umfaßte, wie man noch wahrnehmen kann, nur 6 Gehöfte, war demnach klein, was auch seine geringe Markung ausweist, die zum Theil zu Kleinaga, zum Theil zu Großaga geschlagen ist. Im Jahre 1364 bestand noch der Ort und wird Rodelin genannt. Die Theilungsacten von 1647 gedenken des Ortes nicht mehr, folglich kann er nicht, wie man irrthümlich meint, im 30jährigen Kriege, sondern muß früher wüst geworden sein. Daß sich dessen Bewohner nach Kleinaga übergesiedelt und auf der dasigen Froschweide angebaut haben, wovon ihnen der Name Froschweider zu Theil wurde, ist gewiß, weil die früher auf der Gemeinde Rödel ruhende Verpflichtung zum langenberger Rügegericht auf die froschweider Bauern überging, die in der Wustung Rödel begütert sind. Selbst auf einem großagaer Bauer blieb diese Verpflichtung wegen seines Besitzes von rödelsdorfer Grundstücken haften. Merkwürdig ist, daß sich in der Wustungsstätte Ueberreste von Mauern und Gewölben, selbst der Vordertheil eines Backofens bis in den Anfang dieses Jahrhunderts erhalten haben. Auch werden noch immer einzelne Geräthschaften gefunden. Der Ort selbst muß frühzeitig gegründet worden sein, weil er dem alten Rügegerichte und Frohntanze zu Langenberg einverleibt war. Uebrigens hieß er beim Rügegerichte niemals Rötheldorf, sondern stets Rödel. Desgleichen nennen die Stadt- und Landgerichtsacten zu Gera das Holz der Wustung den Rödel (auch Kastenholz) und die Flurkarten schreiben Rödelgrund und Rödelfelder. Nach dem Namen zu schließen, ist der Ort ein deutscher Anbau."},
                {"block_type": "paragraph", "content": "Reichenbach (urkundlich 1364 Richenbach, Reichenbach, im Volke „Reichmich, Reichmerich, Reichermich“), Dörfchen, 3/4 Stunde S. von Großaga, in der oberen sanften Agamulde, am Reichenbächlein, 740 Fuß (Dorfsmitte) hoch gelegen, hat seinen Namen, wie die übrigen 30 gleichnamigen Orte Deutschlands, von dem quellenreichen Boden und ist, wie der Name bezeugt, ein deutscher Anbau. Eine Vicinalstraße verbindet den Ort mit Kleinaga und eine Allee mit der Heerstraße beim goldenen Kranich. Er zerfällt in Vorderdorf und Hinterdorf und begreift 1 Gemeindehaus und 18 Privathäuser mit 15 Scheunen und 13 Höfen, in 20"},
            ],
            "footnotes": [],
        },
    },
    751: {
        "page_number": 739,
        "structure": {
            "page_number_printed": "739",
            "header": "III. Der Landestheil Lobenstein-Ebersdorf.",
            "content_blocks": [
                {"block_type": "paragraph", "content": "Im Jahre 1732, wo Ebersdorf mit Lobenstein einen Zug von 1000 salzburger Emigranten zwei Tage mit dem rühmlichsten Eifer pflegte, wurde von der Landesherrschaft ein Armen- und Waisenhaus gegründet und 1739 durch den Bau eines größeren erweitert, das 1748 an die Brüdergemeinde gegen Ueberlassung ihres seitherigen Chorhauses der ledigen Brüder überging. Am 9. October 1806 nahm Napoleon auf seinem Kriegszuge gegen Preußen im hiesigen Schlosse Quartier und erließ von hier die erste Proclamation an die Sachsen. Von ihm erlangte die damalige durch ihren Geist imponirende Fürstin, die Mutter des hier geborenen Heinrich LXXII., Erleichterung und Schutz nicht allein für ihr Gebiet, sondern auch für das ganze Reußenland*). Zu Anfange der 1830r Jahre war hier die schöne Spanierin Lola zum Besuche bei dem Fürsten Heinrich LXXII., der sie in London aus drückenden Verhältnissen erlöst hatte. Sie wurde jedoch hier bald ungezogen, lästig und mußte deshalb das Land räumen. Ende der 1830r Jahre kam leider von hier eine durch den Missionär Zwick nach Ebersdorf gebrachte Sammlung von 1500 orientalischen Münzen unter Vermittlung des Diacon Kühnemann käuflich um 1000 Thlr. nach Jena. Unter den Münzen ist die älteste allein 1000 Thlr. werth."},
                {"block_type": "paragraph", "content": "Wenn auch nicht von Hagelschlägen (besonders 1775, 1781 und 1787), so ist doch der Ort von bedeutenden Bränden verschont geblieben. 1864 ging"},
            ],
            "footnotes": [
                {"marker": "*)", "text": "Ueber Ebersdorf, auf Saalburg zu, gingen am 8. October 1806 der Großherzog von Berg mit seinem Corps und nach ihm die Truppen der Marschälle von Ponte-Corvo und Davoust. Am Abende desselben Tages langte ein Theil der kaiserlichen Garde mit dem kaiserlichen Hauptquartier in Ebersdorf an. Napoleon nahm seine Wohnung im Schlosse. Der Fürst Heinrich LI. war eben kränklich, aber seine Gemahlin, eine ebenso menschenfreundliche, als geistvolle Dame, mit welcher der Kaiser sich lange unterhielt, erwarb sich die Achtung des großen Mannes. Ihr verdankte die Herrschaft Ebersdorf Befreiung von weiterer Einquartierung und Vorspann, sowie das ganze reußische Land späterhin einen kaiserlichen Schutzbrief und gänzliche Befreiung von jeder Contribution. Zudem blieben die reußischen Mannschaften unentwaffnet. Am 9. October Vormittags machte Napoleon eine Recognoscirung gegen Schleiz hin und ertheilte darauf dem Marschall Fürst v. Ponte-Corvo den Befehl, Schleiz zu nehmen. Als er am Morgen des 10. Octobers von Ebersdorf aufbrach, ließ er daselbst ein Commando seiner Garden als Sauvegarde zurück mit dem gemessenen Befehle, nicht zu gestatten, daß irgend ein Militär im Schlosse oder in Ebersdorf sich einquartiere. Am Abende desselben Tages, wo das kaiserliche Hauptquartier abgegangen war, traf Marschall Lefèbre an der Spitze von 3000 Garden ein. Ebersdorf war ihm zum Quartier angewiesen, dennoch ging er weiter, obgleich die Truppen schon einen starken Marsch gemacht hatten. Zwei Tage später kam der Staatssecretär Maret, welcher auf dem ganzen Wege in den vormaligen Quartieren des Kaisers das seinige genommen hatte. Er hielt vor dem Schlosse, nannte der Wache seinen Namen, erhielt aber zur Antwort, daß sie ohne Unterschied Niemand einlassen dürfe. Jetzt verlangte er, dem Fürsten seinen Namen zu melden, und erst nach der Einladung vom Fürsten ließ ihn die Wache durch. Am 10. October nahm Napoleon sein Hauptquartier zu Schleiz, am 11. zu Auma. Bereits am Vormittage des letzten Tages waren die französischen Truppen unter dem Großherzog von Berg und dem Marschall Ponte-Corvo in Gera eingerückt und bis Langenberg vorgedrungen; am Nachmittage traf auch Napoleon in Gera ein, ritt aber sogleich auf den Galgenberg zur Recognoscirung der Gegend, entwarf nach seiner Rückkunft in die Stadt in Gegenwart des Großherzogs von Berg, in dessen Quartier er einige Stunden abgestiegen war, und in Gegenwart der Marschälle von Neufchatel, Ponte-Corvo und Davoust den Plan zur Schlacht bei Jena und ging hierauf in sein Hauptquartier nach Auma zurück. Am 12. October Nachmittags 3 Uhr kam die Fußgarde Napoleons, 10,000 Mann stark, nach Gera und eine Stunde darauf der Kaiser selbst. Er nahm, nachdem er wiederum den mit zwei Kanonen besetzten Galgenberg bestiegen hatte, sein Hauptquartier im Gebäude der Landesregierung. Hier war es, wo er die ersten Trophäen des Sieges seiner Armee bei Saalfeld erhielt. Mit Napoleon waren zugleich in Gera die Marschälle Düroc, Soult, Lefèbre, Bessieres, die Generäle Oudinot, Villemancy, Savary, Rapp, Hülin, Esteve, Chasseloup, Macon, Berthier, Clarke, Caulincourt und der Kunstkenner Dinon. Am 13. October Vormittags 10 Uhr rückte Napoleon, an der Spitze seiner Garden, aus Gera und nahm den Weg über Köstritz nach Jena. Dies der Zug Napoleons durch das reußische Land."},
            ],
        },
    },
}


def main() -> None:
    key = os.environ.get("GEMINI_API_KEY") or Path.home().joinpath("Downloads", "gemini_key.txt").read_text().strip()
    client = genai.Client(api_key=key)
    for seq, rec in PAGES.items():
        out = ROOT / "data" / "raw_fill" / f"seq_{seq:04d}.json"
        text = _build_ocr_text(rec["structure"])
        ents, model = [], MODEL_ID
        for attempt in range(8):
            model = MODEL_ID if attempt < 2 else "gemini-3.5-flash"
            ents = perform_ner(client, text, ENTITY_TYPES, model, thinking_level=THINKING_LEVEL)
            if ents:
                break
            time.sleep(10 * (attempt + 1))
        full = {
            "page_number": rec["page_number"], "seq": seq, "image_filename": f"bsb11005578_seq_{seq:03d}.jpg",
            "structure": rec["structure"], "ocr_text": text, "entities": [e.__dict__ for e in ents],
            "processing_timestamp": dt.datetime.now().isoformat(),
            "model_used": "claude-opus-5-5 (transcription from facsimile); " + model + " (NER)",
            "note": "Gemini OCR refused this page (finish reason RECITATION) in 2026-03 and 2026-10; transcribed manually by Claude from the BSB scan.",
        }
        out.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"seq {seq}: {len(text)} chars, {len(ents)} entities ({model})")


if __name__ == "__main__":
    main()
