# Synthesizes the deck's per-slide narration (narration.json -> audio/*.wav + audio/index.json) with ../tts.py.

import json, subprocess, soundfile as sf, os
N=json.load(open('narration.json')); out=[]
for i,s in enumerate(N):
    f=f"audio/{i:02d}-{s['id']}.wav"
    subprocess.run(['python3',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','tts.py'),'--out',f], input=s['say'].encode(), check=True, env={**os.environ,'CX_KOKORO_DIR':os.environ.get('CX_KOKORO_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','kokoro'))})
    d,sr=sf.read(f); out.append({'id':s['id'],'file':f,'dur':round(len(d)/sr,2)}); print(i, s['id'], round(len(d)/sr,1))
json.dump(out, open('audio/index.json','w'), indent=1); print('total min', round(sum(o['dur'] for o in out)/60,1))
