import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker from './src/worker.js';
const sqlite = new DatabaseSync(':memory:');
sqlite.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
const env = {SNAPSHOTS:{}, WAYON_UPLOAD_TOKEN:'upload-test', WAYON_VIEW_TOKEN:'view-test', DB:{prepare(sql){
  const statement = sqlite.prepare(sql); let values=[];
  return {bind(...args){values=args; return this}, async run(){return statement.run(...values)}, async all(){return {results:statement.all(...values)}}, async first(){return statement.get(...values)??null}};
}}};
async function request(path, token='view-test', body){
  const r = new Request('https://example.test'+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});
  return worker.fetch(r,env,{});
}
assert.equal((await request('/api/json','wrong')).status,401);
assert.equal((await request('/api/remote/session','upload-test',{})).status,404);
assert.equal((await request('/api/live/session','upload-test',{})).status,404);
for(let i=0;i<27;i++){
  const payload={id:'trip-'+i, deviceId:'test-id4',startedAt:'2026-09-09T00:00:00Z',endedAt:'2026-09-09T01:00:00Z',distanceM:10000,durationS:3600,route:[{latitude:37,longitude:127,speedMps:3}]};
  assert.equal((await request('/api/trips','view-test',payload)).status,401);
  assert.equal((await (await request('/api/trips','upload-test',payload)).json()).id,payload.id);
}
const ids=new Set();
for(let offset=0;offset<30;offset+=10){
  const result=await (await request(`/api/trips?limit=10&offset=${offset}&include_route=true`)).json();
  for(const trip of result.trips){ids.add(trip.id);assert.equal(trip.route[0].latitude,37);}
}
assert.equal(ids.size,27);
const telemetry={deviceId:'test-id4',updatedAt:'2026-09-09T01:00:00Z',onroad:false,vehicle:{battery_wh:24050,odometer_km:75248}};
assert.equal((await request('/api/telemetry','upload-test',telemetry)).status,200);
const feed=await (await request('/api/json')).json();
assert.equal(JSON.parse(feed.state.raw_json).vehicle.battery_wh,24050);
assert.equal(feed.trips.length,25);
assert.equal(feed.vehicleStatus,null);
sqlite.close();
console.log('PASS: original telemetry/trip schema, upload/view auth, 27 trips paginated with routes, remote endpoints disabled');
