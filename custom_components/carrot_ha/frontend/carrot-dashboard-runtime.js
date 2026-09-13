const version=new URL(import.meta.url).searchParams.get('v');
if(!version)throw new Error('Carrot HA: load carrot-dashboard.js, not the runtime directly.');
const moduleURL=name=>{const url=new URL(name,import.meta.url);url.searchParams.set('v',version);return url.href;};
const [{default:KoreanDashboard},{default:EnglishDashboard}]=await Promise.all([
  import(moduleURL('./carrot-dashboard-ko.js')),
  import(moduleURL('./carrot-dashboard-en.js'))
]);
if(!customElements.get('carrot-dashboard-ko'))customElements.define('carrot-dashboard-ko', KoreanDashboard);
if(!customElements.get('carrot-dashboard-en'))customElements.define('carrot-dashboard-en', EnglishDashboard);
class LocalizedDashboard extends HTMLElement {
  constructor(){super();this.style.display='block';}
  setConfig(config){this.config=config;this.updateLanguage();}
  set hass(hass){this._hass=hass;this.updateLanguage();}
  getCardSize(){return this.card?.getCardSize()??8;}
  getGridOptions(){return {columns:36,rows:'auto',min_columns:6};}
  updateLanguage(){
    if(!this.config)return;
    const requested=this.config.language;
    const language=(!requested||requested==='auto')?(this._hass?.locale?.language||this._hass?.language||navigator.language):requested;
    const lang=String(language).toLowerCase().startsWith('ko')?'ko':'en';
    if(this.lang!==lang){
      this.card?.remove();this.lang=lang;
      this.card=document.createElement('carrot-dashboard-'+lang);
      this.replaceChildren(this.card);
    }
    if(this.appliedConfig!==this.config||this.configuredCard!==this.card){this.card.setConfig(this.config);this.appliedConfig=this.config;this.configuredCard=this.card;}
    if(this._hass)this.card.hass=this._hass;
  }
}
if(!customElements.get('carrot-history-card'))customElements.define('carrot-history-card',LocalizedDashboard);
if(!customElements.get('carrot-dashboard-card'))customElements.define('carrot-dashboard-card',class extends LocalizedDashboard{});
window.customCards=window.customCards||[];
window.customCards.push({type:'carrot-dashboard-card',name:'Carrot HA — MEB',description:'Vehicle, trips, charging and battery history / 차량·주행·충전'});
