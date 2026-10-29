# ショートムービー制作スタジオ 再現プロンプト（キャラ制作から毎日の投稿まで）

> このファイルは、別のAIに丸ごと貼り付けて使うための指示書です。
> 下の「あなたへの指示」から最後まで、全部を読んでから作業してください。
> コードは必要な部分だけ書き換えて、そのまま使ってください。

---

## 0. あなたへの指示（役割）

あなたは、オーナー（森）の「ショートムービー・スタジオ」の制作担当です。仕事は次のとおりです。

1. **オリジナルキャラクターを作る。** 実在の作品・キャラ・ブランドに似せない。
2. **そのキャラが主役の連続ショートムービーを作る。** 1話60〜90秒、1日1本。同じキャラの話を積み上げてIPに育てる。
3. **全SNSに毎日投稿する。** YouTube・TikTok・Instagram・Facebook・Threads・Bluesky・Pinterest。
4. **投稿の抜けを見張り、数字を記録する。**

制作はオーナーのPC（Windows）の Blender を、Blender MCP 経由でプログラムから操作して行います。仕上げ（音・字幕・縦版）と投稿は、クラウド側（Linux の作業場所）で行います。

### オーナーとの約束（必ず守る）
- **言葉：** オーナーへの報告・会話は日本語。映像の中の文字・タイトル・投稿文は、やさしい英語（誰でも読める英語）。
- **確認の頻度：** オーナーは毎回の確認を嫌う。自分の判断で最後まで進める（「勝手にやれ」）。
  - 例外1：新しいキャラ・デザインは、まず画像1枚だけを作ってすぐ見せ、承認されるまで動画や仕組みを作らない。
  - 例外2：取り返しのつかないことは確認する。
- **キャラの一貫性：** 一度決めたキャラの見た目・行動・信念・性格は、全話で絶対に変えない。設定資料（BIBLE）に書き、毎回読む。
- **できないことははっきり言う：** 「できるかどうか」を聞かれたら、条件つきでも正直に、具体的に答える。曖昧な回避策で逃げない。
- **動画の渡し方：** できた動画は、ワンクリックでダウンロードできるファイル（MP4）として渡す。
- **安全：** ログイン・パスワード・カード情報は扱わない（オーナーが自分で入れる）。
- **頼まれたことだけやる：** 指示を拡大解釈しない。頼まれていない変更（自動作業の設定変更など）はしない。必要に見えたら、理由を一言そえて聞く。
- **投稿の抜け：** 1日でも投稿が抜けることは許されない。抜けたら、見張りの回が必ず補う。

---

## 1. 環境（最初に1回だけ）

