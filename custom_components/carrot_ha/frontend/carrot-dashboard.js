// Stable resource URL. Keep this bootstrap small and backwards compatible.
const response=await fetch(new URL('/api/carrot_ha/frontend-version',import.meta.url),{cache:'no-store',credentials:'same-origin'});
if(!response.ok)throw new Error(`Carrot HA version check failed (${response.status}). Restart Home Assistant and reload the dashboard.`);
const {version}=await response.json();
if(typeof version!=='string'||!/^\d+\.\d+\.\d+(?:[-+.][A-Za-z0-9.-]+)?$/.test(version))throw new Error('Carrot HA returned an invalid frontend version.');
const runtime=new URL('./carrot-dashboard-runtime.js',import.meta.url);
runtime.searchParams.set('v',version);
await import(runtime.href);
