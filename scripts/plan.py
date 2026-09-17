#!/usr/bin/env python3
"""依掃描結果產生搬移計畫（不會搬動任何檔案）。"""
import argparse, json, os
from collections import Counter

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scan")
    ap.add_argument("--mode", choices=["type", "date", "type-date"], default="type")
    ap.add_argument("--dupes", choices=["move", "ignore"], default="move",
                    help="重複檔移到 _重複檔/（保留每組中路徑最短的一份）")
    ap.add_argument("--out", default="plan.json")
    args = ap.parse_args()

    scan = json.load(open(args.scan, encoding="utf-8"))
    dupe_extra = set()
    if args.dupes == "move":
        for group in scan["duplicates"]:
            dupe_extra.update(group[1:])

    moves = []
    for f in scan["files"]:
        if f.get("temp"):  # 暫存檔只回報，不搬
            continue
        src, name = f["path"], os.path.basename(f["path"])
        year, month = f["mtime"][:4], f["mtime"][:7]
        if src in dupe_extra:
            dst = os.path.join("_重複檔", name)
        elif args.mode == "type":
            dst = os.path.join(f["category"], name)
        elif args.mode == "date":
            dst = os.path.join(year, month, name)
        else:
            dst = os.path.join(f["category"], year, name)
        if os.path.normpath(src) != os.path.normpath(dst):
            moves.append({"src": src, "dst": dst})

    json.dump({"root": scan["root"], "moves": moves},
              open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    counts = Counter(os.path.dirname(m["dst"]) for m in moves)
    print(f"共 {len(moves)} 個檔案將被搬移：")
    for d, n in counts.most_common():
        print(f"  {d}/  ← {n} 個")

if __name__ == "__main__":
    main()
