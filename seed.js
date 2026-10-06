// Starter data. Everything here can be edited from /admin.
const P=(id,name,category,price,emoji,extra={})=>({id,name,category,price,emoji,image:'',desc:'Freshly baked in Swarup Nagar, Kanpur.',veg:true,bestseller:false,active:true,flavours:[],weights:[],...extra});
const W=(a)=>a.map(([label,price])=>({label,price}));
module.exports={
settings:{
  name:'Upper Crust',tagline:'Baking Kanpur happy since 1989',
  phone:'+91 00000 00000',whatsapp:'910000000000',
  address:'112/368-F, Swarup Nagar, Kanpur, Uttar Pradesh 208002',
  hours:'Open daily, 10 AM – 10 PM',freeDeliveryAbove:999,
  areas:['Swarup Nagar','Civil Lines','Kakadeo','Kidwai Nagar','Arya Nagar','Govind Nagar','Kalyanpur','Shyam Nagar'],
  announcement:'🎂 Free delivery on orders above ₹999 · Same day delivery in Kanpur'
},
categories:[
 {id:'cakes',name:'Cakes',emoji:'🎂',color:'#7a4a2b'},
 {id:'eggless',name:'Eggless & Vegan',emoji:'🌿',color:'#6b7f3a'},
 {id:'pastries',name:'Pastries',emoji:'🍰',color:'#b5481f'},
 {id:'savouries',name:'Savouries',emoji:'🥪',color:'#c8872c'},
 {id:'bakery',name:'Breads & Cookies',emoji:'🍪',color:'#a56a35'},
 {id:'custom',name:'Wedding & Custom',emoji:'💍',color:'#8a3b52'}
],
products:[
 P('p1','Eggless Black Forest Cake','eggless',1050,'🍒',{bestseller:true,weights:W([['500 g',1050],['1 kg',2000]]),flavours:['Black Forest']}),
 P('p2','Eggless Vegan Choco Mud Cake','eggless',1000,'🍫',{weights:W([['500 g',1000],['1 kg',1900]])}),
 P('p3','New Truffle Cake','cakes',1350,'🍫',{bestseller:true,weights:W([['500 g',1350],['1 kg',2600]]),flavours:['Dark Truffle','Belgian Truffle']}),
 P('p4','Celebration Kitkat Cake','cakes',1150,'🍬',{weights:W([['500 g',1150],['1 kg',2200]])}),
 P('p5','New Oreo Pinata Cake','cakes',1200,'🍪',{weights:W([['500 g',1200],['1 kg',2300]])}),
 P('p6','Sugar Free Chocolate Truffle Bento','cakes',780,'🍰',{weights:W([['Bento',780]])}),
 P('p7','Eggless Pineapple Grande','eggless',1000,'🍍',{weights:W([['500 g',1000],['1 kg',1900]])}),
 P('p8','Eggless Butter Scotch Pastry','pastries',90,'🍰'),
 P('p9','Truffle Slice Pastry','pastries',120,'🍫',{bestseller:true}),
 P('p10','Chocolate Boat','pastries',60,'🚤',{bestseller:true}),
 P('p11','Paneer Patty','savouries',45,'🥟'),
 P('p12','Grilled Veg Sandwich','savouries',90,'🥪'),
 P('p13','Marble Tea Cake','bakery',180,'🧁',{weights:W([['Small',180],['Big',390]])}),
 P('p14','Garlic Rusk','bakery',120,'🥖'),
 P('p15','Tiered Wedding Cake','custom',4500,'💒',{desc:'Custom designed. Book at least 3 days ahead.',weights:W([['2 tier · 3 kg',4500],['3 tier · 5 kg',7500]])})
],
offers:[
 {id:'o1',tag:'Welcome',badge:'10% OFF',title:'Get 10% off on orders over ₹999',code:'CRUST10',percent:10,min:999,max:150,active:true},
 {id:'o2',tag:'Flat',badge:'₹100 OFF',title:'Flat ₹100 off on orders above ₹1500',code:'FLAT100',flat:100,min:1500,max:100,active:true}
],
banners:[
 {id:'b1',title:'Tall-N-Fancy',subtitle:'Tastes just as great as it looks!',cta:'Order Now',link:'#/menu/cakes',emoji:'🎂',image:'',bg:'#f6dcc0',active:true},
 {id:'b2',title:'Eggless & Vegan',subtitle:'Guilt-free, flavour-full celebrations.',cta:'Explore',link:'#/menu/eggless',emoji:'🌿',image:'',bg:'#e3ead0',active:true}
],
occasions:[
 {id:'oc1',name:'Birthday',sub:'Celebrate Another Year',emoji:'🎈',image:'',link:'#/menu/cakes'},
 {id:'oc2',name:'Wedding',sub:'Crafted for your big day',emoji:'💍',image:'',link:'#/menu/custom'},
 {id:'oc3',name:'Anniversary',sub:'Cherish Every Moment',emoji:'💐',image:'',link:'#/menu/cakes'},
 {id:'oc4',name:'Snack Box',sub:'Party Time Favourites',emoji:'🥡',image:'',link:'#/menu/savouries'}
],
orders:[]
};
const IMG={p1:'black-forest',p2:'choco-mud',p3:'truffle',p4:'kitkat',p5:'oreo',p6:'bento',p7:'pineapple',p8:'butterscotch',p9:'truffle-slice',p10:'boat',p11:'patty',p12:'sandwich',p13:'teacake',p14:'rusk',p15:'wedding',p16:'cookies'};
const D=module.exports;
D.products.push(P('p16','Choco Chip Cookies','bakery',80,'🍪',{desc:'Crunchy, buttery, loaded with chocolate chips.'}));
D.products.forEach(p=>p.image=IMG[p.id]?'/img/'+IMG[p.id]+'.svg':'');
const CI={cakes:'cat-cakes',eggless:'cat-eggless',pastries:'cat-pastries',savouries:'sandwich',bakery:'cookies',custom:'wedding'};
D.categories.forEach(c=>c.image='/img/'+CI[c.id]+'.svg');
D.banners[0].image='/img/banner-fancy.svg';D.banners[1].image='/img/banner-eggless.svg';
['birthday','wedding','anniversary','snack'].forEach((n,i)=>D.occasions[i].image='/img/occ-'+n+'.svg');
D.settings.heroImage='/img/hero.svg';D.users=[];