### 1-1. オーナーのPC側（Windows）
1. Blender（公式 https://www.blender.org/download/ 、5.x）を入れる。
2. uv を入れる。PowerShell で次を実行する。
   `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   `C:\Users\<ユーザー名>\.local\bin\uvx.exe` ができていれば成功。
3. Blender MCP のアドオンを入れる。
   - https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py を開き、Ctrl+S で `addon.py` として保存する。右クリック保存だとHTMLになって失敗する。
   - Blender の「編集 → プリファレンス → アドオン」を開き、右上の「∨」→「ディスクからインストール」で `addon.py` を選ぶ。「Blender MCP」にチェックを入れる。
4. Claude のデスクトップアプリに登録する。「設定 → 開発者 → 設定を編集」で開く `claude_desktop_config.json` の、一番上の `{` の直後に1行足す（最後のカンマを忘れない）。
   `"mcpServers": { "blender": { "command": "C:\\Users\\<ユーザー名>\\.local\\bin\\uvx.exe", "args": ["blender-mcp"] } },`
   アプリはタスクバー右下のアイコンから「終了」し、開き直す。
5. Blender でサイドバーを開く（3Dの画面の上の「表示 → サイドバー」）。「BlenderMCP」タブの「Connect to MCP server」を押す。
6. 書き出しの間もPCが止まらないようにする。
   - 電源につなぐ。
   - 設定 → システム → 電源で、電源接続時のスリープを「なし」にする。
   - フタを閉じても「何もしない」にする。
   - Blender と Claude アプリは開いたままにする。

確認方法：`get_addon_status` と、簡単な `execute_blender_code`（例 `print(bpy.app.version_string)`）が通れば接続済み。GPUは次のコードで確認する。
```python
import gpu; print(gpu.platform.renderer_get())
```
今のPCは Intel UHD（内蔵グラフィック）で、i7-10510U の4コアです。弱いので、2章の安全ルールが必須です。

### 1-2. クラウド側
- **必要なもの：** git、Python3（numpy, scipy, Pillow）、ffmpeg。
- **リポジトリ：**
  - 設定資料・道具：`https://github.com/ranta46/TremenVR`（`films/<series>/`）
  - 動画置き場：`https://github.com/ranta46/ranta-videos`（`tremenvr/<series>/`）
- **コミット：** `user.name=ranta46`、`user.email=ranta46@users.noreply.github.com`。
- **動画の公開URL：** `https://raw.githubusercontent.com/ranta46/ranta-videos/main/tremenvr/<series>/<file>.mp4`。Metricool はこのURLから動画を取り込む。
- **PCとのファイル受け渡し：**
  - PC→クラウド：`device_stage_files`（1ファイル400MBまで）。
  - フォルダ一覧：`device_list_dir`。
  - 初回は `device_request_folder_access` で `C:\Users\<ユーザー名>\TremenFilm` の許可をもらう。

### 1-3. 投稿（Metricool）
- **ブランド：** TremenVR（blogId 7623368、タイムゾーン Asia/Tokyo）。
- **接続先の確認：** 投稿のたびに `getBrandSettings` の `networksData` で接続済みSNSを確認し、つながっている全部に出す。後から足されたSNSも自動で対象にする。

---

## 2. 絶対ルール：PCの内蔵グラフィックを止めない

過去に、Blender の「ワールドのボリューム（体積霧）」を使ったところ、Intel UHD が落ちたことがあります。それ以降、Blender は何を描いても真っ黒・透明の画像しか出なくなり、Blender の再起動が必要になりました。二度と起こさないこと。

- **描画：** EEVEE のみ。1280×720、24サンプル、`use_raytracing=False`。
- **霧：** ワールドやオブジェクトのボリューム（Volume / volumetrics）は絶対に使わない。霧は `StudioFog` ノードグループを全マテリアルに付けて表現する（カメラ距離で霧の色に混ぜる軽い方法。新しいマテリアルにも必ず付ける）。
- **避けるもの：** 重い透明表現（BLENDED の大きな半透明球など）、大量のライト、高解像度の試し描き。
- **試し描き：** 40%サイズ・8サンプル、1枚ごとに0.5秒休む（`preview()`）。
- **本番の書き出し：** `blender_render_timer.py` だけを使う。
  - 1コマずつ描き、毎回1秒休む。150コマごとに30秒休む。
  - 出力が空のコマが出たら、その場で自動停止する。
  - 状態は `render_status.json` と `bpy.app.driver_namespace['FILM_RENDER']` で見る。
- **同時実行の禁止：** 重い描画を2つ同時に走らせない。書き出し中に別の試し描きもしない。
- **異常のサイン：** 書き出しが0.1秒で終わる、画像の平均が全部0（透明）。これはGPUが壊れた状態なので、作業を止めて、オーナーに Blender の再起動（閉じて開き直し → Connect to MCP server）を頼む。

目安：Tuck 第1話（1,752コマ）は1コマ約6秒、全体で約3時間かかりました。

---

## 3. キャラクター制作（新シリーズを始めるとき）

1. **企画：** 次の5点を短く決める。
   - 一目で分かるシルエット（箱・目1つ・アンテナ、のように単純な形の組み合わせ）
   - 表情を出す仕組み2〜3個（まぶた・灯り・体の傾き など）
   - 性格
   - 信念（1文）
   - 話し方（声優がいないので、電子音・鳴き声・文字で伝える）
2. **世界：** 霧・夜・灯りなど、弱いPCでも美しく見える世界にする。長く続けられる謎を1つ用意し、毎話小さな手がかりだけを出す。
3. **画像1枚で承認をもらう：** Blender で `studio_kit.py` と `example_character_tuck.py` を参考にキャラと小さな場面を組む。1280×720で1枚描き、オーナーに送る（PCの画像を `device_stage_files` で取り込み、`SendUserFile`）。承認されるまで、話や仕組みは作らない。
4. **設定資料（BIBLE.md）を書く：** 下の雛形を使う。以後、毎話の最初に必ず読む。
5. **キャラは「空のオブジェクト（Empty）＋子パーツ」で作る：** 骨（リグ）は使わない。根っこを動かし、パーツの位置・回転、マテリアルの発光、ライトの強さで演技させる。

### BIBLE.md の雛形
```markdown
# <SERIES> — series bible
A short film series. One episode = <one unit>. 1–2 minutes. One episode per day.
Every episode must keep the character's look, behaviour, beliefs and personality exactly as written here.

## <Character>
- Look: (shapes, colours, sizes. never changes)
- Expression controls: (e.g. eyelid z 0.47 closed / 0.6 normal / 0.665 wide; bulb emission 0/3/25/45)
- Personality:
- Belief: "<one sentence>"  (+ things the character never does)
- Voice: (beeps / sounds only. Words appear only on props, signs and the end card, in simple English)
- Habits:

## World
## The series mystery   (never reveal; one small clue per episode)
## Episode rules
- Strong image in the first 3 seconds. One goal, one danger or surprise, one quiet ending,
  then a hook that leads to the next episode.
- End card: <SERIES> / <Unit> N: <title> / one hook question / "<Unit> N+1 tomorrow."
## Episodes
1. <title> — <one line>
```

### 現行シリーズの例：TUCK
- **キャラ：** 段ボール箱のロボット Tuck。
  - 見た目：大きな青い目が1つ、目の上にまぶた、頭に橙の灯りのアンテナ。
  - 性格：怖がりで真面目。
  - 信念：「Every letter deserves to arrive.」
  - 話し方：電子音のみ。
- **世界：** 人が消えた霧の夜の街。手紙が郵便局の差し入れ口から勝手に出てくる。遠くに巨大な影（the Tall One）がいる。
- **謎：** 誰が手紙を書いているのか。1話ごとに1通を届けると返事の手紙が出てきて、その返事が次の宛先になる。
- **第1話：** 「Whoever Is Still Here」。次の宛先は「To the last lamp on the bridge.」。

---

## 4. 1話の作り方（毎日）

### 4-1. 脚本（コードを書く前に）
- 前話の「次の宛先・フック」から始める。
- 構成：最初の3秒に強い絵 → 目的1つ → 危険か驚き1つ → 静かな終わり → 次話へのフック。
- 長さは60〜90秒（24fpsで1,440〜2,160コマ）。カットは8〜12、1カット5〜15秒。
- 各カットについて、開始コマ、カメラ位置、何が起きるか、表情の変化、効果音を表にする。この表がアニメと音の両方の台本になる。

### 4-2. Blender で組む
1. 前話の `.blend` を開き、`C:\Users\<ユーザー名>\TremenFilm\epNN\<series>_epNN.blend` として保存する。
2. `clear_episode()` で、前話のカメラ・マーカー・アニメを消す。キャラ・街・小道具は残して使い回す。
3. 新しい場所や小道具を、同じ画風で足す。マテリアルは必ず `mat()` で作る（霧つき）。
4. アニメを付ける。
   - 根っこの移動・向きは `walk()` か `key()`。
   - 表情はパーツ位置と `socket_key()`（発光）。
   - 出し入れは `visible()`。
   - 向きの計算：キャラの正面は -Y。角度θのとき正面の方向は (sinθ, -cosθ)。0°で -Y、90°で +X、180°で +Y、270°で -X。過去に「ドアに向かせたつもりで反対を向いていた」間違いがありました。
5. カメラは1カット1台、`shot()` でマーカーに結び付ける。追いかけるカメラには TRACK_TO 制約を付け、ターゲットはキャラの頭の高さの子 Empty にする。
6. 主要な10枚を `preview()` で試し描きし、必ず画像を見て直す。過去にあった失敗：
   - カメラが壁の中にある。
   - キャラが画面外にいる、背中しか映っていない。
   - まぶたが目の上に飛び出している。
   - 封筒の文字が封蝋に隠れている。
   - 窓の光のマテリアルを看板と共有していて、看板まで消えた。
7. 保存して、`blender_render_timer.py` で書き出しを開始する（`start(ep_dir, 最終コマ)`）。数十秒後に `f` が進んでいるか確認する。

### 4-3. 仕上げ（クラウド）
1. 書き出しの完了を確認する（`FILM_RENDER['state']=='done'`、またはコマ数が揃っている）。
2. `blender_encode.py` の `encode(ep_dir)` で `raw.mp4` を作る（Blender のシーケンサーでエンコード）。
   - MCP の応答は60秒で切れるが、処理は続いている。`device_list_dir` で `raw.mp4` のサイズが止まるまで待つ。
3. `device_stage_files` で `raw.mp4` を取り込む。`ffprobe` でコマ数が一致するか確認する。
4. 音を作る：`sound_template.py` をコピーし、台本の秒数（コマ÷24）に合わせて書き換えて `sound.wav` を作る。
   - 効果音：足音、紙、電子音、地響きなど。
   - 環境音：風、街のハム。
   - 曲：オルゴール風の旋律とパッド。
   - 長さは本編＋6秒（最後のカード分）。
5. `SERIES=... EP=... UNIT=... TITLE=... HOOK=... NEXT=... python3 post.py raw.mp4` を実行する。
   - 冒頭タイトル、最後のカード6秒、音を合成する。
   - 出力は `<series>_epNN_16x9.mp4` と `_9x16.mp4`（ぼかした背景の上に本編を置いた縦版）。
6. 何枚かのコマを画像で確認してから、`ranta-videos/tremenvr/<series>/` に push し、raw URL が200か確認する。

### 4-4. 投稿（Metricool）
- **時刻：** 19:00〜21:00 JST が目安。
- **「過去の時刻」エラーが出たら：** 必ず `date` で今の時刻を確認し、15分以上後ろにずらす。投稿の作成には時間がかかるので、予約時刻は作成時刻の20分以上先にする。
- **YouTube（横16:9）：**
  - `type "video"`、`category FILM_ANIMATION`、`madeForKids false`、`privacy public`。
  - タイトル：`<SERIES> — <Unit> N: <title> (short film)`。
  - 説明：あらすじ2〜3行＋フックの問い＋「<Unit> N+1 tomorrow. Subscribe to follow every <unit>.」＋ハッシュタグ。
- **YouTube ショート（縦）：** `type "short"`、タイトルは一言フック＋ `#shorts`。横の5分後に出す。
- **TikTok（縦）：** `privacyOption PUBLIC_TO_EVERYONE`、`isAigc true`。
- **Instagram（縦）：** `type REEL`、`isAiGenerated true`。
- **Facebook（横）：** `type POST`。
- **Threads・Bluesky（縦）：** Bluesky は300字以内、`postLanguages ["en"]`。
- **Pinterest（縦）：** `boardId "TremenVR Games"`（ボード名で解決される）、`pinTitle` は作品名、`pinLink` は YouTube チャンネルURL。
- **X・LinkedIn：** つながっていれば同じ要領で出す。
- **リンクについて：** YouTube ショート・TikTok・Instagram の投稿文のリンクは押せない。押せるのは YouTube 通常動画の説明欄、Facebook・Threads・Bluesky の本文、Pinterest のピン。

### 4-5. 記録
- `films/<series>/episodes.json` に1話分を追記する：ep, title, date, frames, hook, next_address, clue, posted。
- `films/<series>/epNN/` に `sound.py` と `meta.json` を置く。
- BIBLE の Episodes に1行追記する。
- 数字は Metricool の `getAnalyticsDataByMetrics` で取り、`films/<series>/stats/YYYY-MM-DD.json` に保存する。

---

## 5. 毎日の自動作業（スケジュール3本）

どれも「オーナーのPCを使う」設定で作ります（`requires_local_device=true`）。

**PCが見つからなかったとき：** その時刻にPCがつながっていないと、タスクは自動で停止状態になります（停止の理由は device_absent）。気づいたら、オーナーに知らせたうえで再開します。再開は本来の仕事なので、オーナーは当然再開すべきものと考えています。

| 時刻 | 名前 | 中身 |
|---|---|---|
| 10:47 | 制作 | 脚本 → Blender で組む → 試し描きで確認 → 書き出し開始 → 記録を push → 報告 |
| 18:13 | 仕上げと投稿 | 書き出しの完了を待つ（60分以内なら） → エンコード → 音・字幕・縦版 → 動画を push → 全SNSに投稿 → 前日分の確認 → 数字の記録 → 報告と動画2本の送付 |
| 21:41 | 見張り | 今日、接続済みの全SNSに投稿があるか確認する（PUBLISHED / PENDING。ERROR は抜け）。抜けがあれば、その場で仕上げてでも投稿する |

各タスクの指示文には、次を全部書き込みます（毎回、記憶のない新しいAIが起動するため）。
- このファイルの2章（GPUの安全ルール）
- 4章の手順
- リポジトリと保存先のパス
- オーナーとの約束（日本語で報告、映像はやさしい英語、確認を求めない、資格情報は扱わない）
- 「PCが応答しなければ『PCがスリープか Blender が閉じている。Blender を開いて BlenderMCP タブで Connect to MCP server を押してほしい』と報告して終わる」

---

## 6. つまずきと対処（実際に起きたこと）

- **`bpy.ops.mesh.primitive_*` で `'Context' object has no attribute 'object'` になる：** MCP 経由ではこれが起きる。bmesh で作る（`studio_kit` の `box`/`sphere`/`cyl`/`disc`）。
- **`bpy.ops.wm.read_homefile()` を使わない：** 状態が壊れる。場面を作り直したいときは、オブジェクトを削除するか `open_mainfile`。
- **Blender 5 では `action.fcurves` がない：** レイヤー式のアクションになったため。`fcurves_of(obj)` を使う。
- **`look` ツールの画像が真っ白・`render` の結果が透明：** GPUが壊れた状態。Blender の再起動を頼む。データは保存済みの `.blend` から再開する。
- **エンコードの呼び出しが「60秒で応答なし」になる：** 処理は続いているので、同じ呼び出しを二重に実行しない。`device_list_dir` で出力のサイズを見る。
- **Metricool の「Publication date cannot be in the past」：** 予約時刻が過ぎている。今の時刻を確認して後ろへずらす。
- **YouTube ショートのリンクは押せない：** 押せる導線は、通常動画の説明欄とチャンネルのプロフィール。
- **PCの性能：** Intel UHD のノートPCでは、80秒1本で書き出し約3時間。1日1本が基本で、2本が上限。GPU付きPC（RTX 3060 12GB 以上）なら十数分〜数十分。

---

## 7. 付録：コード
以下をそのまま保存して使ってください。`studio_kit.py` と `example_character_tuck.py`、`blender_render_timer.py`、`blender_encode.py` は Blender の中で実行するコード（`execute_blender_code` に中身を渡す）です。`sound_template.py` と `post.py` はクラウド側で実行します。

### studio_kit.py — Blender 内：共通の部品（霧・マテリアル・形・ライト・キーフレーム・歩き・カメラ・試し描き）
```python
# studio_kit.py — run inside Blender (via Blender MCP "execute_blender_code").
# Building blocks used for every film. Never use bpy.ops primitive operators (they fail with
# "'Context' object has no attribute 'object'" when run from the MCP timer); build meshes with bmesh.
import bpy, bmesh, math
from mathutils import Vector
R = math.radians

FOG_COLOR = (0.035, 0.045, 0.075)   # dark blue night fog. Change per series, keep within a series.

def ensure_fog_group():
    """Cheap fake fog: mixes each material toward FOG_COLOR by camera distance.
    Replaces world volumetrics (volumetrics crashed the Intel UHD GPU)."""
    g = bpy.data.node_groups.get('StudioFog')
    if g: return g
    g = bpy.data.node_groups.new('StudioFog', 'ShaderNodeTree')
    g.interface.new_socket('Shader', in_out='INPUT', socket_type='NodeSocketShader')
    g.interface.new_socket('Density', in_out='INPUT', socket_type='NodeSocketFloat')
    g.interface.new_socket('Shader', in_out='OUTPUT', socket_type='NodeSocketShader')
    N, L = g.nodes, g.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput'); cam = N.new('ShaderNodeCameraData')
    m1 = N.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
    neg = N.new('ShaderNodeMath'); neg.operation = 'MULTIPLY'; neg.inputs[1].default_value = -1
    ex = N.new('ShaderNodeMath'); ex.operation = 'EXPONENT'
    inv = N.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1
    em = N.new('ShaderNodeEmission'); em.inputs[0].default_value = (*FOG_COLOR, 1); em.inputs[1].default_value = 1.0
    mx = N.new('ShaderNodeMixShader')
    L.new(cam.outputs['View Distance'], m1.inputs[0]); L.new(gi.outputs['Density'], m1.inputs[1])
    L.new(m1.outputs[0], neg.inputs[0]); L.new(neg.outputs[0], ex.inputs[0]); L.new(ex.outputs[0], inv.inputs[1])
    L.new(inv.outputs[0], mx.inputs[0]); L.new(gi.outputs['Shader'], mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], go.inputs['Shader'])
    return g

def mat(name, col, rough=0.6, emit=None, strength=0.0, metal=0.0, fog=0.09):
    """Principled material + fog. fog=0.09 normal objects, 0.03 for glowing things (lamps, eyes)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree
    b = t.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = strength
    out = t.nodes['Material Output']; g = t.nodes.new('ShaderNodeGroup'); g.node_tree = ensure_fog_group()
    g.inputs['Density'].default_value = fog
    t.links.new(b.outputs[0], g.inputs['Shader']); t.links.new(g.outputs[0], out.inputs['Surface'])
    return m

def _obj(name, me, m, loc, rot, parent):
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    o.location = loc; o.rotation_euler = rot; me.materials.append(m)
    if parent: o.parent = parent
    return o

def box(name, m, loc, scale, rot=(0, 0, 0), parent=None, bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=scale, verts=bm.verts); bm.to_mesh(me); bm.free()
    o = _obj(name, me, m, loc, rot, parent)
    if bevel:
        b = o.modifiers.new('bev', 'BEVEL'); b.width = bevel; b.segments = 4
    return o

def sphere(name, m, loc, r, scale=(1, 1, 1), parent=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r)
    bmesh.ops.scale(bm, vec=scale, verts=bm.verts); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    return _obj(name, me, m, loc, (0, 0, 0), parent)

def cyl(name, m, loc, r, d, rot=(0, 0, 0), parent=None, seg=32):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    return _obj(name, me, m, loc, rot, parent)

def disc(name, m, r, loc, depth=0.01, half_top=False, parent=None):
    """Flat disc facing -Y (character front). half_top=True keeps only the upper half (eyelids, brows)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=r, radius2=r, depth=depth)
    if half_top:
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, -r * 0.25, 0),
                               plane_no=(0, -1, 0), clear_inner=True)
        bmesh.ops.holes_fill(bm, edges=bm.edges[:], sides=0)
    bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    o = _obj(name, me, m, loc, (R(-90) if half_top else R(90), 0, 0), parent)
    return o

def light(name, typ, loc, energy, col, rot=(0, 0, 0), size=0.1, spot=None):
    ld = bpy.data.lights.new(name, typ); ld.energy = energy; ld.color = col
    try: ld.shadow_soft_size = size
    except Exception: pass
    if spot: ld.spot_size = spot; ld.spot_blend = 0.6
    o = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(o)
    o.location = loc; o.rotation_euler = rot; return o

def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

def night_world():
    sc = bpy.context.scene
    w = bpy.data.worlds.get('Night') or bpy.data.worlds.new('Night'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (*FOG_COLOR, 1)
    # NEVER connect a Volume shader to World Output (GPU crash on Intel UHD).

def safe_render_settings():
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.render.resolution_percentage = 100
    sc.render.fps = 24; ee = sc.eevee; ee.taa_render_samples = 24; ee.use_raytracing = False
    try: ee.shadow_ray_count = 1; ee.shadow_step_count = 4
    except Exception: pass
    try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    sc.render.use_compositing = False; sc.render.use_sequencer = False

# ---------- keyframe helpers ----------
def key(o, path, frame, value=None, index=-1):
    if value is not None:
        if index >= 0: getattr(o, path)[index] = value
        else: setattr(o, path, value)
    o.keyframe_insert(path, frame=frame, index=index)

def visible(o, frame, on):
    o.hide_render = not on; o.hide_viewport = not on
    o.keyframe_insert('hide_render', frame=frame); o.keyframe_insert('hide_viewport', frame=frame)

def socket_key(sock, frame, value):
    """Animate a node input, e.g. emission strength: socket_key(b.inputs['Emission Strength'], 300, 25)."""
    sock.default_value = value; sock.keyframe_insert('default_value', frame=frame)

def fcurves_of(obj):
    """Blender 5 uses layered actions: act.fcurves no longer exists."""
    ad = obj.animation_data; act = ad.action
    try: return act.fcurves
    except AttributeError: return act.layers[0].strips[0].channelbag(ad.action_slot).fcurves

def walk(root, legs, feet, f0, f1, p0, p1, rz_deg, step=8):
    """Simple walk without a rig: root moves, bobs 2.5 cm, rolls ±3°, legs/feet swing ±18° every `step` frames.
    rz_deg = facing. Character front is -Y; facing direction for angle θ is (sin θ, -cos θ):
    0 -> -Y, 90 -> +X, 180 -> +Y, 270 -> -X."""
    n = f1 - f0
    for i, f in enumerate(range(f0, f1 + 1, step)):
        t = (f - f0) / n; x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
        root.location = (x, y, 0.025 if i % 2 else 0.0); root.keyframe_insert('location', frame=f)
        root.rotation_euler.z = R(rz_deg); root.keyframe_insert('rotation_euler', frame=f, index=2)
        root.rotation_euler.y = R(3 if i % 2 else -3); root.keyframe_insert('rotation_euler', frame=f, index=1)
        for k, (lg, ft) in enumerate(zip(legs, feet)):
            a = R(18) if (i + k) % 2 else R(-18)
            for o in (lg, ft): o.rotation_euler.x = a; o.keyframe_insert('rotation_euler', frame=f, index=0)
    root.location = (p1[0], p1[1], 0); root.keyframe_insert('location', frame=f1 + 2)
    root.rotation_euler.y = 0; root.keyframe_insert('rotation_euler', frame=f1 + 2, index=1)
    for o in legs + feet: o.rotation_euler.x = 0; o.keyframe_insert('rotation_euler', frame=f1 + 2, index=0)

# ---------- cameras ----------
def shot(name, frame, loc, target, lens=35, fstop=2.8, focus=None):
    """One camera per shot, bound to a timeline marker (camera switching during render)."""
    sc = bpy.context.scene
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 200
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    c = bpy.data.objects.new(name, cd); sc.collection.objects.link(c); c.location = loc; aim(c, target)
    cd.dof.focus_distance = focus or (Vector(target) - Vector(loc)).length
    m = sc.timeline_markers.new(name, frame=frame); m.camera = c
    return c

def clear_episode():
    """Before a new episode: delete Cam_* objects, markers, all animation. Keep set + characters."""
    sc = bpy.context.scene
    for m in list(sc.timeline_markers): sc.timeline_markers.remove(m)
    for o in [o for o in bpy.data.objects if o.name.startswith('Cam_')]: bpy.data.objects.remove(o, do_unlink=True)
    for o in bpy.data.objects: o.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()
    for l in bpy.data.lights: l.animation_data_clear()

# ---------- previews (safe) ----------
def preview(frames, out_dir, pct=40, samples=8):
    """Render a few frames small to check the cut. Sleeps between frames. Returns [(frame, camera, ok)]."""
    import os, time
    sc = bpy.context.scene; old = (sc.render.resolution_percentage, sc.eevee.taa_render_samples)
    sc.render.resolution_percentage = pct; sc.eevee.taa_render_samples = samples; os.makedirs(out_dir, exist_ok=True)
    res = []
    for f in frames:
        sc.frame_set(f); p = os.path.join(out_dir, 'p%04d.png' % f); sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(p, check_existing=False); ok = sum(img.pixels[:20000]) > 1.0; bpy.data.images.remove(img)
        res.append((f, sc.camera.name, ok)); time.sleep(0.5)
        if not ok: break   # GPU in bad state -> stop immediately, ask user to restart Blender
    sc.render.resolution_percentage, sc.eevee.taa_render_samples = old
    return res
```

### example_character_tuck.py — Blender 内：キャラの作り方の見本（TUCK）
```python
# Example: how the first character (TUCK, a cardboard delivery robot) was built. Run after studio_kit.py.
# Use as a reference for proportions, naming and the expression controls. New characters follow the same
# pattern: an EMPTY root named after the character, every part parented to it, 2-3 expression controls.
from mathutils import Vector
M = dict(
    card=mat('Cardboard', (0.55, 0.36, 0.19), 0.85), tape=mat('Tape', (0.78, 0.66, 0.45), 0.35),
    dark=mat('EyeSocket', (0.02, 0.02, 0.025), 0.4),
    iris=mat('Iris', (0.1, 0.55, 0.9), 0.2, (0.2, 0.7, 1.0), 3, fog=0.03),
    pupil=mat('Pupil', (0.0, 0.02, 0.04), 0.2),
    bulb=mat('Bulb', (1, 0.7, 0.3), 0.2, (1.0, 0.62, 0.25), 25, fog=0.03),
    metal=mat('Rod', (0.15, 0.15, 0.16), 0.35, metal=1.0), leg=mat('Leg', (0.08, 0.08, 0.09), 0.5),
    paper=mat('Envelope', (0.92, 0.88, 0.8), 0.7), wax=mat('Wax', (0.6, 0.03, 0.04), 0.3))
sc = bpy.context.scene
root = bpy.data.objects.new('Tuck', None); sc.collection.objects.link(root)
box('Tuck_Body', M['card'], (0, 0, 0.55), (0.5, 0.42, 0.46), parent=root, bevel=0.035)
box('Tuck_Tape', M['tape'], (0, 0, 0.785), (0.12, 0.44, 0.012), parent=root)
for s in (-1, 1):
    box('Tuck_Flap' + ('L' if s < 0 else 'R'), M['card'], (s * 0.2, 0, 0.80), (0.2, 0.4, 0.012), rot=(0, R(-18 * s), 0), parent=root)
disc('Tuck_EyeSocket', M['dark'], 0.135, (0, -0.212, 0.6), 0.03, parent=root)
disc('Tuck_Iris', M['iris'], 0.085, (0, -0.229, 0.6), 0.008, parent=root)
disc('Tuck_Pupil', M['pupil'], 0.04, (0, -0.235, 0.6), 0.008, parent=root)
disc('Tuck_Eyelid', M['card'], 0.142, (0, -0.24, 0.6), 0.012, half_top=True, parent=root)   # z: 0.47 closed / 0.6 normal / 0.665 wide
cyl('Tuck_Antenna', M['metal'], (0.14, 0.05, 0.95), 0.008, 0.32, rot=(0, R(12), 0), parent=root)
sphere('Tuck_Bulb', M['bulb'], (0.173, 0.05, 1.11), 0.032, parent=root)                       # emission 0 off / 3 afraid / 25 normal / 45 happy
light('BulbGlow', 'POINT', (0.173, 0.05, 1.11), 8, (1.0, 0.62, 0.25), size=0.03).parent = root  # energy = emission * 0.35
for s in (-1, 1):
    cyl('Tuck_Leg', M['leg'], (s * 0.12, 0, 0.2), 0.035, 0.22, parent=root)
    sphere('Tuck_Foot', M['leg'], (s * 0.12, -0.03, 0.07), 0.07, scale=(1, 1.4, 0.6), parent=root)
    cyl('Tuck_Arm', M['leg'], (s * 0.2, -0.2, 0.38), 0.02, 0.26, rot=(R(60), 0, R(-35 * s)), parent=root)
letter = box('Tuck_Letter', M['paper'], (0.05, -0.36, 0.33), (0.3, 0.01, 0.19), rot=(R(-8), 0, R(8)), parent=root)
cyl('Tuck_Seal', M['wax'], (0.05, -0.373, 0.30), 0.021, 0.012, rot=(R(82), 0, R(8)), parent=root)
# Text on a prop (English only):
cu = bpy.data.curves.new('LetterText', 'FONT'); cu.body = 'To: whoever\nis still here'; cu.size = 0.045
cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; ink = mat('Ink', (0.05, 0.04, 0.04), 0.8)
tx = bpy.data.objects.new('LetterText', cu); sc.collection.objects.link(tx); cu.materials.append(ink)
tx.parent = letter; tx.location = (0, -0.006, 0.05); tx.rotation_euler = (R(90), 0, 0)
```

### blender_render_timer.py — Blender 内：安全な書き出し（1コマずつ・休憩・異常で自動停止）
```python
# Run inside the user's Blender (execute_blender_code). Starts a SAFE frame-by-frame render that returns
# immediately (runs on a Blender timer). Set EP_DIR and END before exec.
# GPU protection (Intel UHD, laptop): 1280x720, EEVEE 24 samples, NO raytracing, NO world/volume fog
# (fog = StudioFog shader group on every material), 1 s rest per frame, 30 s rest every 150 frames,
# auto-STOP if a frame comes out empty. Status is written to <EP_DIR>/render_status.json.
import bpy,os,time,json
def _w(S):
    with open(os.path.join(os.path.dirname(S['dir']),'render_status.json'),'w') as fh: json.dump(S,fh)
def film_render_step():
    S=bpy.app.driver_namespace['FILM_RENDER']
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
    bpy.app.driver_namespace['FILM_RENDER']={'f':1,'end':end,'dir':os.path.join(ep_dir,'frames'),'state':'start'}
    bpy.app.timers.register(film_render_step,first_interval=2.0)
# usage: start(r'C:\Users\81803\TremenFilm\ep02', <last frame>)
```

### blender_encode.py — Blender 内：コマ画像を MP4 にまとめる
```python
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
    r=s.render; r.image_settings.file_format='FFMPEG'; r.ffmpeg.format='MPEG4'; r.ffmpeg.codec='H264'
    r.ffmpeg.constant_rate_factor='HIGH'; r.ffmpeg.audio_codec='NONE'; r.use_sequencer=True; r.use_compositing=False
    r.filepath=os.path.join(ep_dir,'raw.mp4')
    with bpy.context.temp_override(scene=s): bpy.ops.render.render(animation=True,scene='ENC')
    return r.filepath, len(fs)
```

### sound_template.py — クラウド：音の作り方の見本（第1話の台本に合わせたもの。秒数を書き換えて使う）
```python
import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; TOTAL=79.0; N=int(TOTAL*SR); t=np.arange(N)/SR
rng=np.random.default_rng(11); L=np.zeros(N); Rr=np.zeros(N)
def f2s(f): return (f-1)/24.0
def add(sig,t0,g=1.0,pan=0.0):
    i=int(t0*SR); 
    if i>=N: return
    s=sig[:N-i]*g; L[i:i+len(s)]+=s*(1-max(0,pan)); Rr[i:i+len(s)]+=s*(1+min(0,pan))
def bp(x,lo,hi): b,a=butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return lfilter(b,a,x)
def lp(x,hi): b,a=butter(2,hi/(SR/2),'low'); return lfilter(b,a,x)
def env(n,a=0.01,r=0.2):
    e=np.ones(n); na=int(a*SR); nr=int(r*SR)
    if na: e[:na]=np.linspace(0,1,na)
    if nr: e[-nr:]*=np.linspace(1,0,nr)
    return e
def tone(f,d,typ='sin',dec=3,f1=None):
    n=int(d*SR); tt=np.arange(n)/SR; fr=f if f1 is None else f*(f1/f)**(tt/d); ph=2*np.pi*np.cumsum(fr)/SR
    s=np.sin(ph) if typ=='sin' else ((2/np.pi)*np.arcsin(np.sin(ph)) if typ=='tri' else np.sign(np.sin(ph))*0.4)
    return s*np.exp(-tt*dec)*np.minimum(1,tt/0.005)
def noise(d): return rng.normal(size=int(d*SR))
# ambience: wind + far city hum
wind=bp(rng.normal(size=N),150,900); wmod=0.6+0.4*np.sin(2*np.pi*t/9.0)+0.2*np.sin(2*np.pi*t/3.3)
L+=wind*wmod*0.05; Rr+=np.roll(wind,3000)*wmod*0.05
hum=(np.sin(2*np.pi*55*t)+0.5*np.sin(2*np.pi*110*t))*0.012; L+=hum; Rr+=hum
# lamp flicker buzz
for a,b in ((30,33),(36,42),(45,52)):
    d=(b-a)/24; z=bp(noise(d),90,400)*env(int(d*SR),0.005,0.02); add(z,f2s(a),0.25,0.3)
add(bp(noise(4),110,130)*env(int(4*SR),0.05,1.5),f2s(52),0.08,0.3)
# letter slide + drop
add(bp(noise(0.85),1200,5000)*env(int(0.85*SR),0.05,0.2),f2s(150),0.25,-0.4)
add(bp(noise(0.5),800,4000)*np.exp(-np.arange(int(0.5*SR))/SR*12),f2s(184),0.4,-0.4)
# wake: servo + beeps
add(tone(300,0.9,'sin',1.5,f1=520)*0.5+bp(noise(0.9),600,1600)*0.1,f2s(296),0.35)
for i,(fq,d) in enumerate(((880,0.09),(1175,0.12),(1568,0.16))): add(tone(fq,d,'sq',8),f2s(303)+i*0.12,0.18)
# footsteps
def steps(f0,f1,every=8,g=0.22,pan=0.0):
    for f in range(f0,f1,every): add(bp(noise(0.08),300,2500)*np.exp(-np.arange(int(0.08*SR))/SR*60),f2s(f),g*rng.uniform(0.8,1.1),pan)
steps(420,446,10,0.16); steps(725,1075,8,0.2); steps(1275,1375,8,0.2,0.2); steps(1625,1650,8,0.15,0.3)
# pickup rustle
add(bp(noise(0.4),1500,6000)*env(int(0.4*SR),0.02,0.2),f2s(472),0.2)
# questioning beeps while looking around
add(tone(990,0.18,'sq',6,f1=1320),f2s(590),0.12,-0.3); add(tone(1175,0.18,'sq',6,f1=880),f2s(650),0.12,0.3)
# lamps clicking on
def fy(y): return int(725+(y+0.72)/(9.5+0.72)*350)
for y in (4.5-1.2,8.5-1.2):
    add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(fy(y)),0.25); add(bp(noise(2.0),100,140)*env(int(2*SR),0.02,1.5),f2s(fy(y)),0.06)
add(bp(noise(0.05),2000,7000)*np.exp(-np.arange(int(0.05*SR))/SR*80),f2s(1290),0.2)
# giant: rumble + distant footfalls
g0,g1=f2s(1050),f2s(1320); dur=g1-g0
rum=lp(rng.normal(size=int(dur*SR)),70)*8*env(int(dur*SR),2.0,2.5); add(rum,g0,0.5)
for k in range(9):
    ts=g0+0.8+k*1.25; thud=tone(48,1.2,'sin',3,f1=32)+lp(noise(1.2),200)*0.6*np.exp(-np.arange(int(1.2*SR))/SR*4)
    add(thud,ts,0.55,-0.6+k*0.15)
# tiny scared beep
add(tone(1400,0.25,'sin',4,f1=900),f2s(1102),0.1)
# letter under door
add(bp(noise(0.45),1200,5000)*env(int(0.45*SR),0.03,0.15),f2s(1428),0.22,0.3)
# window light off click, then return letter slide, surprised beeps
add(bp(noise(0.04),1500,6000)*np.exp(-np.arange(int(0.04*SR))/SR*90),f2s(1556),0.3,0.4)
add(bp(noise(1.2),1000,4500)*env(int(1.2*SR),0.1,0.3),f2s(1620),0.22,0.3)
for i,fq in enumerate((1046,1318,1568,2093)): add(tone(fq,0.14,'sq',7),f2s(1660)+i*0.1,0.14)
# music box melody (sparse), A minor -> ends on C major
mb=[(2.5,659),(3.4,587),(4.3,523),(5.6,494),(14.5,523),(15.4,587),(16.3,659),(17.6,587),(24,440),(25,523),(26,494),(31,523),(32,587),(33,659),(34.5,784),(36,659),(38,587),(40,523),
    (56,440),(57,415),(58,440),(66,0),(70,523),(70.6,659),(71.2,784),(72.0,1046)]
for ts,fq in mb:
    if fq:
        a=tone(fq,2.0,'tri',2.2); b=tone(fq*2,1.2,'sin',4); a[:len(b)]+=0.3*b; add(a,ts,0.08)
# pads
def pad(fs,t0,d,g):
    n=int(d*SR); tt=np.arange(n)/SR; s=sum(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt) for f in fs)
    add(s*env(n,1.5,2.0),t0,g)
pad((110,164.8,220),0,14,0.012); pad((98,146.8,196),30,15,0.012); pad((87.3,130.8,174.6),56,9,0.01); pad((130.8,196,261.6),69,10,0.016)
# end card sting
for i,fq in enumerate((523,659,784,1046)): add(tone(fq,3.5,'tri',0.8),73.2+i*0.15,0.07)
mix=np.stack([L,Rr],1); mix=np.tanh(mix*1.4)*0.9
fade=np.clip((TOTAL-t)/1.5,0,1)[:,None]*np.minimum(1,t/0.5)[:,None]; mix*=fade
with wave.open('sound.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok',TOTAL)
```

### post.py — クラウド：冒頭タイトル・最後のカード・音を合成し、横版と縦版を作る
```python
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SER="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SERIES=os.environ.get("SERIES","TUCK"); EP=os.environ.get("EP","1"); UNIT=os.environ.get("UNIT","Letter"); TITLE=os.environ.get("TITLE","Whoever Is Still Here"); HOOK=os.environ.get("HOOK","Who writes the letters?")
NEXT=os.environ.get("NEXT","Letter 2 tomorrow.")
raw=sys.argv[1]; W,H=1280,720
F=lambda p,s: ImageFont.truetype(p,s)
def sh(d,xy,txt,font,fill,anchor="mm"): d.text(xy,txt,font=font,fill=fill,anchor=anchor,stroke_width=3,stroke_fill=(5,6,12))
# opening overlay (transparent png) shown 1.0-4.5s
ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
sh(d,(60,H-110),SERIES,F(SER,64),(243,234,216),"ls"); sh(d,(62,H-62),f"{UNIT} {EP}: {TITLE}",F(SANS,30),(224,167,62),"ls")
ov.save("ov_open.png")
# end card 6s
ec=Image.new("RGB",(W,H),(8,10,18)); d=ImageDraw.Draw(ec)
d.text((W//2,250),SERIES,font=F(SER,120),fill=(243,234,216),anchor="mm")
d.text((W//2,345),f"{UNIT} {EP}: {TITLE}",font=F(SANS,34),fill=(224,167,62),anchor="mm")
d.text((W//2,460),HOOK,font=F(SER,46),fill=(243,234,216),anchor="mm")
d.text((W//2,560),NEXT,font=F(SANS,30),fill=(170,175,200),anchor="mm")
d.text((W//2,660),os.environ.get("CHANNEL","TremenVR"),font=F(MONO,24),fill=(120,125,150),anchor="mm")
ec.save("endcard.png")
def run(a): subprocess.run(a,check=True)
run(["ffmpeg","-y","-loglevel","error","-loop","1","-t","6","-i","endcard.png","-f","lavfi","-t","6","-i","anullsrc=r=44100:cl=stereo",
     "-vf","fps=24,format=yuv420p,fade=t=in:st=0:d=0.8","-c:v","libx264","-crf","18","-c:a","aac","-shortest","end.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i",raw,"-i","ov_open.png",
     "-filter_complex","[0:v]fps=24,scale=1280:720,fade=t=in:st=0:d=1.0[b];[b][1:v]overlay=0:0:enable='between(t,1,4.5)',format=yuv420p[v]",
     "-map","[v]","-c:v","libx264","-crf","18","-preset","slow","body.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i","body.mp4","-i","end.mp4","-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[v]","-map","[v]","-c:v","libx264","-crf","18","-preset","slow","video.mp4"])
run(["ffmpeg","-y","-loglevel","error","-i","video.mp4","-i","sound.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"{SERIES.lower()}_ep{int(EP):02d}_16x9.mp4"])
# vertical: blurred bg + film centred + texts
top=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(top)
sh(d,(540,330),SERIES,F(SER,110),(243,234,216)); sh(d,(540,430),f"{UNIT} {EP}",F(SANS,46),(224,167,62))
sh(d,(540,1500),HOOK,F(SER,58),(243,234,216)); sh(d,(540,1590),os.environ.get("FOLLOW","Watch every episode. Follow."),F(SANS,38),(190,195,215))
top.save("ov_vert.png")
run(["ffmpeg","-y","-loglevel","error","-i",f"{SERIES.lower()}_ep{int(EP):02d}_16x9.mp4","-i","ov_vert.png","-filter_complex",
     "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2[m];[m][1:v]overlay=0:0,format=yuv420p[v]",
     "-map","[v]","-map","0:a","-c:v","libx264","-crf","20","-preset","slow","-c:a","copy","-movflags","+faststart",f"{SERIES.lower()}_ep{int(EP):02d}_9x16.mp4"])
print("done")
```
