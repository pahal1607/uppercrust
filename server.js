const express=require('express'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const app=express(),PORT=process.env.PORT||3000,PASS=process.env.ADMIN_PASSWORD||'admin123';
const STORAGE=path.join(__dirname,'data');
const DB=path.join(STORAGE,'db.json');
const UP=path.join(STORAGE,'uploads');
fs.mkdirSync(UP,{recursive:true});
if(!fs.existsSync(DB))fs.writeFileSync(DB,JSON.stringify(require('./seed.js'),null,2));
const load=()=>JSON.parse(fs.readFileSync(DB,'utf8')),save=d=>fs.writeFileSync(DB,JSON.stringify(d,null,2));
const uid=()=>crypto.randomBytes(5).toString('hex');
app.use(express.json({limit:'12mb'}));
app.use('/uploads',express.static(UP));
app.use(express.static(path.join(__dirname,'public')));
app.get('/admin',(q,r)=>r.sendFile(path.join(__dirname,'public','admin.html')));

const tokens=new Set();
const auth=(q,r,n)=>tokens.has((q.headers.authorization||'').replace('Bearer ',''))?n():r.status(401).json({error:'Please log in again'});

// ---- public ----
const SK=path.join(__dirname,'data','secret.key');
if(!fs.existsSync(SK))fs.writeFileSync(SK,crypto.randomBytes(32).toString('hex'));
const SECRET=process.env.SECRET||fs.readFileSync(SK,'utf8');
const sign=ph=>ph+'.'+crypto.createHmac('sha256',SECRET).update(ph).digest('hex');
const who=q=>{const t=String(q.headers['x-user-token']||''),[ph,sg]=t.split('.');return ph&&sg&&sign(ph)===t?ph:''};
const ph10=p=>String(p||'').replace(/\D/g,'').slice(-10);
const hash=(p,s)=>crypto.scryptSync(String(p),s,32).toString('hex');
app.get('/api/data',(q,r)=>{const d=load();delete d.orders;delete d.users;r.json(d)});
app.post('/api/register',(q,r)=>{const d=load(),b=q.body||{},ph=ph10(b.phone);d.users=d.users||[];
  if(!b.name||ph.length!==10||String(b.password||'').length<6)return r.status(400).json({error:'Enter name, 10-digit phone and a password of 6+ characters'});
  if(d.users.find(u=>u.phone===ph))return r.status(409).json({error:'This number is already registered — please log in'});
  const salt=uid();d.users.push({name:String(b.name).slice(0,40),phone:ph,salt,hash:hash(b.password,salt)});save(d);r.json({token:sign(ph),name:b.name,phone:ph})});
app.post('/api/user-login',(q,r)=>{const d=load(),ph=ph10(q.body.phone),u=(d.users||[]).find(x=>x.phone===ph);
  if(!u||hash(q.body.password,u.salt)!==u.hash)return r.status(401).json({error:'Wrong phone number or password'});r.json({token:sign(ph),name:u.name,phone:ph})});
app.get('/api/me',(q,r)=>{const ph=who(q),u=ph&&(load().users||[]).find(x=>x.phone===ph);u?r.json({name:u.name,phone:u.phone}):r.sendStatus(401)});
app.get('/api/my-orders',(q,r)=>{const ph=who(q);if(!ph)return r.sendStatus(401);r.json(load().orders.filter(o=>o.userPhone===ph).map(({id,createdAt,status,items,total})=>({id,createdAt,status,items,total})))});
app.post('/api/orders',(q,r)=>{
  const d=load(),b=q.body||{};
  if(!b.name||!/^\d{10}$/.test(String(b.phone||'').replace(/\D/g,'').slice(-10))||!b.address||!Array.isArray(b.items)||!b.items.length)
    return r.status(400).json({error:'Please fill name, 10-digit phone, address and cart'});
  let sub=0;const items=[];
  for(const i of b.items){
    const p=d.products.find(x=>x.id===i.id&&x.active!==false);if(!p)continue;
    const w=(p.weights||[]).find(x=>x.label===i.weight);const price=w?w.price:p.price,qty=Math.max(1,Math.min(50,+i.qty||1));
    sub+=price*qty;items.push({id:p.id,name:p.name,price,qty,weight:i.weight||'',flavour:i.flavour||'',message:String(i.message||'').slice(0,30)});
  }
  if(!items.length)return r.status(400).json({error:'Cart is empty'});
  let discount=0;const o=d.offers.find(x=>x.active&&b.code&&x.code.toLowerCase()===String(b.code).toLowerCase());
  if(o&&sub>=o.min){discount=o.percent?Math.round(sub*o.percent/100):o.flat;if(o.max)discount=Math.min(discount,o.max)}
  const delivery=sub>=d.settings.freeDeliveryAbove?0:50,total=sub-discount+delivery;
  const order={id:'UC'+Date.now().toString().slice(-6),createdAt:new Date().toISOString(),status:'New',userPhone:who(q),name:b.name,phone:b.phone,address:b.address,area:b.area||'',date:b.date||'',slot:b.slot||'',note:String(b.note||'').slice(0,200),items,sub,discount,delivery,total,code:discount?o.code:''};
  d.orders.unshift(order);save(d);r.json(order);
});
app.post('/api/validate-code',(q,r)=>{
  const d=load(),o=d.offers.find(x=>x.active&&x.code.toLowerCase()===String(q.body.code||'').toLowerCase());
  if(!o)return r.status(404).json({error:'Invalid code'});
  if(q.body.sub<o.min)return r.status(400).json({error:`Minimum order ${o.min}`});
  let v=o.percent?Math.round(q.body.sub*o.percent/100):o.flat;if(o.max)v=Math.min(v,o.max);r.json({discount:v});
});

// ---- admin ----
app.post('/api/login',(q,r)=>{
  if(q.body.password!==PASS)return r.status(401).json({error:'Wrong password'});
  const t=crypto.randomBytes(24).toString('hex');tokens.add(t);r.json({token:t});
});
app.get('/api/admin/orders',auth,(q,r)=>r.json(load().orders));
app.patch('/api/admin/orders/:id',auth,(q,r)=>{const d=load(),o=d.orders.find(x=>x.id===q.params.id);if(!o)return r.sendStatus(404);o.status=q.body.status;save(d);r.json(o)});
app.delete('/api/admin/orders/:id',auth,(q,r)=>{const d=load();d.orders=d.orders.filter(x=>x.id!==q.params.id);save(d);r.json({ok:1})});
app.put('/api/admin/settings',auth,(q,r)=>{const d=load();d.settings={...d.settings,...q.body};save(d);r.json(d.settings)});
app.post('/api/admin/upload',auth,(q,r)=>{
  const m=/^data:image\/(png|jpe?g|webp|gif);base64,(.+)$/.exec(q.body.data||'');
  if(!m)return r.status(400).json({error:'Only png/jpg/webp/gif images'});
  const f=uid()+'.'+m[1].replace('jpeg','jpg');fs.writeFileSync(path.join(UP,f),Buffer.from(m[2],'base64'));r.json({url:'/uploads/'+f});
});
const COLS=['products','categories','offers','banners','occasions'];
app.post('/api/admin/:c',auth,(q,r)=>{if(!COLS.includes(q.params.c))return r.sendStatus(404);const d=load(),it={...q.body,id:uid()};d[q.params.c].push(it);save(d);r.json(it)});
app.put('/api/admin/:c/:id',auth,(q,r)=>{if(!COLS.includes(q.params.c))return r.sendStatus(404);const d=load(),a=d[q.params.c],i=a.findIndex(x=>x.id===q.params.id);if(i<0)return r.sendStatus(404);a[i]={...q.body,id:a[i].id};save(d);r.json(a[i])});
app.delete('/api/admin/:c/:id',auth,(q,r)=>{if(!COLS.includes(q.params.c))return r.sendStatus(404);const d=load();d[q.params.c]=d[q.params.c].filter(x=>x.id!==q.params.id);save(d);r.json({ok:1})});

app.listen(PORT,'0.0.0.0',()=>console.log(`Upper Crust running on port ${PORT}`));
