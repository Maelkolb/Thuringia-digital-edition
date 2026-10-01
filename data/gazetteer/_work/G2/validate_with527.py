import sys, json
sys.path.insert(0, r"C:\Users\totom\Projects\reuss-edition\tools")
import validate_gazetteer as v
blocks = json.load(open(r"C:\Users\totom\Projects\reuss-edition\data\gazetteer\_work\G2\p527_blocks.json", encoding="utf-8"))
if not v.pages["527"]["blocks"]:
    v.pages["527"]["blocks"] = blocks
    print("(using scratch transcription of p.527)")
sys.exit(v.main(sys.argv[1]))
