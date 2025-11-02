import React from "react";

export default function ChatJuridicoUITeste(){
  return <ChatPro />
}

function ChatPro(){
  const [baseUrl, setBaseUrl] = React.useState(()=>localStorage.getItem("cj_base")||"http://127.0.0.1:8000");
  const [mode, setMode] = React.useState(()=>localStorage.getItem("cj_mode")||"rag"); // chat | rag | agent
  const [openSettings, setOpenSettings] = React.useState(false);
  React.useEffect(()=>localStorage.setItem("cj_base", baseUrl),[baseUrl]);
  React.useEffect(()=>localStorage.setItem("cj_mode", mode),[mode]);

  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const listRef = React.useRef(null);

  React.useEffect(()=>{ listRef.current?.scrollTo({top:listRef.current.scrollHeight, behavior:"smooth"}) },[messages,loading]);

  function push(role, content, extra={}){
    setMessages(m=>[...m,{ id: crypto.randomUUID(), role, content, ...extra }]);
  }

  async function send(){
    const text = input.trim();
    if(!text || loading) return;
    setInput("");
    push("user", text);
    setLoading(true);
    try{
      let url = baseUrl;
      let payload = {};
      if(mode==='chat'){ url += '/chat'; payload = { message: text }; }
      else if(mode==='rag'){ url += '/rag/query'; payload = { query: text }; }
      else { url += '/agent/route'; payload = { text }; }

      const res = await fetch(url,{ method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
      const json = await res.json();

      if(mode==='agent'){
        push('assistant','OK, segue o resultado do agente:', { agent: json });
      } else {
        const answer = json.answer ?? JSON.stringify(json,null,2);
        const parsed = parseRagAnswer(answer);
        push('assistant', parsed.text, { sources: parsed.sources });
      }
    }catch(e){ push('assistant', `Erro: ${e?.message||e}`); }
    finally{ setLoading(false); }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-zinc-100 text-zinc-900">
      <TopBar onSettings={()=>setOpenSettings(true)} mode={mode} setMode={setMode} />

      <div className="max-w-5xl mx-auto px-4 pb-28">
        <Hero />
        <div ref={listRef} className="bg-white border border-zinc-200 rounded-3xl shadow-sm p-4 md:p-6 h-[60vh] overflow-auto">
          {messages.length===0 && <EmptyState/>}
          <ul className="space-y-4">
            {messages.map(msg=> (
              <li key={msg.id} className={`flex ${msg.role==='user' ? 'justify-end' : 'justify-start'}`}>
                <Bubble role={msg.role} content={msg.content} sources={msg.sources} agent={msg.agent}/>
              </li>
            ))}
            {loading && (
              <li className="flex justify-start"><Bubble role="assistant" content={<TypingDots/>}/></li>
            )}
          </ul>
        </div>
      </div>

      <Composer value={input} onChange={setInput} onSend={send} placeholder={mode==='rag' ? 'Pergunte algo sobre juridico.' : mode==='agent' ? 'Descreva a demanda do cliente…' : 'Converse com o LLM…'} />

      {openSettings && <SettingsModal baseUrl={baseUrl} setBaseUrl={setBaseUrl} onClose={()=>setOpenSettings(false)} />}
    </div>
  )
}

function TopBar({ onSettings, mode, setMode }){
  return (
    <header className="sticky top-0 z-10 backdrop-blur supports-[backdrop-filter]:bg-white/70 bg-white/90 border-b border-zinc-200">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-zinc-900 text-white grid place-items-center font-bold">CJ</div>
        <div className="mr-auto">
          <div className="font-semibold leading-tight">Chat Jurídico</div>
          <div className="text-xs text-zinc-500">LLM + RAG + Agente</div>
        </div>
        <ModeTabs mode={mode} setMode={setMode} />
        <button onClick={onSettings} className="ml-2 text-sm px-3 py-1.5 rounded-lg border border-zinc-300 hover:bg-zinc-50">Configurar</button>
      </div>
    </header>
  );
}

function ModeTabs({ mode, setMode }){
  const tabs = [ {id:'chat', label:'LLM'}, {id:'rag', label:'RAG'}, {id:'agent', label:'Agente'} ];
  return (
    <div className="flex items-center rounded-xl bg-zinc-100 p-1">
      {tabs.map(t=> (
        <button key={t.id} onClick={()=>setMode(t.id)} className={`text-sm px-3 py-1.5 rounded-lg transition ${mode===t.id? 'bg-white shadow border border-zinc-200' : 'text-zinc-600 hover:text-zinc-900'}`}>{t.label}</button>
      ))}
    </div>
  );
}

function Hero(){
  return (
    <div className="py-6">
      <h2 className="text-xl md:text-2xl font-semibold">laboratório de testes</h2>
      <p className="text-zinc-600 text-sm mt-1">Conecte no FastAPI e valide rapidamente as funções de chat, RAG e agente.</p>
    </div>
  );
}

function EmptyState(){
  return (
    <div className="text-center text-zinc-500 py-12">
      <div className="text-4xl mb-2">💬</div>
      <div className="font-medium">Sem mensagens ainda</div>
      <div className="text-sm">Selecione um modo acima, escreva sua pergunta e envie.</div>
    </div>
  );
}

function Bubble({ role, content, sources, agent }){
  const isUser = role==='user';
  return (
    <div className={`max-w-[80%] rounded-2xl px-4 py-3 border ${isUser? 'bg-zinc-900 text-white border-zinc-900' : 'bg-zinc-50 border-zinc-200'}`}>
      <div className="text-xs opacity-60 mb-1">{isUser? 'Você' : 'Assistente'}</div>
      <div className="whitespace-pre-wrap text-sm leading-relaxed">{content}</div>
      {sources && sources.length>0 && (
        <div className="mt-3 text-xs text-zinc-500">
          <div className="font-medium text-zinc-600 mb-1">Fontes</div>
          <ul className="list-disc pl-5 space-y-0.5">{sources.map(s=> <li key={s}>{s}</li>)}</ul>
        </div>
      )}
      {agent && (
        <div className="mt-3 text-xs">
          <div className="font-medium text-zinc-600 mb-1">Resultado do agente</div>
          <pre className="bg-white border border-zinc-200 rounded-xl p-2 overflow-auto max-h-56">{JSON.stringify(agent, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

function Composer({ value, onChange, onSend, placeholder }){
  function onKey(e){ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); onSend(); } }
  return (
    <div className="fixed bottom-0 inset-x-0 border-t border-zinc-200 bg-white/90 backdrop-blur">
      <div className="max-w-5xl mx-auto px-4 py-3 flex gap-3">
        <textarea value={value} onChange={e=>onChange(e.target.value)} onKeyDown={onKey} placeholder={placeholder} className="flex-1 min-h-[56px] max-h-40 resize-y rounded-2xl border border-zinc-300 px-3 py-3 outline-none focus:ring-2 focus:ring-zinc-400" />
        <button onClick={onSend} className="px-5 py-3 rounded-2xl bg-zinc-900 text-white hover:bg-zinc-800 active:bg-zinc-950">Enviar</button>
      </div>
    </div>
  );
}

function SettingsModal({ baseUrl, setBaseUrl, onClose }){
  return (
    <div className="fixed inset-0 bg-black/30 grid place-items-center p-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl border border-zinc-200">
        <div className="p-4 border-b border-zinc-100 flex items-center justify-between">
          <div className="font-semibold">Configurações</div>
          <button onClick={onClose} className="text-zinc-500 hover:text-zinc-900">✕</button>
        </div>
        <div className="p-5 grid gap-4">
          <label className="text-sm">
            <div className="text-zinc-600 mb-1">Base URL da API</div>
            <input value={baseUrl} onChange={e=>setBaseUrl(e.target.value)} className="w-full rounded-xl border border-zinc-300 px-3 py-2 outline-none focus:ring-2 focus:ring-zinc-400" />
          </label>
          <div className="text-xs text-zinc-500">Ex.: http://127.0.0.1:8000</div>
        </div>
        <div className="p-4 border-t border-zinc-100 flex justify-end">
          <button onClick={onClose} className="px-4 py-2 rounded-xl border border-zinc-300 hover:bg-zinc-50">Fechar</button>
        </div>
      </div>
    </div>
  );
}

function TypingDots(){
  return (
    <span className="inline-flex items-center gap-1 text-zinc-500">
      <i className="w-2 h-2 rounded-full bg-current animate-pulse" />
      <i className="w-2 h-2 rounded-full bg-current animate-pulse [animation-delay:120ms]" />
      <i className="w-2 h-2 rounded-full bg-current animate-pulse [animation-delay:240ms]" />
    </span>
  );
}

function parseRagAnswer(answer){
  const m = /\n\s*Fontes?:\s*(.*)$/is.exec(answer);
  if(!m) return { text: answer, sources: [] };
  const text = answer.replace(m[0], "").trim();
  const raw = m[1].replace(/[\.\s]+$/,'');
  const items = raw.split(/;|,|\|/).map(s=>s.trim()).filter(Boolean);
  return { text, sources: items };
}
