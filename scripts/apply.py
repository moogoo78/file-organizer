#!/usr/bin/env python3
"""執行 plan.json：搬移檔案、避免覆蓋、寫入可復原的紀錄。"""
import argparse, json, os, shutil, sys
from datetime import datetime

def unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while os.path.exists(f"{base} ({i}){ext}"):
        i += 1
    return f"{base} ({i}){ext}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    args = ap.parse_args()

    plan = json.load(open(args.plan, encoding="utf-8"))
    root = os.path.realpath(plan["root"])
    done, skipped = [], []

    for m in plan["moves"]:
        src = os.path.realpath(os.path.join(root, m["src"]))
        dst = os.path.realpath(os.path.join(root, m["dst"]))
        if not (src.startswith(root + os.sep) and dst.startswith(root + os.sep)):
            skipped.append({**m, "reason": "路徑超出目標資料夾"}); continue
        if not os.path.isfile(src):
            skipped.append({**m, "reason": "來源不存在"}); continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        dst = unique_path(dst)
        try:
            shutil.move(src, dst)
            rec = {"src": os.path.relpath(src, root), "dst": os.path.relpath(dst, root)}
            for k in ("reason", "confidence"):
                if k in m:
                    rec[k] = m[k]
            done.append(rec)
        except OSError as e:
            skipped.append({**m, "reason": str(e)})

    # 驗證：目的地存在、來源已不在
    failed = [d for d in done
              if not os.path.isfile(os.path.join(root, d["dst"]))
              or os.path.exists(os.path.join(root, d["src"]))]

    log = os.path.join(root, f".organize_log_{datetime.now():%Y%m%d_%H%M%S}.json")
    json.dump({"root": root, "moves": done, "skipped": skipped, "verify_failed": failed},
              open(log, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已搬移 {len(done)} 個，跳過 {len(skipped)} 個，驗證失敗 {len(failed)} 個")
    for f in failed[:20]:
        print(f"  驗證失敗 {f['src']} → {f['dst']}")
    for s in skipped[:20]:
        print(f"  跳過 {s['src']}：{s['reason']}")
    print(f"復原紀錄：{log}")

if __name__ == "__main__":
    main()
