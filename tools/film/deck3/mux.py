import json, subprocess, soundfile as sf, numpy as np, glob, os, sys
FF=subprocess.run(['python3','-c','import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())'],capture_output=True,text=True).stdout.strip()
idx=json.load(open('audio/index.json')); M=json.load(open('out/marks.json'))
webm=glob.glob('out/*.webm')[0]
sr=24000; total=0
# Recording starts before the first slide is shown; CX_OFFSET is the lead measured by ffmpeg scene detection (first slide change pts minus its mark).
OFF=float(os.environ.get('CX_OFFSET','0'))
clips=[]
for s,m in zip(idx,M['marks']):
    d,r=sf.read(s['file']); 
    if d.ndim>1: d=d.mean(1)
    if r!=sr:
        import math; d=np.interp(np.linspace(0,len(d),int(len(d)*sr/r),endpoint=False),np.arange(len(d)),d)
    clips.append((m['at']+OFF,d.astype(np.float32)))
end=max(a+len(d)/sr for a,d in clips)+1.0
track=np.zeros(int(end*sr),dtype=np.float32)
for a,d in clips:
    o=int(a*sr); track[o:o+len(d)]+=d
sf.write('out/track.wav',track,sr)
out=sys.argv[1] if len(sys.argv)>1 else 'out/agi-future-foundation-investor-pitch.mp4'
subprocess.run([FF,'-y','-i',webm,'-i','out/track.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','24','-pix_fmt','yuv420p','-r','30','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],check=True)
print('wrote',out, os.path.getsize(out)//1048576,'MiB')
