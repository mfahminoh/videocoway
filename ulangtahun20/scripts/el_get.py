"""Muat turun take ElevenLabs dan potong ke ayat.  python scripts/el_get.py V02 '<url>'"""
import subprocess, sys
import vo
from common import AUDIO, load_videos

vid, url = sys.argv[1], sys.argv[2]
dst = AUDIO / "el" / f"{vid}.mp3"
dst.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(["curl", "-s", "--retry", "3", "-o", str(dst), url], check=True)
v = next(x for x in load_videos() if x["id"] == vid)
vo.from_file(v, dst)
vo.assemble(v)
