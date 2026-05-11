import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

const db = {
  users: [], parcels: [], routes: [], offers: [], messages: [], payments: [], reviews: [], deliveryStatuses: []
};

const add = (name) => app.post(`/api/${name}`, (req, res) => { const item = { id: Date.now(), ...req.body }; db[name].push(item); res.status(201).json(item); });
const list = (name) => app.get(`/api/${name}`, (_, res) => res.json(db[name]));

['users','parcels','routes','offers','messages','payments','reviews','deliveryStatuses'].forEach((name)=>{add(name);list(name);});

app.get('/api/health', (_,res)=>res.json({ok:true, service:'tanem-backend'}));

if (process.env.NODE_ENV !== 'test') {
  app.listen(4000, () => console.log('TANEM backend on 4000'));
}

export default app;
