# Generates illustrated placeholder images into public/img  (run: python3 make_art.py)
import random,os
OUT='public/img';os.makedirs(OUT,exist_ok=True)
N=[0]
def uid():
    N[0]+=1;return f'g{N[0]}'
def lin(i,a,b):return f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
def shade(h,f):
    h=h.lstrip('#');h=''.join(c*2 for c in h) if len(h)==3 else h;r,g,b=[int(h[i:i+2],16) for i in(0,2,4)]
    return '#%02x%02x%02x'%tuple(max(0,min(255,int(c*f))) for c in(r,g,b))
def top_items(kind,rnd,cx,ty):
    s=''
    if kind=='cherry':
        for dx in(-70,-20,35,85):
            x=cx+dx;y=ty-6+rnd.randint(-8,8);s+=f'<path d="M{x} {y-14} q12 -34 30 -38" stroke="#3b7a2a" stroke-width="3" fill="none"/><circle cx="{x}" cy="{y}" r="17" fill="#c2182b"/><circle cx="{x-6}" cy="{y-6}" r="5" fill="#fff" opacity=".55"/>'
    if kind=='berry':
        for dx in(-80,-30,25,75):
            x=cx+dx;y=ty-4;s+=f'<path d="M{x-18} {y-12} Q{x} {y-24} {x+18} {y-12} Q{x+14} {y+24} {x} {y+30} Q{x-14} {y+24} {x-18} {y-12}Z" fill="#e0314b"/><path d="M{x-10} {y-14} l10 -8 l10 8Z" fill="#3d9a3a"/>'+''.join(f'<circle cx="{x+a}" cy="{y+b}" r="1.8" fill="#ffd9a0"/>' for a,b in((-6,-2),(5,2),(-2,10),(6,12),(-8,12)))
    if kind=='oreo':
        for dx in(-80,-25,30,80):
            x=cx+dx;y=ty-8;s+=f'<ellipse cx="{x}" cy="{y}" rx="26" ry="12" fill="#2a1a14"/><ellipse cx="{x}" cy="{y-3}" rx="22" ry="8" fill="#3d2820"/><path d="M{x-14} {y-3} h28" stroke="#f3e9dd" stroke-width="3"/>'
    if kind=='kitkat':
        for k in range(8):
            x=cx-105+k*30;s+=f'<rect x="{x}" y="{ty+4}" width="22" height="110" rx="3" fill="#b3202a"/><rect x="{x+3}" y="{ty+10}" width="16" height="98" rx="2" fill="#7a3b1d" opacity=".55"/>'
    if kind=='shard':
        for i,dx in enumerate((-80,-40,0,40,80)):
            s+=f'<rect x="{cx+dx-8}" y="{ty-52+abs(dx)//8}" width="16" height="58" rx="3" fill="#4a2616" transform="rotate({(i-2)*14} {cx+dx} {ty})"/>'
    if kind=='pine':
        for dx in(-70,0,70):
            x=cx+dx;s+=f'<circle cx="{x}" cy="{ty-6}" r="26" fill="#ffd54a"/><circle cx="{x}" cy="{ty-6}" r="9" fill="#fff3c4"/><circle cx="{x}" cy="{ty-6}" r="26" fill="none" stroke="#e8a914" stroke-width="3"/>'
    if kind=='rose':
        for dx,dy in((-80,0),(-30,-12),(30,-12),(80,0),(0,10)):
            x=cx+dx;y=ty+dy;s+=f'<circle cx="{x}" cy="{y}" r="22" fill="#f4a8c0"/><circle cx="{x}" cy="{y}" r="14" fill="#f78fb0"/><circle cx="{x}" cy="{y}" r="6" fill="#e0527f"/>'
    if kind=='sprinkle':
        for _ in range(34):
            x=cx+rnd.randint(-120,120);y=ty+rnd.randint(-14,16);s+=f'<rect x="{x}" y="{y}" width="12" height="4" rx="2" fill="{rnd.choice(["#ff5d8f","#ffd23f","#3bceac","#5b8def","#fff"])}" transform="rotate({rnd.randint(0,180)} {x} {y})"/>'
    if kind=='swirl':
        for dx in(-95,-48,0,48,95):
            x=cx+dx;s+=f'<path d="M{x-18} {ty+6} q18 -50 36 0Z" fill="#fff4e2"/><path d="M{x-12} {ty-4} q12 -26 24 0" stroke="#e8cfae" stroke-width="3" fill="none"/>'
    return s
