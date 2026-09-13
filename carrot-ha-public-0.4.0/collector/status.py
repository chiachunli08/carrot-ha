import json
import time
from pathlib import Path
base=Path(__file__).resolve().parent
for name in ['status.json','delivery.json']:
    path=base/'state'/name
    if not path.exists():print(name,': waiting');continue
    data=json.loads(path.read_text());data['age_seconds']=round(time.time()-data.get('at',0))
    print(name,json.dumps(data,indent=2))
