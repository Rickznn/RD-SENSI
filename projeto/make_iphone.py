import json, os
from PIL import Image
os.makedirs('iphone', exist_ok=True)
im = Image.open('icon.png').convert('RGBA')
bg = Image.new('RGB', im.size, (255, 140, 0)); bg.paste(im, (0, 0), im)
for n, sz in [('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)]:
    bg.resize((sz, sz), Image.LANCZOS).save('iphone/' + n)
s = open('index.html').read()
head = '''<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="RD SENSI">
<meta name="theme-color" content="#0b0d12">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<link rel="manifest" href="manifest.json">'''
for a, b in [('<meta name="viewport" content="width=device-width, initial-scale=1.0">', head),
             ('min-height:100vh;padding:18px}', 'min-height:100vh;padding:18px;padding-top:max(18px,env(safe-area-inset-top));padding-bottom:max(18px,env(safe-area-inset-bottom))}')]:
    assert s.count(a) == 1, a; s = s.replace(a, b)
open('iphone/index.html', 'w').write(s)
json.dump({"name": "RD SENSI", "short_name": "RD SENSI", "start_url": "./", "display": "standalone",
           "background_color": "#0b0d12", "theme_color": "#0b0d12",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open('iphone/manifest.json', 'w'), ensure_ascii=False, indent=1)
