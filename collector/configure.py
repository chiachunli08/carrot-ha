"""Interactive credentials for a new installation; never prints secrets."""
import argparse,getpass,json,os
from pathlib import Path
from urllib.parse import urlsplit

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--vehicle-profile',choices=('vw_meb','ioniq5'))
    args=parser.parse_args()
    path=Path(__file__).resolve().parent/'connection.json'
    if args.vehicle_profile:
        if not path.exists():raise SystemExit('connection.json does not exist. Run configure.py without arguments first.')
        try:config=json.loads(path.read_text())
        except (OSError,ValueError):raise SystemExit('connection.json is invalid; preserved unchanged.')
        if not isinstance(config,dict):raise SystemExit('connection.json is invalid; preserved unchanged.')
        config['vehicle_profile']=args.vehicle_profile
        temp=path.with_suffix('.tmp')
        fd=os.open(temp,os.O_CREAT|os.O_TRUNC|os.O_WRONLY,0o600)
        with os.fdopen(fd,'w') as f:json.dump(config,f)
        os.replace(temp,path)
        print('Vehicle profile updated to '+args.vehicle_profile+'. Reboot to restart the collector.')
        return
    if path.exists():raise SystemExit('connection.json already exists. Preserved; do not reconfigure an existing device.')
    url=input('Worker HTTPS URL: ').strip().rstrip('/')
    parsed=urlsplit(url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.path or parsed.query or parsed.fragment or parsed.username:raise SystemExit('Invalid base URL')
    device=input('Device ID (same as HA): ').strip()
    token=getpass.getpass('UPLOAD token (hidden): ').strip()
    profile=input('Vehicle profile [vw_meb/ioniq5] (default vw_meb): ').strip().lower() or 'vw_meb'
    if profile not in ('vw_meb','ioniq5'):raise SystemExit('Vehicle profile must be vw_meb or ioniq5')
    if not device or len(token)<32:raise SystemExit('Device ID and token of at least 32 characters required')
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'w') as f:json.dump(dict(url=url,device=device,token=token,vehicle_profile=profile),f)
    print('Saved. Next run install.py while parked.')

if __name__=='__main__':main()
