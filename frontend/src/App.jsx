import { useMemo, useState } from 'react';
import { Link, Route, Routes } from 'react-router-dom';
import { translations } from './i18n/translations';

const pages = ['home', 'send', 'carry', 'search', 'calculator', 'auth', 'dashboard', 'payment', 'faq', 'contact', 'legal'];

const Form = ({ t }) => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const onSubmit = (e) => {
    e.preventDefault();
    if (!email || !email.includes('@')) return setMessage(t.formErrors.email);
    setMessage('✓');
  };
  return <form onSubmit={onSubmit} className="card"><input placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} /><button>{t.cta}</button><p>{message}</p></form>;
};

const Page = ({ title, t }) => <section className="page"><h1>{title}</h1><p>{t.pages.home}</p><Form t={t} /></section>;

export default function App() {
  const [lang, setLang] = useState('hy');
  const t = useMemo(() => translations[lang], [lang]);
  return (
    <div>
      <header>
        <img src="/tanem-logo.svg" alt="TANEM logo" className="logo" />
        <nav>{pages.slice(0,7).map((p, i)=><Link key={p} to={p==='home'?'/':'/'+p}>{t.nav[i]||p}</Link>)}</nav>
        <select value={lang} onChange={(e)=>setLang(e.target.value)}><option value="hy">Հայերեն</option><option value="ru">Русский</option><option value="en">English</option></select>
      </header>
      <main>
        <Routes>
          {pages.map((p)=><Route key={p} path={p==='home'?'/':'/'+p} element={<Page title={t.pages[p]} t={t} />} />)}
        </Routes>
      </main>
    </div>
  );
}
