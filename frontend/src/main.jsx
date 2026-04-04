import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';

const API = 'http://localhost:8000';

function App() {
  const [token, setToken] = useState('');
  const [projectId, setProjectId] = useState(null);
  const [brand, setBrand] = useState('');
  const [results, setResults] = useState([]);

  const register = async () => {
    const r = await fetch(`${API}/auth/register`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email:'user@depozio.fr', password:'StrongPass123!'})});
    const j = await r.json(); setToken(j.access_token);
  };

  const step1 = async () => {
    const r = await fetch(`${API}/brandcraft/step1`, {method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify({brand_name: brand, activity_description:'software finance'})});
    const j = await r.json(); setProjectId(j.project_id);
  };

  const search = async () => {
    await fetch(`${API}/brandcraft/step2/${projectId}`, {method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify({territory:'EU'})});
    const s = await fetch(`${API}/brandcraft/step3/suggest/${projectId}`, {headers:{'Authorization':`Bearer ${token}`}});
    const sj = await s.json();
    await fetch(`${API}/brandcraft/step3/${projectId}`, {method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify({nice_classes:sj.suggested})});
    await fetch(`${API}/brandcraft/step4/search`, {method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify({project_id:projectId})});
    const r = await fetch(`${API}/brandcraft/step5/results/${projectId}`, {headers:{'Authorization':`Bearer ${token}`}});
    const j = await r.json(); setResults(j.results);
  };

  return <div style={{fontFamily:'sans-serif',padding:20,background:'#1A1A2E',color:'white',minHeight:'100vh'}}>
    <h1 style={{color:'#FF5C1A'}}>DEPOZIO</h1>
    <input placeholder='Brand name' value={brand} onChange={e=>setBrand(e.target.value)} />
    <div><button onClick={register}>Auth</button><button onClick={step1}>Step1</button><button onClick={search}>Run Wizard</button></div>
    <ul>{results.map((r,i)=><li key={i}>{r.candidate_name} - {r.score} - {r.risk_level}</li>)}</ul>
  </div>
}

createRoot(document.getElementById('root')).render(<App />);
