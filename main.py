"""Operator roast one-liner: gate check pipeline, JSON receipt, 140 char cap."""

import json
import os
from pathlib import Path

CAP = 140
TAG = "ryo-11260042"


def pipeline(handle):
    blob = handle.read()
    squeezed = " ".join(blob.split())
    yield squeezed
    yield "blank" if not squeezed else f"{len(squeezed)} chars"


def main():
    src = Path(__file__).resolve().parent / "entry.txt"
    flow = pipeline(src.open(encoding="utf-8"))
    line = next(flow)
    detail = next(flow)
    if not line:
        print(json.dumps({"status": "REFUSED", "detail": detail}))
        raise SystemExit(1)
    if len(line) > CAP:
        print(json.dumps({"status": "REFUSED", "detail": detail}))
        raise SystemExit(1)
    zone = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    zone.mkdir(parents=True, exist_ok=True)
    (zone / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "ACCEPTED", "detail": detail, "wrote": str(zone / "entry.txt"), "tag": TAG}))


if __name__ == "__main__":
    main()
