#!/usr/bin/env python3
"""依紀錄檔把檔案搬回原位，並移除變空的資料夾。"""
import json, os, shutil, sys

def main():
    if len(sys.argv) != 2:
        sys.exit("用法：python undo.py <.organize_log_xxx.json>")
    log = json.load(open(sys.argv[1], encoding="utf-8"))
    root = log["root"]
    restored = 0
    for m in reversed(log["moves"]):
        cur, orig = os.path.join(root, m["dst"]), os.path.join(root, m["src"])
        if os.path.exists(cur) and not os.path.exists(orig):
            os.makedirs(os.path.dirname(orig), exist_ok=True)
            shutil.move(cur, orig)
            restored += 1
            d = os.path.dirname(cur)
            while d != root and os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
                d = os.path.dirname(d)
        else:
            print(f"無法復原：{m['dst']}")
    print(f"已復原 {restored}/{len(log['moves'])} 個檔案")

if __name__ == "__main__":
    main()