def cake(base,cream,drip,top,x=0,y=0,sc=1,seed=1,tiers=1,layers=2):
    rnd=random.Random(seed);i=uid();s=f'<g transform="translate({x} {y}) scale({sc})"><defs>{lin(i+"a",shade(base,1.15),shade(base,.78))}{lin(i+"b",shade(cream,1.05),shade(cream,.85))}{lin(i+"p","#ffffff","#e4d6c6")}</defs>'
    s+=f'<ellipse cx="300" cy="470" rx="235" ry="46" fill="#000" opacity=".12"/><ellipse cx="300" cy="458" rx="230" ry="42" fill="url(#{i}p)"/><ellipse cx="300" cy="452" rx="196" ry="33" fill="#fff" opacity=".7"/>'
    def tier(cx,w,bot,h):
        l,r=cx-w//2,cx+w//2;t=bot-h;o=f'<path d="M{l} {t} v{h} a{w//2} {w//9} 0 0 0 {w} 0 v-{h}Z" fill="url(#{i}a)"/>'
        for k in range(1,layers+1):
            yy=t+h*k/(layers+1);o+=f'<path d="M{l} {yy:.0f} q{w//2} {w//9*2} {w} 0 v9 q-{w//2} {w//9*2} -{w} 0Z" fill="url(#{i}b)"/>'
        o+=f'<ellipse cx="{cx}" cy="{t}" rx="{w//2}" ry="{w//9}" fill="{cream}"/><ellipse cx="{cx}" cy="{t}" rx="{w//2-8}" ry="{w//9-4}" fill="{shade(cream,1.06)}"/>'
        d=f'M{l} {t} '
        for k in range(0,w,38):
            ln=rnd.randint(18,52);d+=f'h{14} q10 0 10 10 v{ln} q0 12 -12 0 v-{ln} q0 -10 10 -10 '
        o+=f'<path d="M{l+2} {t+2} '+''.join(f'q{9} 0 {9} 12 v{rnd.randint(14,48)} q0 12 -{13} 0 v-{rnd.randint(2,10)} q0 -12 {19} -12 ' for _ in range(w//46))+f'H{r-2} v-2Z" fill="{drip}" opacity="0"/>'
        # drips as simple rounded rects hanging from rim
        for k in range(0,w-30,34):
            ln=rnd.randint(16,50);o+=f'<rect x="{l+10+k}" y="{t+3}" width="18" height="{ln}" rx="9" fill="{drip}"/>'
        o+=f'<ellipse cx="{cx}" cy="{t+2}" rx="{w//2-6}" ry="{w//9-3}" fill="{drip}"/>'
        return o,t
    if tiers==1:
        b,t=tier(300,300,430,150);s+=b;s+=top_items(top,rnd,300,t)
    else:
        sizes=[(330,430,110),(240,320,100),(150,220,90)][:tiers]
        for w,bot,h in sizes:
            b,t=tier(300,w,bot,h);s+=b
        s+=top_items(top,rnd,300,t)
    return s+'</g>'
def svg(body,w=600,h=600,bg=('#fff3e4','#f6cfa4')):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><radialGradient id="bg" cx=".5" cy=".4" r=".8"><stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></radialGradient></defs><rect width="{w}" height="{h}" fill="url(#bg)"/>'+''.join(f'<circle cx="{(k*97)%w}" cy="{(k*53)%h}" r="{6+k%4*3}" fill="#fff" opacity=".18"/>' for k in range(1,14))+body+'</svg>'
def plate():return '<ellipse cx="300" cy="470" rx="235" ry="46" fill="#000" opacity=".12"/><ellipse cx="300" cy="455" rx="230" ry="42" fill="#fff"/><ellipse cx="300" cy="452" rx="190" ry="30" fill="#f1e6da"/>'
def slice_(a,cream,top,seed=1):
    i=uid();s=plate()+f'<defs>{lin(i,shade(a,1.1),shade(a,.8))}</defs><g transform="translate(300 330)"><path d="M-150 80 L150 80 L150 -10 L-150 -10Z" fill="url(#{i})"/>'
    for k,y in enumerate((18,50)):s+=f'<rect x="-150" y="{y}" width="300" height="12" fill="{cream}"/>'
    s+=f'<path d="M-150 -10 L150 -10 L110 -50 L-110 -50Z" fill="{cream}"/><path d="M-110 -50 L110 -50 L90 -64 L-90 -64Z" fill="{shade(cream,1.08)}"/><path d="M-150 80 L150 80 L150 94 L-150 94Z" fill="{shade(a,.6)}"/>'
    s+=top_items(top,random.Random(seed),0,-62).replace('rx="26"','rx="20"')+'</g>';return svg(s)
def boat():
    return svg(plate()+'<g transform="translate(300 380)"><path d="M-170 -30 Q0 40 170 -30 L130 60 Q0 100 -130 60Z" fill="#5a2e1b"/><path d="M-160 -30 Q0 30 160 -30 Q0 -60 -160 -30Z" fill="#fff4e2"/><path d="M-130 -34 q30 -34 60 0 q30 -34 60 0 q30 -34 60 0 q30 -34 60 0" stroke="#f0d9b8" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="-60" cy="-52" r="12" fill="#c2182b"/><circle cx="50" cy="-52" r="12" fill="#c2182b"/></g>')
def patty():
    s=plate()+'<g transform="translate(300 400)"><path d="M-160 20 Q-160 -110 0 -110 Q160 -110 160 20 Z" fill="#d99a3e"/><path d="M-160 20 Q-160 -110 0 -110 Q160 -110 160 20 Z" fill="none" stroke="#b9772a" stroke-width="8"/>'
    for k in range(-5,6):s+=f'<path d="M{k*26} -100 q-6 60 0 118" stroke="#f1c274" stroke-width="5" fill="none" opacity=".8"/>'
    return svg(s+'<path d="M-170 28 h340" stroke="#a86a20" stroke-width="14" stroke-linecap="round"/></g>')
def sandwich():
    s=plate()+'<g transform="translate(300 390)"><path d="M-150 40 L0 -110 L150 40Z" fill="#e8c27d"/><path d="M-130 30 L0 -100 L130 30Z" fill="#f6e0b0"/><path d="M-110 20 L0 -90 L110 20Z" fill="#58a03a"/><path d="M-90 20 L0 -70 L90 20Z" fill="#e0443a"/><path d="M-70 20 L0 -50 L70 20Z" fill="#ffd54a"/><path d="M-50 20 L0 -30 L50 20Z" fill="#f6e0b0"/><path d="M-150 40 L150 40 L150 62 L-150 62Z" fill="#c99a52"/></g>'
    return svg(s)
def teacake():
    return svg(plate()+'<g transform="translate(300 380)"><rect x="-170" y="-60" width="340" height="120" rx="30" fill="#c98a4b"/><rect x="-170" y="-60" width="340" height="50" rx="30" fill="#e0a867"/><path d="M-130 -30 q40 -40 80 0 t80 0 t80 0" stroke="#5a2e1b" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-130 20 q40 -30 80 0 t80 0 t80 0" stroke="#5a2e1b" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/></g>',bg=('#fff3e4','#eec79a'))
def cookies():
    s=plate()
    for x,y in((230,420),(370,420),(300,360)):
        s+=f'<circle cx="{x}" cy="{y}" r="62" fill="#d99a52"/><circle cx="{x}" cy="{y}" r="62" fill="none" stroke="#b97730" stroke-width="5"/>'+''.join(f'<circle cx="{x+a}" cy="{y+b}" r="9" fill="#4a2616"/>' for a,b in((-25,-15),(20,-25),(-8,20),(28,12),(-35,18)))
    return svg(s)
def rusk():
    s=plate()
    for k in range(5):s+=f'<rect x="{150+k*62}" y="{360-k%2*18}" width="52" height="108" rx="14" fill="#d6924a" transform="rotate({(k-2)*6} {176+k*62} 410)"/><rect x="{158+k*62}" y="{368-k%2*18}" width="36" height="12" rx="6" fill="#f0c27d" transform="rotate({(k-2)*6} {176+k*62} 410)"/>'
    return svg(s)
def balloons():
    s=''
    for x,y,c in((170,230,'#ff5d8f'),(300,170,'#ffd23f'),(430,240,'#5b8def'),(235,330,'#3bceac'),(370,330,'#b36cf0')):
        s+=f'<path d="M{x} {y+60} q-4 90 8 160" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/><ellipse cx="{x}" cy="{y}" rx="52" ry="62" fill="{c}"/><ellipse cx="{x-16}" cy="{y-22}" rx="12" ry="20" fill="#fff" opacity=".4"/><path d="M{x-8} {y+62} h16 l-8 12Z" fill="{c}"/>'
    return svg(s+cake('#5a2e1b','#fff4e2','#3a1d10','sprinkle',150,300,.5),bg=('#ffe3ee','#f5a9c8'))
def rings():
    return svg('<g fill="none" stroke-width="16"><circle cx="250" cy="330" r="95" stroke="#e8b84a"/><circle cx="350" cy="330" r="95" stroke="#f3d27a"/></g><path d="M300 170 l32 46 -32 46 -32 -46Z" fill="#dff4ff" stroke="#8fd0f0" stroke-width="5"/>'+cake('#fff4e2','#fff','#f4a8c0','rose',150,330,.5,tiers=3),bg=('#f9e6f0','#d6a3c2'))
def flowers():
    s=''
    for x,y,c in((170,300,'#f78fb0'),(300,230,'#ffd23f'),(430,300,'#b36cf0'),(240,390,'#ff7a59'),(370,390,'#f4a8c0')):
        s+=''.join(f'<ellipse cx="{x}" cy="{y-34}" rx="18" ry="34" fill="{c}" transform="rotate({a} {x} {y})"/>' for a in range(0,360,60))+f'<circle cx="{x}" cy="{y}" r="16" fill="#fff3c4"/>'
    return svg(s,bg=('#efe3ff','#c9a8ec'))
def snack():
    return svg('<rect x="140" y="260" width="320" height="200" rx="16" fill="#c98a4b"/><rect x="140" y="260" width="320" height="50" rx="16" fill="#e0a867"/><rect x="270" y="260" width="60" height="200" fill="#b5481f" opacity=".85"/>'+'<g transform="translate(300 250) scale(.4) translate(-300 -300)">'+patty().split('</defs>')[-1][:0]+'</g><circle cx="220" cy="240" r="40" fill="#d99a52"/><circle cx="300" cy="215" r="44" fill="#e8c27d"/><circle cx="385" cy="240" r="38" fill="#d6924a"/>',bg=('#fff0d6','#f2c27d'))
def tiered_wedding():return svg(cake('#fff8ef','#ffffff','#f4a8c0','rose',tiers=3,layers=1),bg=('#fdeef4','#efc1d6'))
def hero():return svg(cake('#4a2616','#fff1dc','#2e160c','cherry',seed=3),bg=('#fff3e4','#f0b17a'))
P={ # filename: svg
 'black-forest':svg(cake('#4a2616','#fff6ea','#2e160c','cherry',seed=2)),
 'choco-mud':svg(cake('#5a2e1b','#6b3a24','#2e160c','shard',seed=4),bg=('#f6e3d3','#d9a27a')),
 'truffle':svg(cake('#3a1d10','#5a2e1b','#1f0f08','shard',seed=5),bg=('#f4e2d6','#cf9a78')),
 'kitkat':svg(cake('#7a3b1d','#f3dcc0','#4a2616','kitkat',seed=6),bg=('#ffe9e4','#ef9f92')),
 'oreo':svg(cake('#6b6b73','#f6f1ea','#2a1a14','oreo',seed=7),bg=('#eef0f6','#b9bfd4')),
 'bento':svg(cake('#4a2616','#6b3a24','#2a1a14','berry',x=90,y=70,sc=.7,seed=8),bg=('#f9e6ee','#e9a3be')),
 'pineapple':svg(cake('#ffe9a8','#fff8dc','#ffd54a','pine',seed=9),bg=('#fff9d8','#f5d36a')),
 'butterscotch':slice_('#e8b867','#fff1c9','sprinkle'),
 'truffle-slice':slice_('#4a2616','#7a4a2b','shard'),
 'boat':boat(),'patty':patty(),'sandwich':sandwich(),'teacake':teacake(),'rusk':rusk(),'cookies':cookies(),
 'wedding':tiered_wedding(),'hero':hero(),'occ-birthday':balloons(),'occ-wedding':rings(),'occ-anniversary':flowers(),'occ-snack':snack(),
 'cat-cakes':svg(cake('#7a4a2b','#fff4e2','#4a2616','swirl',seed=11)),
 'cat-eggless':svg(cake('#e8f0c8','#fff','#9fb85a','berry',seed=12),bg=('#eef6d8','#b9d27a')),
 'cat-pastries':slice_('#b5481f','#fff1dc','berry'),
}
def banner(cakes,bg,pod,sc=.7):
    b=''
    for cx,c in cakes:
        pt=sc*455-70+10
        b+=f'<rect x="{cx-135}" y="{pt}" width="270" height="260" fill="{pod}"/><ellipse cx="{cx}" cy="{pt}" rx="135" ry="26" fill="{shade(pod,1.25)}"/>'+c.replace('<g transform="translate(0 0) scale(1)">',f'<g transform="translate({cx-300*sc} -70) scale({sc})">',1)
    return svg(b,900,520,bg)
c1=cake('#fff4e2','#fff','#f4a8c0','swirl',seed=21);c2=cake('#4a2616','#6b3a24','#2e160c','shard',seed=22);c3=cake('#fff1c9','#fff','#e8a914','pine',seed=23)
P['banner-fancy']=banner([(150,c1),(450,c2),(750,c3)],('#f6dcc0','#e8a76e'),'#7a2d1a')
P['banner-eggless']=banner([(250,cake('#e8f0c8','#fff','#9fb85a','berry',seed=31)),(650,cake('#ffe9a8','#fff8dc','#ffd54a','pine',seed=32))],('#e3ead0','#a9c06a'),'#4a6a2a')
for k,v in P.items():open(f'{OUT}/{k}.svg','w').write(v)
print(len(P),'images written')
