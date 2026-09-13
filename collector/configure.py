"""Interactive credentials for a new installation; never prints secrets."""
import getpass,json,os
from pathlib import Path
from urllib.parse import urlsplit

def main():
    path=Path(__file__).resolve().parent/'connection.json'
    if path.exists():raise SystemExit('connection.json already exists. Preserved; do not reconfigure an existing device.')
    url=input('Worker HTTPS URL: ').strip().rstrip('/')
    parsed=urlsplit(url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.path or parsed.query or parsed.fragment or parsed.username:raise SystemExit('Invalid base URL')
    device=input('Device ID (same as HA): ').strip()
    token=getpass.getpass('UPLOAD token (hidden): ').strip()
    if not device or len(token)<32:raise SystemExit('Device ID and token of at least 32 characters required')
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'w') as f:json.dump(dict(url=url,device=device,token=token),f)
    print('Saved. Next run install.py while parked.')

if __name__=='__main__':main()
