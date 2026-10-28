# Run inside the user's Blender (execute_blender_code). Starts a SAFE frame-by-frame render that returns
# immediately (runs on a Blender timer). Set EP_DIR and END before exec.
# GPU protection (Intel UHD, laptop): 1280x720, EEVEE 24 samples, NO raytracing, NO world/volume fog
# (fog = TuckFog shader group on every material), 1 s rest per frame, 30 s rest every 150 frames,
# auto-STOP if a frame comes out empty. Status is written to <EP_DIR>/render_status.json.
import bpy,os,time,json
def _w(S):
    with open(os.path.join(os.path.dirname(S['dir']),'render_status.json'),'w') as fh: json.dump(S,fh)
def tuck_render_step():
    S=bpy.app.driver_namespace['TUCK_RENDER']
    if S.get('stop'): S['state']='stopped'; _w(S); return None
    sc=bpy.context.scene; f=S['f']
    if f>S['end']: S['state']='done'; _w(S); return None
    p=os.path.join(S['dir'],'f%05d.png'%f)
    if os.path.exists(p): S['f']=f+1; return 0.01
    sc.frame_set(f); sc.render.filepath=p
    t=time.time(); bpy.ops.render.render(write_still=True); dt=time.time()-t
    ok=os.path.exists(p) and os.path.getsize(p)>20000
    if ok:
        img=bpy.data.images.load(p,check_existing=False); px=img.pixels[:40000]; bpy.data.images.remove(img); ok=sum(px)>1.0
    if not ok:
        if os.path.exists(p): os.remove(p)
        S['state']='FAILED at %d (empty frame, GPU protection stop)'%f; _w(S); return None
    S['f']=f+1; S['last']=round(dt,2); S['state']='rendering'; S['t']=time.strftime('%H:%M:%S')
    if f%25==0: _w(S)
    if f%150==0: return 30.0
    return 1.0 if dt<8 else 3.0
def start(ep_dir,end):
    sc=bpy.context.scene
    sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.render.resolution_percentage=100
    sc.eevee.taa_render_samples=24; sc.eevee.use_raytracing=False
    sc.render.use_compositing=False; sc.render.use_sequencer=False
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGB'
    os.makedirs(os.path.join(ep_dir,'frames'),exist_ok=True)
    bpy.app.driver_namespace['TUCK_RENDER']={'f':1,'end':end,'dir':os.path.join(ep_dir,'frames'),'state':'start'}
    bpy.app.timers.register(tuck_render_step,first_interval=2.0)
# usage: start(r'C:\Users\81803\TremenFilm\ep02', <last frame>)
