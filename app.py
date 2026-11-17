import os
from flask import Flask, jsonify, render_template_string, send_from_directory

app = Flask(__name__)

HTML = r"""
<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#090909">
  <meta name="description" content="IBROHIM CALCULATOR — qora va oltin premium kalkulyator.">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%23090909'/%3E%3Ctext x='50' y='67' font-size='55' text-anchor='middle' fill='%23d8b45a'%3E I %3C/text%3E%3C/svg%3E">
  <title>IBROHIM CALCULATOR</title>
  <style>
    :root{--bg:#090909;--panel:#141414;--panel2:#1b1b1b;--gold:#d8b45a;--gold2:#f2d58a;--muted:#8c877b;--text:#f7f3e9;--line:#30291a;--danger:#d77b70}
    *{box-sizing:border-box} body{margin:0;background:radial-gradient(ellipse at 50% -15%,#302512 0,#111 34%,var(--bg) 70%);color:var(--text);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;min-height:100vh}
    button,input,select{font:inherit} .wrap{max-width:1120px;margin:auto;padding:22px 16px 42px}
    header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:22px}
    .brand{display:flex;align-items:center;gap:12px}.logo{width:46px;height:46px;border:1px solid var(--gold);border-radius:14px;display:grid;place-items:center;color:var(--gold2);font-weight:900;font-size:23px;box-shadow:0 0 24px #d8b45a20}
    h1{font-size:clamp(17px,3vw,22px);letter-spacing:1.8px;margin:0}.tag{font-size:10px;color:var(--gold);letter-spacing:2.2px;margin-top:4px}
    .install{border:1px solid #80652e;color:var(--gold2);background:#1b160c;border-radius:12px;padding:10px 13px;cursor:pointer;font-size:12px}
    .layout{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);gap:18px}
    .card{background:linear-gradient(145deg,#171717,#101010);border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 18px 55px #0008}
    .display{min-height:145px;padding:12px 8px 18px;display:flex;flex-direction:column;justify-content:flex-end;text-align:right;overflow:hidden}
    .expression{color:var(--muted);font-size:clamp(17px,3vw,23px);min-height:32px;overflow-wrap:anywhere}
    .result{font-size:clamp(34px,7vw,52px);font-weight:650;letter-spacing:-1.5px;color:var(--gold2);overflow-wrap:anywhere}
    .keys{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
    .key{border:1px solid #29251d;background:linear-gradient(145deg,#242424,#191919);color:var(--text);border-radius:15px;min-height:62px;font-size:20px;cursor:pointer;transition:.15s;box-shadow:0 4px 0 #080808}
    .key:active{transform:translateY(2px);box-shadow:0 2px 0 #080808}.key.fn{color:var(--gold2);background:#211b10;border-color:#4a3a1c}.key.op{color:var(--gold);font-size:23px}.key.equal{background:linear-gradient(135deg,#e6c878,#b78b35);color:#17120a;border:0;font-weight:800}.key.zero{grid-column:span 2}
    .tabs{display:flex;gap:7px;overflow:auto;padding-bottom:12px;margin-bottom:12px}.tab{white-space:nowrap;background:#171717;color:#aaa18e;border:1px solid #332a1a;border-radius:999px;padding:9px 13px;font-size:12px;cursor:pointer}.tab.active{background:#332713;color:var(--gold2);border-color:#9b7733}
    .toolpane{display:none}.toolpane.active{display:block}.toolpane h2{font-size:17px;margin:5px 0 15px}.field{display:grid;gap:6px;margin:12px 0}.field label{font-size:12px;color:#b5ad9c}.field input,.field select{width:100%;background:#0b0b0b;color:var(--text);border:1px solid #3a3020;border-radius:12px;padding:13px;outline:none}.field input:focus,.field select:focus{border-color:var(--gold)}
    .action{width:100%;padding:13px;border:0;border-radius:12px;background:linear-gradient(135deg,#e6c878,#b78b35);color:#17120a;font-weight:800;cursor:pointer;margin-top:6px}
    .answer{margin-top:13px;padding:14px;border:1px solid #4b3b1d;border-radius:13px;color:var(--gold2);background:#211a0d;min-height:48px;overflow-wrap:anywhere}
    .history-head{display:flex;align-items:center;justify-content:space-between;margin:0 0 10px}.history-head h2{font-size:15px;margin:0}.clear{background:transparent;color:var(--muted);border:0;cursor:pointer;font-size:12px}.history{display:grid;gap:8px;max-height:290px;overflow:auto}.history-item{padding:10px 12px;border-radius:11px;background:#0d0d0d;border:1px solid #252017;cursor:pointer}.history-item small{display:block;color:var(--muted);font-size:11px}.history-item strong{display:block;color:var(--gold2);text-align:right;font-size:16px;margin-top:3px}.empty{color:#777064;font-size:13px;padding:15px 2px}
    .foot{text-align:center;color:#716b5f;font-size:11px;margin-top:22px;letter-spacing:.6px}
    @media(max-width:760px){.wrap{padding:15px 12px 30px}.layout{grid-template-columns:1fr}.card{padding:14px}.key{min-height:59px}.display{min-height:128px}.history{max-height:180px}}
    @media(min-width:761px){.calculator{position:sticky;top:16px;align-self:start}}
  </style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand"><div class="logo">I</div><div><h1>IBROHIM CALCULATOR</h1><div class="tag">PRECISION • SIMPLICITY • LUXURY</div></div></div>
    <button class="install" id="installBtn" hidden>＋ O‘rnatish</button>
  </header>

  <main class="layout">
    <section class="card calculator">
      <div class="display">
        <div class="expression" id="expression">0</div>
        <div class="result" id="result">0</div>
      </div>
      <div class="keys" id="keys">
        <button class="key fn" data-action="clear">AC</button>
        <button class="key fn" data-action="delete">⌫</button>
        <button class="key fn" data-value="%">%</button>
        <button class="key op" data-value="÷">÷</button>
        <button class="key" data-value="7">7</button><button class="key" data-value="8">8</button><button class="key" data-value="9">9</button><button class="key op" data-value="×">×</button>
        <button class="key" data-value="4">4</button><button class="key" data-value="5">5</button><button class="key" data-value="6">6</button><button class="key op" data-value="−">−</button>
        <button class="key" data-value="1">1</button><button class="key" data-value="2">2</button><button class="key" data-value="3">3</button><button class="key op" data-value="+">+</button>
        <button class="key zero" data-value="0">0</button><button class="key" data-value=".">.</button><button class="key equal" data-action="equals">=</button>
      </div>
    </section>

    <section class="card">
      <div class="tabs">
        <button class="tab active" data-tab="history">Tarix</button>
        <button class="tab" data-tab="discount">Chegirma</button>
        <button class="tab" data-tab="loan">Kredit</button>
        <button class="tab" data-tab="bmi">BMI</button>
        <button class="tab" data-tab="currency">Valyuta</button>
      </div>
      <div class="toolpane active" id="pane-history">
        <div class="history-head"><h2>Hisoblash tarixi</h2><button class="clear" id="clearHistory">Tozalash</button></div>
        <div class="history" id="history"><div class="empty">Hozircha hisoblashlar yo‘q.</div></div>
      </div>
      <div class="toolpane" id="pane-discount">
        <h2>Chegirma kalkulyatori</h2>
        <div class="field"><label>Mahsulot narxi</label><input id="price" type="number" min="0" placeholder="Masalan, 250000"></div>
        <div class="field"><label>Chegirma (%)</label><input id="percent" type="number" min="0" max="100" placeholder="Masalan, 15"></div>
        <button class="action" onclick="discountCalc()">Hisoblash</button><div class="answer" id="discountAnswer">Natija shu yerda chiqadi.</div>
      </div>
      <div class="toolpane" id="pane-loan">
        <h2>Kredit kalkulyatori</h2>
        <div class="field"><label>Kredit summasi</label><input id="loanAmount" type="number" min="0" placeholder="Masalan, 10000000"></div>
        <div class="field"><label>Yillik foiz (%)</label><input id="loanRate" type="number" min="0" step="0.1" placeholder="Masalan, 24"></div>
        <div class="field"><label>Muddat (oy)</label><input id="loanMonths" type="number" min="1" placeholder="Masalan, 12"></div>
        <button class="action" onclick="loanCalc()">Oylik to‘lovni hisoblash</button><div class="answer" id="loanAnswer">Natija shu yerda chiqadi.</div>
      </div>
      <div class="toolpane" id="pane-bmi">
        <h2>Tana massasi indeksi</h2>
        <div class="field"><label>Vazn (kg)</label><input id="weight" type="number" min="1" placeholder="Masalan, 70"></div>
        <div class="field"><label>Bo‘y (sm)</label><input id="height" type="number" min="1" placeholder="Masalan, 175"></div>
        <button class="action" onclick="bmiCalc()">BMI hisoblash</button><div class="answer" id="bmiAnswer">Natija shu yerda chiqadi.</div>
      </div>
      <div class="toolpane" id="pane-currency">
        <h2>Valyuta konvertori</h2>
        <div class="field"><label>Miqdor</label><input id="currencyAmount" type="number" min="0" value="1"></div>
        <div class="field"><label>Dan</label><select id="fromCurrency"><option>USD</option><option>EUR</option><option>UZS</option><option>RUB</option><option>GBP</option><option>TRY</option></select></div>
        <div class="field"><label>Ga</label><select id="toCurrency"><option>UZS</option><option>USD</option><option>EUR</option><option>RUB</option><option>GBP</option><option>TRY</option></select></div>
        <button class="action" onclick="currencyCalc()">Konvertatsiya qilish</button><div class="answer" id="currencyAnswer">Valyuta kursi internet orqali olinadi.</div>
        <div style="color:#777064;font-size:11px;margin-top:8px">Kurslar taxminiy bo‘lishi mumkin. Moliyaviy bitimdan oldin bank kursini tekshiring.</div>
      </div>
    </section>
  </main>
  <div class="foot">IBROHIM CALCULATOR · BLACK & GOLD EDITION</div>
</div>
<script>
let expr = "";
let justEvaluated = false;
const $ = id => document.getElementById(id);
const pretty = n => {
  if (!Number.isFinite(n)) throw new Error("Nolga bo‘lish yoki noto‘g‘ri hisob.");
  return Number(n.toPrecision(12)).toLocaleString("en-US",{maximumFractionDigits:10});
};
function render(){ $("expression").textContent = expr || "0"; try{$("result").textContent = expr ? pretty(safeEval(expr)) : "0";}catch(e){$("result").textContent="";} }
function safeEval(source){
  let s=source.replace(/×/g,"*").replace(/÷/g,"/").replace(/−/g,"-").replace(/,/g,"");
  if(!/^[0-9+\-*/().%\s]+$/.test(s)) throw new Error("Noto‘g‘ri ifoda");
  s=s.replace(/(\d+(?:\.\d+)?)%/g,"($1/100)");
  const tokens=s.match(/\d+(?:\.\d+)?|[()+\-*/]/g)||[]; let i=0;
  function atom(){
    const t=tokens[i++];
    if(t==="+") return atom(); if(t==="-") return -atom();
    if(t==="("){const v=add();if(tokens[i++]!==")")throw Error();return v;}
    if(t===undefined||!/^(\d+\.?\d*|\.\d+)$/.test(t))throw Error();
    return Number(t);
  }
  function mul(){let v=atom();while(tokens[i]==="*"||tokens[i]==="/"){const op=tokens[i++],b=atom();v=op==="*"?v*b:v/b;}return v;}
  function add(){let v=mul();while(tokens[i]==="+"||tokens[i]==="-"){const op=tokens[i++],b=mul();v=op==="+"?v+b:v-b;}return v;}
  const value=add();if(i!==tokens.length)throw Error("Ifoda xato");return value;
}
function push(v){if(justEvaluated && /[0-9.]/.test(v))expr="";justEvaluated=false;expr+=v;render();}
function equals(){try{const val=safeEval(expr);const row={expr,result:pretty(val),time:new Date().toLocaleString()};let h=JSON.parse(localStorage.getItem("ibrohimHistory")||"[]");h.unshift(row);localStorage.setItem("ibrohimHistory",JSON.stringify(h.slice(0,40)));expr=String(Number(val.toPrecision(12)));$("expression").textContent=row.expr+" =";$("result").textContent=pretty(val);justEvaluated=true;showHistory();}catch(e){$("result").textContent="Xatolik";}}
$("keys").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;if(b.dataset.action==="clear"){expr="";justEvaluated=false;render();}else if(b.dataset.action==="delete"){expr=expr.slice(0,-1);render();}else if(b.dataset.action==="equals")equals();else if(b.dataset.value)push(b.dataset.value);});
document.addEventListener("keydown",e=>{if(/[0-9.+\-*/()%]/.test(e.key)&&e.key.length===1)push(e.key.replace("*","×").replace("/","÷"));else if(e.key==="Enter")equals();else if(e.key==="Backspace"){$("keys").querySelector('[data-action="delete"]').click();}else if(e.key==="Escape")$("keys").querySelector('[data-action="clear"]').click();});
function showHistory(){const h=JSON.parse(localStorage.getItem("ibrohimHistory")||"[]");$("history").innerHTML=h.length?h.map((x,i)=>`<div class="history-item" data-index="${i}"><small>${x.time} · ${x.expr}</small><strong>${x.result}</strong></div>`).join(""):'<div class="empty">Hozircha hisoblashlar yo‘q.</div>';}
$("history").addEventListener("click",e=>{const item=e.target.closest(".history-item");if(!item)return;const h=JSON.parse(localStorage.getItem("ibrohimHistory")||"[]");expr=h[+item.dataset.index].expr;justEvaluated=false;render();});
$("clearHistory").onclick=()=>{localStorage.removeItem("ibrohimHistory");showHistory();};
document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===b));document.querySelectorAll(".toolpane").forEach(x=>x.classList.toggle("active",x.id==="pane-"+b.dataset.tab));});
function money(n){return new Intl.NumberFormat("uz-UZ",{maximumFractionDigits:2}).format(n);}
function discountCalc(){const p=+$("price").value,d=+$("percent").value;if(p<0||d<0||d>100||!$("price").value||!$("percent").value){$("discountAnswer").textContent="Narx va chegirma foizini to‘g‘ri kiriting (0–100%).";return;}const save=p*d/100;$("discountAnswer").innerHTML=`Chegirma: <b>${money(save)}</b><br>Yakuniy narx: <b>${money(p-save)}</b>`;}
function loanCalc(){const p=+$("loanAmount").value,r=+$("loanRate").value/1200,n=+$("loanMonths").value;if(p<=0||r<0||n<=0||!Number.isFinite(n)){$("loanAnswer").textContent="Barcha maydonlarni to‘g‘ri to‘ldiring.";return;}const m=r===0?p/n:p*r/(1-Math.pow(1+r,-n));$("loanAnswer").innerHTML=`Taxminiy oylik to‘lov: <b>${money(m)}</b><br>Jami to‘lov: <b>${money(m*n)}</b>`;}
function bmiCalc(){const w=+$("weight").value,h=+$("height").value/100;if(w<=0||h<=0){$("bmiAnswer").textContent="Vazn va bo‘yni kiriting.";return;}const bmi=w/(h*h);const label=bmi<18.5?"Vazn yetishmasligi":bmi<25?"Me'yor":bmi<30?"Ortiqcha vazn":"Semizlik diapazoni";$("bmiAnswer").innerHTML=`BMI: <b>${bmi.toFixed(1)}</b><br>${label}<br><small>Bu umumiy ko‘rsatkich, tibbiy tashxis emas.</small>`;}
async function currencyCalc(){const amount=+$("currencyAmount").value,from=$("fromCurrency").value,to=$("toCurrency").value;if(amount<0||!Number.isFinite(amount)){$("currencyAnswer").textContent="Miqdorni kiriting.";return;}if(from===to){$("currencyAnswer").textContent=money(amount)+" "+to;return;}$("currencyAnswer").textContent="Kurs yuklanmoqda…";try{const res=await fetch(`https://open.er-api.com/v6/latest/${from}`);if(!res.ok)throw Error();const data=await res.json();if(data.result!=="success"||!data.rates[to])throw Error();$("currencyAnswer").innerHTML=`Natija: <b>${money(amount*data.rates[to])} ${to}</b><br><small>Kurs sanasi: ${data.time_last_update_utc||"noma'lum"}</small>`;}catch(e){$("currencyAnswer").textContent="Kursni olish imkoni bo‘lmadi. Internetni tekshiring."}}
showHistory();render();
let installPrompt;window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();installPrompt=e;$("installBtn").hidden=false;});$("installBtn").onclick=async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;$("installBtn").hidden=true;};
if("serviceWorker" in navigator)window.addEventListener("load",()=>navigator.serviceWorker.register("/sw.js").catch(()=>{}));
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/manifest.json")
def manifest():
    return jsonify({
        "name": "IBROHIM CALCULATOR",
        "short_name": "IBROHIM CALC",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#090909",
        "theme_color": "#090909",
        "description": "Qora va oltin premium kalkulyator",
        "icons": []
    })

@app.get("/sw.js")
def service_worker():
    js = """
const CACHE='ibrohim-calculator-v1';
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/','/manifest.json']))));
self.addEventListener('fetch',e=>{if(e.request.method==='GET' && new URL(e.request.url).origin===location.origin){e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return res;}).catch(()=>caches.match('/'))));}});
"""
    return app.response_class(js, mimetype="application/javascript")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
