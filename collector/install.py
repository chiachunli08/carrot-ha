"""Install one non-blocking /data/continue.sh hook, leaving the git checkout intact."""
import json
import os
import shutil
import subprocess
from pathlib import Path

BASE=Path('/data/id4-collector')
HOOK=Path('/data/continue.sh')
MARKER='# CARROT_HA_COLLECTOR_V03'
LINE='[ ! -f /data/id4-collector/enabled ] || nohup bash /data/id4-collector/supervisor.sh >/dev/null 2>&1 < /dev/null &'

def main():
    if Path(__file__).resolve().parent!=BASE:raise SystemExit('Copy this folder to /data/id4-collector first.')
    if not HOOK.is_file() or HOOK.is_symlink():raise SystemExit('Unsupported startup file: /data/continue.sh. Nothing changed; send this message.')
    source=HOOK.read_text()
    if 'launch_openpilot' not in source and 'launch_chffrplus' not in source:
        raise SystemExit('Unrecognized continue.sh. Nothing changed; startup review required.')
    if not source.startswith('#!') or 'bash' not in source.splitlines()[0]:raise SystemExit('Expected bash startup. Nothing changed.')
    if subprocess.run(['bash','-n',str(HOOK)]).returncode:raise SystemExit('Existing startup syntax error. Nothing changed.')
    from openpilot.cereal import messaging
    from openpilot.common.params import Params
    if Params().get_bool('IsOnroad'):raise SystemExit('Install while parked/offroad. Nothing changed.')
    import wayon_vehicle_telemetry as reference
    config_path=BASE/'connection.json'
    if config_path.exists():
        config=json.loads(config_path.read_text())
    else:
        config=json.loads(Path('/data/id4-cloud-import/connection.json').read_text())
        fd=os.open(config_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:json.dump(config,f)
    profile=reference.normalize_vehicle_profile(config.get('vehicle_profile'))
    # MEB needs its DBC. IONIQ 5 is a passive ISO-TP observer and needs no DBC.
    if profile=='vw_meb':
        from opendbc.can import CANParser
        CANParser('vw_meb',[(x,0) for x in ['Motor_16','HVEM_02','MEB_HVEM_01','BMS_04','Diagnose_01','Klima_Sensor_02','Klima_11','Klima_12']],0)
    if MARKER not in source:
        backup=BASE/'continue.sh.before-carrot-ha'
        if not backup.exists():shutil.copy2(HOOK,backup)
        lines=source.splitlines(keepends=True)
        patched=lines[0]+MARKER+'\n'+LINE+'\n'+''.join(lines[1:])
        temp=HOOK.with_name('continue.sh.carrot-ha.tmp')
        temp.write_text(patched);os.chmod(temp,HOOK.stat().st_mode)
        if subprocess.run(['bash','-n',str(temp)]).returncode:raise SystemExit('New hook syntax invalid; original unchanged.')
        temp.replace(HOOK)
    (BASE/'enabled').touch()
    subprocess.Popen(['bash',str(BASE/'supervisor.sh')],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    print('Installed '+profile+'. Git checkout unchanged. Startup backup: /data/id4-collector/continue.sh.before-carrot-ha')
    print('Wait 90 seconds, then: python3 /data/id4-collector/status.py')

if __name__=='__main__':main()
