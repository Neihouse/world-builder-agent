# research gaps — what we didn't know

compiled from deep research on Horizon Worlds import pipeline, materials, audio, scripting, publishing, and monetization. several critical findings that change our approach.

---

## BLOCKERS (must resolve before import)

### 1. desktop editor is WINDOWS ONLY

the Horizon Worlds Desktop Editor (now called Horizon Studio) only runs on Windows via the Meta Quest Link PC app. **no macOS support.** this is the tool you need for:
- importing FBX files
- placing lights, spawn points, trigger zones
- setting up scripting (TypeScript)
- testing and publishing

**options:**
- use a Windows PC or laptop
- run Windows via Boot Camp or Parallels on Mac (if Intel Mac)
- use a cloud Windows VM (Shadow PC, Azure, etc.)
- borrow/rent a Windows machine for import + setup sessions

### 2. blender materials DO NOT transfer

horizon worlds **ignores all Blender shader/material data**. it only reads:
- the **material name** (suffix determines type)
- the **texture filenames** (channel-packed PNGs)

our current build uses procedural materials with no textures. on import, horizon will create materials based on our suffixes (_Metal, _Unlit) but they will be **flat/default** — no roughness, metallic, or emission values carry over from Blender.

**what we need to do:**
- option A: bake textures from Blender into channel-packed PNGs (_BR and _MEO format)
- option B: rely on material suffixes for type, then tweak values in the Horizon editor
- option C: use the [Blender to Horizon Worlds Exporter addon](https://github.com/FairFight14/Blender-to-Horizon-Worlds-Exporter) which automates baking + export

**texture channel packing format:**
| texture | suffix | channels |
|---|---|---|
| TextureA | `_BR` | RGB = base color, A = roughness |
| TextureB | `_MEO` | R = metalness, G = emissive, B = ambient occlusion |

### 3. blender lighting DOES NOT transfer

all 10 lights we placed in Blender are **ignored on FBX import**. lighting must be recreated entirely in the Horizon editor using:
- **Static Light Gizmo** — baked, more detailed, better performance (point, spot, directional)
- **Dynamic Light Gizmo** — scriptable, can change color/intensity at runtime, but more expensive

**our lighting design doc is still valuable** as a reference for recreating the setup in Horizon.

---

## MAJOR CORRECTIONS TO OUR ASSUMPTIONS

### 4. emissive materials don't cast light

our _Unlit materials (Screen_Unlit, OriginRing_Unlit, ReliefGlow_Unlit, FlowGuide_Unlit) will appear self-illuminated but will **not illuminate surrounding geometry**. they are cosmetic glow only.

**fix:** pair every emissive surface with an actual light gizmo in Horizon to simulate light casting. this is what we partially did in Blender — the approach is correct, just need to redo it in Horizon.

### 5. no bloom or post-processing

Quest hardware does not support bloom, color grading, depth of field, or other post-fx. emissive surfaces will look flat-bright, not glowy. to fake glow:
- use particle effects (ParticleFX Gizmo) for sparkles/haze near emissive surfaces
- use fog via Environment Gizmo for atmospheric depth
- pair emissives with Dynamic Light Gizmos for actual light spread

### 6. max texture resolution is 4096x4096 (not 2048)

our CLAUDE.md says 2048x2048 max. the actual limit is **4096x4096** per Meta's docs. however, for Quest performance, **1024x1024 or smaller is strongly recommended** for most assets. 2048 is fine for hero surfaces (screen, stage).

### 7. no live video OR audio streaming for indie creators

this is the biggest gap for our use case:
- **video streaming**: the BLACKPINK/iHeartRadio concerts use Meta's internal production pipeline. there is **no public RTMP endpoint** for indie creators to stream from OBS/DJ setup.
- **audio streaming**: no Icecast/Shoutcast/WebRTC support in custom worlds.

**what IS available:**
- pre-recorded audio files up to 20 minutes (upload via Desktop Editor)
- Sound Recorder Gizmo (record from Quest mic)
- AI-generated ambient audio
- scripted audio playback sequences via TypeScript

**workaround for DJ sets:** pre-record 20-minute mix segments, upload them, and script sequential/looped playback. not live, but functional.

**for actual live streaming:** must work with Meta's creator program / Venues team directly. this is not self-serve.

---

## OPPORTUNITIES WE DIDN'T KNOW ABOUT

### 8. full TypeScript scripting system

horizon worlds has a complete TypeScript scripting system (not just visual blocks). this enables:
- **interactive DJ booth** — Custom UI Gizmo with buttons/sliders for track selection, volume, effects
- **animated lighting** — Dynamic Light Gizmos scripted for color cycling, beat-sync, triggers
- **color-animated entities** — cycle neon colors on meshes via setInterval()
- **trigger zones** — detect players entering dance floor, VIP, backstage
- **teleportation** — script player movement between zones
- **audio control** — play/stop/loop Sound Recorder Gizmos programmatically

this is a major opportunity for making the venue interactive.

### 9. dynamic lights exist and are scriptable

we assumed lighting was static. Dynamic Light Gizmos can be:
- toggled on/off via script
- color-changed at runtime
- intensity-animated
- triggered by events (button press, timer, player proximity)

**this means we can build a light show.** combine Dynamic Lights with color-animated entities for a responsive venue.

### 10. 100+ concurrent users (new Horizon Engine)

as of September 2025, the new Horizon Engine supports "well over 100" concurrent users per space (was ~20 previously). also 4x faster loading. this makes a club venue viable for real events.

### 11. members-only worlds for private testing

can publish a world as invite-only (up to 150 members, 25 concurrent). perfect for:
- testing before public launch
- private Primordial Groove events
- invite-only listening sessions

### 12. monetization is available

through the Meta Horizon Creator Program (MHCP):
- **paid admission**: $0.99–$9.99 per entry (Meta takes 30%)
- **in-world purchases**: virtual merch, accessories (Meta takes 25%)
- **tips**: $1–$20 from visitors
- **creator fund**: monthly bonuses from $50M fund based on engagement
- **requirement**: 1,000+ unique visits within 30 days to unlock monetization

### 13. particle effects and fog available

- **ParticleFX Gizmo**: smoke, sparks, fire, sparkles — scriptable
- **TrailFX Gizmo**: ribbon/trail effects on moving objects
- **Environment Gizmo fog**: distance-based fog with custom color
- no volumetric fog or volumetric lighting

### 14. spawn point gizmo with facing direction

the Spawn Point Gizmo controls exactly where players appear and which direction they face. supports multiple spawn points and randomization. our spawn marker mesh is correctly placed — just need to add the actual gizmo at the same position in Horizon.

### 15. community blender exporter addon

[Blender to Horizon Worlds Exporter](https://github.com/FairFight14/Blender-to-Horizon-Worlds-Exporter) automates:
- texture baking from Blender materials
- channel packing into _BR and _MEO format
- correct FBX export settings
- material suffix naming

worth investigating as it could save significant manual work.

---

## UPDATED PIPELINE (what we actually need to do)

### phase A: pre-import prep (in Blender, on Mac)
1. decide on texture strategy: bake textures or rely on Horizon editor tweaking
2. if baking: install community exporter addon, bake _BR and _MEO textures for each material
3. if not baking: accept flat default materials and plan to tweak in Horizon
4. verify FBX export settings (Apply All Transforms, FBX_SCALE_ALL)
5. export FBX + any PNG textures

### phase B: import + setup (on Windows)
1. install Meta Quest Link + Horizon Desktop Editor
2. create new blank world
3. import FBX + textures via "Add New > 3D Model"
4. verify scale and orientation (test with a single cube first)
5. recreate all 10 lights using Static + Dynamic Light Gizmos
6. set up Environment Gizmo (dark ambient, fog, custom skybox)
7. place Spawn Point Gizmo at our spawn marker location (y=3, facing stage)
8. add Trigger Zone Gizmos for dance floor / tier 1 / backstage

### phase C: interactivity (TypeScript in Desktop Editor)
1. upload pre-recorded audio tracks (20 min segments)
2. place Sound Recorder Gizmos at speaker positions (spatial audio)
3. build DJ booth UI (Custom UI Gizmo with track buttons + volume slider)
4. script Dynamic Light Gizmos for color cycling / beat response
5. script color-animated entities for emissive surfaces
6. add ParticleFX for fog/haze near stage

### phase D: test + publish
1. preview on desktop (no VR needed)
2. test in VR on Quest headset
3. publish as members-only (invite-only, up to 150 members)
4. run private test event
5. apply to Meta Horizon Creator Program
6. when ready: publish publicly
7. hit 1,000 visits/month → unlock monetization

---

## MATERIAL NAMING CORRECTIONS

our current material names use underscores before the suffix (e.g., `DarkConcrete_Metal`). Meta docs say to **avoid underscores in the name itself** — only use the underscore for the suffix.

**current (may have issues):**
```
DarkConcrete_Metal
DarkWall_Metal
OriginRing_Unlit
```

**should be:**
```
DarkConcrete_Metal     ← this is fine (one underscore for suffix)
ReliefGlow_Unlit       ← fine
FlowGuide_Unlit        ← fine
```

wait — actually our names only have ONE underscore (the suffix). the CamelCase before it is correct. **our naming is fine.** the rule is don't use multiple underscores like `Dark_Concrete_Floor_Metal`.

---

## FILING CABINET — key reference links

- [Getting Started with Custom Model Import](https://developers.meta.com/horizon-worlds/learn/documentation/custom-model-import/getting-started-with-custom-model-import)
- [Materials Guidance](https://developers.meta.com/horizon-worlds/learn/documentation/custom-model-import/creating-custom-models-for-horizon-worlds/materials-guidance-and-reference-for-custom-models)
- [Best Practices for Custom Models](https://developers.meta.com/horizon-worlds/learn/documentation/custom-model-import/creating-custom-models-for-horizon-worlds/best-practices)
- [Static Light Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/static-light-gizmo/)
- [Dynamic Light Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/dynamic-light-gizmo)
- [Environment Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/use-the-environment-gizmo/)
- [Sound Recorder Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/use-the-sound-recorder-gizmo/)
- [TypeScript in Horizon Worlds](https://developers.meta.com/horizon-worlds/learn/documentation/typescript/getting-started/using-typescript-in-horizon-worlds)
- [Custom UI Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/custom-ui-gizmo)
- [Spawn Point Gizmo](https://developers.meta.com/horizon-worlds/learn/documentation/code-blocks-and-gizmos/use-the-spawn-point-gizmo)
- [Publish Your World](https://developers.meta.com/horizon-worlds/learn/documentation/save-optimize-and-publish/publish-your-world)
- [Members-Only Worlds](https://developers.meta.com/horizon-worlds/learn/documentation/get-started/set-up-members-only-world)
- [MHCP Creator Program](https://developers.meta.com/horizon-worlds/programs)
- [Blender to Horizon Worlds Exporter](https://github.com/FairFight14/Blender-to-Horizon-Worlds-Exporter)
- [MHCP Community Creator Manual](https://github.com/MHCPCreators/horizonCreatorManual)
- [Performance Limits](https://developers.meta.com/horizon-worlds/learn/documentation/performance-best-practices-and-tooling/performance-limits-for-a-world)
- [World Capacity Dialog](https://developers.meta.com/horizon-worlds/learn/documentation/desktop-editor/getting-started/world-capacity)
