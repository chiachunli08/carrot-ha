import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker from './src/worker.js';
const db=new DatabaseSync(':memory:');db.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
const env={SNAPSHOTS:{},WAYON_UPLOAD_TOKEN:'upload',WAYON_VIEW_TOKEN:'view',DB:{prepare(sql){
 let args=[];const stmt=db.prepare(sql);
 return {bind(...v){args=v;return this},async run(){return stmt.run(...args)},async first(){return stmt.get(...args)||null},async all(){return {results:stmt.all(...args)}}};
}}};
async function call(path,body,token=body?'upload':'view'){
 return worker.fetch(new Request('https://example.test'+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined}),env,{});
}
const state=t=>({deviceId:'test-id4',updatedAt:`2026-09-10T00:0${t}:00Z`,onroad:false,vehicle:{battery_wh:20000+t*100,charge_sessions:[]}});
for(const t of [2,1,2])assert.equal((await call('/api/telemetry',state(t))).status,200);
assert.equal((await call('/api/telemetry-history',null,'bad')).status,401);
let page=await (await call('/api/telemetry-history?limit=1')).json();assert.equal(page.events.length,1);assert.equal(page.has_more,true);
page=await (await call(`/api/telemetry-history?after=${page.events[0].sequence}`)).json();assert.equal(page.events.length,1);assert.equal(page.has_more,false);
assert.equal(JSON.parse((await (await call('/api/json')).json()).state.raw_json).vehicle.battery_wh,20200);
assert.equal(db.prepare('SELECT COUNT(*) AS n FROM telemetry_history').get().n,2);
console.log('PASS: telemetry history, cursor, deduplication, older replay does not replace latest, read authentication');
db.close();
