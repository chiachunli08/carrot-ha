from pathlib import Path
import subprocess
base=Path('/data/id4-collector')
(base/'enabled').unlink(missing_ok=True)
# Remove only our marked two-line hook; preserve subsequent user/upstream edits.
hook=Path('/data/continue.sh')
lines=hook.read_text().splitlines(keepends=True)
for i,line in enumerate(lines):
    if line.strip()=='# CARROT_HA_COLLECTOR_V03' and i+1<len(lines) and '/data/id4-collector/supervisor.sh' in lines[i+1]:
        del lines[i:i+2];hook.write_text(''.join(lines));break
subprocess.run(['pkill','-f','^/usr/local/venv/bin/python3 -u collector.py$'],check=False)
print('Collector disabled. Stored data and git checkout preserved.')
