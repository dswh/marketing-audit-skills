"""Build a portable annotated audit from unchanged PNG/JPEG screenshot files."""

import argparse
import base64
import hashlib
from html import escape as esc
import json
import math
from pathlib import Path
import struct
from urllib.parse import urlsplit


STYLE = '''
.va-report{font:16px/1.55 Arial,sans-serif;color:#20231e}.va-report *{box-sizing:border-box}.va-report h1{font:42px/1.15 Georgia,serif;margin:0 0 14px}.va-report h2{font-size:25px;line-height:1.25;margin:0}.va-report h3{font-size:18px;margin:0}.va-intro{max-width:850px;color:#535d4b}.va-screen{margin:32px 0 48px;break-inside:avoid}.va-top{display:flex;align-items:start;justify-content:space-between;gap:18px;margin-bottom:12px}.va-state{font-size:14px;margin:6px 0;color:#57624e}.va-toggle{border:1px solid #adb99d;background:white;color:#30471e;border-radius:6px;padding:9px 13px;font-weight:700;cursor:pointer;white-space:nowrap}.va-toggle:focus-visible{outline:3px solid #8aa85c;outline-offset:3px}.va-frame{border:1px solid #c5ceba;border-radius:10px;overflow:hidden;background:#20231e;box-shadow:0 5px 22px #1e2a1512}.va-scroll{overflow:auto}.va-canvas{display:block;width:100%;min-width:680px;height:auto}.va-meta{padding:11px 15px;background:#eef3e5;color:#3b4c2d;font-size:12px;display:flex;flex-wrap:wrap;gap:5px 18px;overflow-wrap:anywhere}.va-meta a{color:inherit}.va-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:18px;align-items:start}.va-card{background:#fff;border:1px solid #d2dac7;border-radius:8px;padding:18px}.va-card-head{display:flex;gap:10px;align-items:start;margin-bottom:12px}.va-number{background:#d7f6a0;border:1px solid #3b5126;color:#202b16;font-weight:700;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;flex:none}.va-status{font-size:12px;display:inline-block;padding:3px 8px;background:#edf0e8;color:#35422e;border-radius:4px;margin:7px 0 0}.va-card p{font-size:14px;margin:10px 0 0;line-height:1.55}.va-card strong{display:block;color:#3d4f2c;font-size:12px;margin-bottom:2px}.va-note{font-size:13px;color:#57624e}.va-key{font-size:12px;color:#57624e;margin-bottom:10px}.va-canvas .va-overlays[hidden]{display:none}@media(max-width:680px){.va-top{flex-direction:column;gap:9px}.va-cards{grid-template-columns:1fr}.va-report h1{font-size:32px}.va-report h2{font-size:23px}.va-canvas{min-width:680px}.va-meta{font-size:12px}}@media print{.va-toggle{display:none}.va-scroll{overflow:visible}.va-canvas{min-width:0!important}.va-cards{grid-template-columns:1fr 1fr}.va-card{break-inside:avoid}.va-screen{break-inside:auto}.va-overlays[hidden]{display:inline!important}.va-frame{box-shadow:none}}
'''

SCRIPT = '''document.addEventListener('click',function(event){const b=event.target.closest('.va-toggle');if(!b)return;const overlay=document.getElementById(b.getAttribute('aria-controls'));const hidden=b.getAttribute('aria-pressed')!=='true';overlay.toggleAttribute('hidden',hidden);b.setAttribute('aria-pressed',String(hidden));b.textContent=hidden?'Show annotations':'Show original';});'''


def image_info(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
        return (*struct.unpack('>II', data[16:24]), 'image/png')
    if data.startswith(b'\xff\xd8'):
        pos = 2
        while pos < len(data):
            if data[pos] != 255:
                raise ValueError('Invalid JPEG marker')
            while pos < len(data) and data[pos] == 255:
                pos += 1
            if pos >= len(data):
                break
            marker = data[pos]
            pos += 1
            if marker in {0xD8, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if marker in {0xD9, 0xDA} or pos + 2 > len(data):
                break
            length = struct.unpack('>H', data[pos:pos+2])[0]
            if length < 2 or pos + length > len(data):
                raise ValueError('Truncated JPEG segment')
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                height, width = struct.unpack('>HH', data[pos+3:pos+7])
                return width, height, 'image/jpeg'
            pos += length
    raise ValueError('Capture must be an actual PNG or JPEG with readable dimensions')


def required_text(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Missing text field: '+key)
    return value.strip()


def load_manifest(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text())
    required_text(data, 'title')
    required_text(data, 'business')
    if not isinstance(data.get('screens'), list) or not data['screens']:
        raise ValueError('At least one actual capture is required')
    screen_ids, finding_ids = set(), set()
    for screen in data['screens']:
        for key in ['id','file','title','url','captured_at','state']:
            required_text(screen,key)
        if screen['id'] in screen_ids:
            raise ValueError('Duplicate screen ID')
        screen_ids.add(screen['id'])
        if urlsplit(screen['url']).scheme not in {'http','https'}:
            raise ValueError('Source URL must use HTTP or HTTPS')
        image = (path.parent/screen['file']).resolve()
        if not image.is_relative_to(path.parent):
            raise ValueError('Capture must remain inside the manifest folder')
        raw = image.read_bytes()
        width,height,mime = image_info(raw)
        if not 0 < width <= 30000 or not 0 < height <= 30000:
            raise ValueError('Unsupported capture dimensions')
        viewport = screen.get('viewport',{})
        for key in ['width','height']:
            if not isinstance(viewport.get(key),(int,float)) or isinstance(viewport[key],bool) or not math.isfinite(viewport[key]) or viewport[key] <= 0:
                raise ValueError('Positive viewport dimensions are required')
        if not isinstance(screen.get('annotations'),list) or not screen['annotations']:
            raise ValueError('Each capture needs at least one supported annotation')
        for annotation in screen['annotations']:
            for key in ['id','title','status','observation','why','next_step','verify']:
                required_text(annotation,key)
            if annotation['id'] in finding_ids:
                raise ValueError('Use unique finding IDs')
            finding_ids.add(annotation['id'])
            if annotation['status'] not in {'Fix','Test','Need data'}:
                raise ValueError('Unsupported action classification')
            rect=annotation.get('rect')
            if not isinstance(rect,list) or len(rect)!=4 or any(not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x) for x in rect):
                raise ValueError('Rectangle must contain four finite pixel coordinates')
            x,y,w,h=rect
            if x<0 or y<0 or w<=0 or h<=0 or x+w>width or y+h>height:
                raise ValueError('Annotation rectangle falls outside the source image')
            badge=annotation.get('badge')
            if badge is not None and (not isinstance(badge,list) or len(badge)!=2 or any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) for v in badge) or not (0<=badge[0]<=width and 0<=badge[1]<=height)):
                raise ValueError('Badge must be a finite point inside the image')
        screen['_raw']=raw
        screen['_width'],screen['_height'],screen['_mime']=width,height,mime
        screen['_hash']=hashlib.sha256(raw).hexdigest()
    return data


