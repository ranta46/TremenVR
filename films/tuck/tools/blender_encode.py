# Run inside Blender after render_status.json says done: encodes frames -> <EP_DIR>/raw.mp4 (no audio).
import bpy,os,glob
def encode(ep_dir):
    fs=sorted(glob.glob(os.path.join(ep_dir,'frames','f*.png')))
    s=bpy.data.scenes.get('ENC') or bpy.data.scenes.new('ENC')
    s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100; s.render.fps=24
    se=s.sequence_editor_create()
    for st in list(se.strips_all): se.strips.remove(st)
    st=se.strips.new_image('frames',fs[0],1,1)
    for f in fs[1:]: st.elements.append(os.path.basename(f))
    s.frame_start=1; s.frame_end=len(fs)
    r=s.render; r.image_settings.media_type='VIDEO'; r.image_settings.file_format='FFMPEG'; r.ffmpeg.format='MPEG4'; r.ffmpeg.codec='H264'
    r.ffmpeg.constant_rate_factor='HIGH'; r.ffmpeg.audio_codec='NONE'; r.use_sequencer=True; r.use_compositing=False
    r.filepath=os.path.join(ep_dir,'raw.mp4')
    with bpy.context.temp_override(scene=s): bpy.ops.render.render(animation=True,scene='ENC')
    return r.filepath, len(fs)
