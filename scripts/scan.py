#!/usr/bin/env python3
"""掃描資料夾，輸出檔案清單、類型統計與疑似重複檔。"""
import argparse, hashlib, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
PROJECT_MARKERS = {".git", "package.json", "requirements.txt", "pyproject.toml", "Cargo.toml"}
TEMP_EXTS = {"tmp", "swp", "bak", "crdownload", "part"}
VERSION_RE = re.compile(
    r"(?<![a-z])(final|draft|old|backup|copy|new)(?![a-z])|副本|複本|(?<![a-z])v\d+(?![a-z])|\(\d+\)$", re.I)

CATEGORIES = {
    "圖片": {"jpg","jpeg","png","gif","webp","heic","bmp","tiff","svg","raw","cr2","nef"},
    "影片": {"mp4","mov","avi","mkv","webm","m4v","wmv"},
    "音訊": {"mp3","wav","flac","aac","m4a","ogg"},
    "文件": {"pdf","doc","docx","txt","md","rtf","odt","pages","epub"},
    "試算表": {"xls","xlsx","csv","numbers","ods"},
    "簡報": {"ppt","pptx","key","odp"},
    "壓縮檔": {"zip","rar","7z","tar","gz","bz2","xz"},
    "安裝檔": {"dmg","pkg","exe","msi","deb","apk","appimage"},
    "程式碼": {"py","js","ts","html","css","json","java","c","cpp","go","rs","sh","ipynb"},
}

def category(ext):
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "其他"

def file_hash(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--out", default="scan.json")
    ap.add_argument("--no-recursive", action="store_true", help="只掃描第一層")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit(f"找不到資料夾：{root}")

    files, projects, temp_files = [], [], []
    by_size = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != "." and PROJECT_MARKERS & (set(dirnames) | set(filenames)):
            projects.append(rel_dir)
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        if args.no_recursive:
            dirnames[:] = []
        for name in filenames:
            if name in SKIP_NAMES or name.startswith(".organize_log_") or name.startswith("."):
                continue
            full = os.path.join(dirpath, name)
            try:
                st = os.stat(full)
            except OSError:
                continue
            ext = os.path.splitext(name)[1].lower().lstrip(".")
            rec = {
                "path": os.path.relpath(full, root),
                "ext": ext,
                "category": category(ext),
                "size": st.st_size,
                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            }
            stem = os.path.splitext(name)[0]
            if name.startswith("~$") or ext in TEMP_EXTS:
                rec["temp"] = True
                temp_files.append(rec["path"])
            if VERSION_RE.search(stem):
                rec["version_hint"] = True
            files.append(rec)
            by_size[st.st_size].append(rec)

    duplicates = []
    for size, group in by_size.items():
        if len(group) < 2 or size == 0:
            continue
        by_hash = defaultdict(list)
        for rec in group:
            try:
                by_hash[file_hash(os.path.join(root, rec["path"]))].append(rec["path"])
            except OSError:
                pass
        duplicates += [sorted(p, key=len) for p in by_hash.values() if len(p) > 1]

    mtimes = sorted(f["mtime"] for f in files)
    summary = {
        "total_files": len(files),
        "total_size_mb": round(sum(f["size"] for f in files) / 1e6, 1),
        "by_category": dict(Counter(f["category"] for f in files).most_common()),
        "top_extensions": dict(Counter(f["ext"] or "(無)" for f in files).most_common(15)),
        "date_range": [mtimes[0], mtimes[-1]] if mtimes else None,
        "duplicate_groups": len(duplicates),
        "temp_files": len(temp_files),
        "version_hint_files": sum(1 for f in files if f.get("version_hint")),
        "project_folders_kept": projects,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"root": root, "summary": summary, "files": files, "duplicates": duplicates},
                  f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