def render_sections(data):
    content=[]
    number=0
    for index,screen in enumerate(data['screens'],1):
        width,height=screen['_width'],screen['_height']
        image='data:'+screen['_mime']+';base64,'+base64.b64encode(screen['_raw']).decode()
        markers,cards=[],[]
        radius=width*.019
        stroke=width*.0022
        for item in screen['annotations']:
            number+=1
            x,y,w,h=item['rect']
            bx,by=item.get('badge',[x-radius*1.4,y+min(h/2,radius)])
            cx=min(width-radius-3,max(radius+3,bx))
            cy=min(height-radius-3,max(radius+3,by))
            markers.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{stroke*2}" fill="none" stroke="white" stroke-width="{stroke*3}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{stroke*2}" fill="none" stroke="#304a20" stroke-width="{stroke}"/><circle cx="{cx}" cy="{cy}" r="{radius}" fill="#d7f6a0" stroke="#202b16" stroke-width="{stroke}"/><text x="{cx}" y="{cy}" dominant-baseline="central" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="{radius*1.12}" fill="#202b16">{number}</text>')
            fields=''.join('<p><strong>'+label+'</strong>'+esc(item[key])+'</p>' for label,key in [('What we see','observation'),('Why it may matter','why'),('Next step','next_step'),('What to check','verify')])
            cards.append('<article class="va-card" id="visual-'+esc(item['id'])+'"><div class="va-card-head"><span class="va-number">'+str(number)+'</span><div><h3>'+esc(item['title'])+'</h3><span class="va-status">'+esc(item['status'])+' | '+esc(item['id'])+'</span></div></div>'+fields+'</article>')
        overlay='visual-overlay-'+str(index)
        fig=f'<svg class="va-canvas" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="'+esc(screen['title'])+' with numbered audit findings"><image href="'+image+f'" width="{width}" height="{height}"/><g class="va-overlays" id="{overlay}">'+''.join(markers)+'</g></svg>'
        content.append('<section class="va-screen"><div class="va-top"><div><h2>'+esc(screen['title'])+'</h2><p class="va-state">'+esc(screen['state'])+'</p></div><button type="button" class="va-toggle" aria-controls="'+overlay+'" aria-pressed="false">Show original</button></div><p class="va-key">Numbers match the finding cards. On small screens, scroll the image to inspect the detail.</p><div class="va-frame"><div class="va-scroll">'+fig+'</div><div class="va-meta"><a href="'+esc(screen['url'],quote=True)+'">'+esc(screen['url'])+'</a><span>Captured '+esc(screen['captured_at'])+f'</span><span>Viewport {screen["viewport"]["width"]} x {screen["viewport"]["height"]}</span><span>Image {width} x {height}</span><span>SHA-256 '+screen['_hash'][:12]+'</span></div></div><div class="va-cards">'+''.join(cards)+'</div></section>')
    for index,section in enumerate(content,1):
        content[index-1]=section.replace('<section class="va-screen">',f'<section class="va-screen" id="visual-screen-{index}">',1)
    return '<div class="va-report">'+''.join(content)+'</div>'


def render_document(data):
    body='<main class="va-report"><h1>'+esc(data['title'])+'</h1><p class="va-intro">'+esc(data['business'])+'. Actual captures, numbered observations and proposed next steps. Business impact remains unmeasured unless supporting data is supplied.</p>'+render_sections(data)+'</main>'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(data['title'])+'</title><style>body{max-width:1180px;margin:36px auto;padding:0 22px;background:#f6f6f0}'+STYLE+'</style></head><body>'+body+'<script>'+SCRIPT+'</script></body></html>'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    data=load_manifest(args.input)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(render_document(data))
    print(args.output)


if __name__=='__main__':
    main()
