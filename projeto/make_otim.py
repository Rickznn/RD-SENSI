import json, os, shutil, re
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAME = "RD OTIMIZAÇÃO"

# ícone
S = 512
im = Image.new("RGB", (S, S), (11, 13, 18))
d = ImageDraw.Draw(im)
for y in range(S):
    t = y / S
    d.line([(0, y), (S, y)], fill=(int(30 + 20 * t), int(16 + 6 * t), int(10)))
d.rounded_rectangle([24, 24, S - 24, S - 24], radius=90, outline=(255, 122, 0), width=10)
bolt = [(290, 60), (150, 280), (245, 280), (205, 440), (360, 210), (262, 210), (300, 60)]
d.polygon(bolt, fill=(255, 190, 0))
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f1, f2 = ImageFont.truetype(F, 96), ImageFont.truetype(F, 52)
def ctext(y, txt, font, fill):
    w = d.textlength(txt, font=font); d.text(((S - w) / 2, y), txt, font=font, fill=fill, stroke_width=4, stroke_fill=(11, 13, 18))
ctext(250, "RD", f1, (255, 122, 0))
ctext(370, "OTIMIZAÇÃO", f2, (255, 200, 0))
im.save("icon-otim.png")

# HTML base (web/Android)
s = open("index.html").read()
rep = [
    ("<title>RD SENSI - Sensibilidade Free Fire</title>", "<title>RD OTIMIZAÇÃO - Otimização para Free Fire</title>"),
    ("<h1>🔥 RD SENSI</h1>", "<h1>⚡ RD OTIMIZAÇÃO</h1>"),
    ("<p>As melhores sensibilidades para Apple, Motorola, Samsung, Poco e Redmi</p>",
     "<p>Deixe seu celular e o Free Fire mais rápidos — Apple, Motorola, Samsung, Poco e Redmi</p>"),
    ("<body>", '<body class="t-otim">'),
    ('<div class="play only-sensi">', '<div class="play">'),
    ("<small>Copia sua sensi e abre o jogo direto pelo aplicativo</small>", "<small>Otimizou o celular? Abra o jogo direto pelo aplicativo</small>"),
    ("  await copyText();\n  if(isAndroid){", "  if(isAndroid){"),
    ('toast("✅ Sensi copiada! Abrindo o jogo...")', 'toast("🔥 Abrindo o jogo...")'),
    ('toast("✅ Sensi copiada! Toque em ABRIR na App Store")', 'toast("👉 Toque em ABRIR na App Store")'),
]
for a, b in rep:
    assert s.count(a) == 1, a; s = s.replace(a, b)
s, n = re.subn(r'\n  <div class="tabs" id="tabs">.*?</div>\n', "\n", s, flags=re.S); assert n == 1
os.makedirs("otim", exist_ok=True)
open("otim/index.html", "w").write(s)

# iPhone (Web App)
shutil.rmtree("otim-iphone", ignore_errors=True); os.makedirs("otim-iphone")
for n_, sz in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
    im.resize((sz, sz), Image.LANCZOS).save("otim-iphone/" + n_)
head = f'''<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{NAME}">
<meta name="theme-color" content="#0b0d12">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<link rel="manifest" href="manifest.json">'''
si = s
for a, b in [('<meta name="viewport" content="width=device-width, initial-scale=1.0">', head),
             ('min-height:100vh;padding:18px}', 'min-height:100vh;padding:18px;padding-top:max(18px,env(safe-area-inset-top));padding-bottom:max(18px,env(safe-area-inset-bottom))}')]:
    assert si.count(a) == 1, a; si = si.replace(a, b)
open("otim-iphone/index.html", "w").write(si)
json.dump({"name": NAME, "short_name": NAME, "start_url": "./", "display": "standalone",
           "background_color": "#0b0d12", "theme_color": "#0b0d12",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open("otim-iphone/manifest.json", "w"), ensure_ascii=False, indent=1)

# projeto Android
if not os.path.isdir("apk-otim"):
    shutil.copytree("apk", "apk-otim", ignore=shutil.ignore_patterns("build", "*.keystore", "assets"))
    os.makedirs("apk-otim/assets")
m = open("apk-otim/AndroidManifest.xml").read()
m = m.replace('android:label="RD SENSI"', f'android:label="{NAME}"').replace('android:versionCode="2" android:versionName="1.1"', 'android:versionCode="1" android:versionName="1.0"')
open("apk-otim/AndroidManifest.xml", "w").write(m)
for dn, sz in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]:
    im.resize((sz, sz), Image.LANCZOS).save(f"apk-otim/res/mipmap-{dn}/ic_launcher.png")
b = open("apk/build.sh").read()
for a, c in [("cp ../index.html assets/index.html", "cp ../otim/index.html assets/index.html"),
             ("-o build/unsigned.apk", "--rename-manifest-package com.rd.otimizacao -o build/unsigned.apk"),
             ("rdsensi.keystore", "rdotim.keystore"), ("-alias rdsensi", "-alias rdotim"),
             ('CN=RD SENSI, O=RD SENSI', 'CN=RD OTIMIZACAO, O=RD SENSI'), ("../RD-SENSI.apk", "../RD-OTIMIZACAO.apk")]:
    assert a in b, a; b = b.replace(a, c)
open("apk-otim/build.sh", "w").write(b); os.chmod("apk-otim/build.sh", 0o755)
print("ok")
