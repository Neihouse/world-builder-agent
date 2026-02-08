# build notes — primordial groove origin world

## status
**rebuild complete** — research-informed layout, all 3 phases integrated

---

## revision history
- **v1** — initial 3-phase build (20x15m room, 4m ceiling, 0.6m stage)
- **v2 (current)** — full rebuild after VR venue research (20x20m room, 7m ceiling, 1.5m stage, entry corridor, tiered dance floor, video-ready screen)

---

## room layout

```
y = +10  ┌──── front entrance ────┐
         │    entry corridor      │  6m wide, 3.5m ceiling
y = +5   │    (reveal moment)     │
         ├────────────────────────┤
         │                        │  20m wide, 7m ceiling
         │    spawn marker (y=3)  │
         │                        │
y = 0    │    origin focal        │
         │                        │
         │    tier 1 (y=-2.7)     │
y = -4.7 ├── stage front edge ────┤
         │    DJ booth (y=-7.7)   │  10m wide, 1.5m elevated
         │    screen (y=-9.5)     │  9m x 4.5m (video-ready)
y = -10  └──── back wall ─────────┘
```

### key dimensions (changed from v1)
| dimension | v1 | v2 | reason |
|---|---|---|---|
| room depth | 15m | 20m (15m main + 5m corridor) | entry corridor builds anticipation |
| ceiling height | 4m | 7m | VR vertical presence, concert-scale feel |
| stage height | 0.6m | 1.5m | VR sightlines — avatars need clear view of performer |
| stage width | 6m | 10m | larger screen, wider presence |
| screen size | 3m x 3m backdrop | 9m x 4.5m screen | video-ready for Meta creator program |
| columns per side | 6 | 7 | taller columns fill 7m height |

---

## shell

### elements
- [x] floor — 20m x 20m plane (full length including corridor)
- [x] walls — back wall, left wall, right wall (full 20m), front wall sections flanking corridor
- [x] entry corridor walls — 6m wide, 5m deep, narrower than main room
- [x] ceiling main — flat plane at 7m
- [x] ceiling entry — lower plane at 3.5m (creates reveal moment entering main room)

### design decisions
- entry corridor at 3.5m ceiling → 7m main room creates dramatic vertical reveal
- corridor is 6m wide (vs 20m main room) — funnels audience toward origin
- back wall houses stage, screen, and frame — single visual anchor

---

## stage

### elements
- [x] stage platform — 10m x 5m, 1.5m elevation
- [x] stage edge — thin lip strip at front for visual definition
- [x] DJ booth desk — 4.5m x 1m x 1.1m, centered on stage
- [x] stage screen — 9m x 4.5m, against back wall behind DJ (video-ready surface)

### design decisions
- 1.5m stage height based on VR venue research — ensures clear sightlines from ground level
- screen positioned behind DJ (y=-9.5) against back wall — performer silhouettes against content
- screen is emissive (Screen_Unlit) — acts as video surface for Meta creator program integration
- DJ booth offset toward front of stage — allows space behind for screen visibility

---

## dance floor

### elements
- [x] front-row tier — 12m x 3m raised platform (0.2m), closest to stage
- [x] origin focal octagon — 3.5m radius disc at room center (y=0)
- [x] origin ring — outer emissive ring (3.8m radius)
- [x] spawn marker — 1m radius disc at y=3, facing stage (7m from stage edge)

### design decisions
- spawn point at y=3 — avatars enter facing stage, ~7m away (VR-researched distance)
- tier 1 gives front-row elevation — slight 0.2m raise differentiates zones
- origin focal unchanged from v1 — octagonal language is core identity
- ~4 sqm per avatar spacing assumed for crowd layout

---

## identity

### elements
- [x] wall columns — 7 per side (14 total), hexagonal tapered (6.5m tall), merged per side
- [x] stage frame / proscenium — pillars + lintel framing the screen (no chevron)
- [x] backdrop relief — concentric octagonal rings + radiating bars on screen surface
- [x] sculptural totems — 2 symmetrical monoliths flanking screen (hex base + oct mid + icosphere cap)
- [x] ceiling beams — 6 cross-beams spanning main room
- [x] floor flow guides — 6 emissive strips (entry-to-origin, origin-to-stage, 4 radial)

### design decisions
- columns taller (6.5m vs ~3.5m) for 7m ceiling — maintain proportions
- stage frame simplified — chevron removed per user feedback, clean pillar+lintel arch
- relief centered on screen surface — visible focal even when no video content
- totems moved behind DJ (was incorrectly at front of stage in v1)
- 6 beams (was 5) — taller room benefits from more rhythm
- flow guides use same octagonal radial language as origin

---

## lighting

| light | energy | color | position | purpose |
|---|---|---|---|---|
| Light_Stage | 1200 | warm (1.0, 0.8, 0.6) | above stage | primary DJ illumination |
| Light_ScreenWash | 200 | dark purple (0.3, 0.15, 0.5) | behind screen | screen backwash / depth |
| Light_Origin | 500 | cool blue (0.5, 0.6, 1.0) | above origin | dance floor focal |
| Light_Fill | 80 | muted purple (0.4, 0.35, 0.5) | mid-room | ambient floor wash |
| Light_Left | 250 | deep purple (0.6, 0.25, 0.9) | left high | left accent |
| Light_Right | 250 | deep purple (0.6, 0.25, 0.9) | right high | right accent |
| Light_ColWash_L | 100 | warm (0.9, 0.6, 0.4) | left low | column graze uplight |
| Light_ColWash_R | 100 | warm (0.9, 0.6, 0.4) | right low | column graze uplight |
| Light_Entry | 60 | warm (0.8, 0.6, 0.5) | corridor | subtle entry guide |
| Light_Tier1 | 150 | purple (0.5, 0.4, 0.8) | above tier 1 | front-row dance wash |

### lighting changes from v1
- stage light boosted (800 → 1200) for taller room
- origin light boosted (400 → 500)
- added Light_ScreenWash — new screen needs backlight depth
- added Light_Entry — corridor needs subtle guide light
- added Light_Tier1 — new tier zone needs dedicated wash
- column wash lights raised (1m → 1.5m) for taller columns
- total: 8 → 10 lights

---

## materials (18 unique)

| material | base color | roughness | metallic | emission |
|---|---|---|---|---|
| DarkConcrete_Metal | (0.055, 0.05, 0.06) | 0.88 | 0.05 | — |
| DarkWall_Metal | (0.025, 0.025, 0.035) | 0.95 | 0.0 | — |
| DarkCeiling_Metal | (0.015, 0.015, 0.018) | 0.98 | 0.0 | — |
| StageSurface_Metal | (0.09, 0.07, 0.1) | 0.5 | 0.4 | — |
| StageEdge_Metal | (0.04, 0.03, 0.05) | 0.3 | 0.85 | — |
| BoothMetal_Metal | (0.035, 0.035, 0.045) | 0.3 | 0.9 | — |
| Screen_Unlit | (0.08, 0.04, 0.12) | 0.5 | 0.0 | str 2.5 |
| OriginSurface_Metal | (0.04, 0.04, 0.055) | 0.4 | 0.6 | — |
| OriginRing_Unlit | (0.18, 0.1, 0.3) | 0.5 | 0.0 | str 5.0 |
| SpawnMarker_Unlit | (0.06, 0.08, 0.12) | 0.5 | 0.0 | str 1.5 |
| ColumnStone_Metal | (0.065, 0.055, 0.075) | 0.7 | 0.25 | — |
| FrameMetal_Metal | (0.03, 0.025, 0.04) | 0.25 | 0.95 | — |
| ReliefGlow_Unlit | (0.14, 0.07, 0.22) | 0.5 | 0.0 | str 5.0 |
| TotemStone_Metal | (0.055, 0.045, 0.065) | 0.55 | 0.45 | — |
| BeamConcrete_Metal | (0.035, 0.035, 0.04) | 0.85 | 0.1 | — |
| FlowGuide_Unlit | (0.08, 0.06, 0.12) | 0.5 | 0.0 | str 2.0 |
| Tier1_Metal | (0.045, 0.04, 0.055) | 0.7 | 0.3 | — |
| EntryCeiling_Metal | (0.02, 0.02, 0.025) | 0.95 | 0.0 | — |

---

## geometry summary

| object | polys | tris | material |
|---|---|---|---|
| Floor | 1 | 2 | DarkConcrete_Metal |
| Wall_Back | 6 | 12 | DarkWall_Metal |
| Wall_Left | 6 | 12 | DarkWall_Metal |
| Wall_Right | 6 | 12 | DarkWall_Metal |
| Wall_Front_L | 6 | 12 | DarkWall_Metal |
| Wall_Front_R | 6 | 12 | DarkWall_Metal |
| Wall_Entry_L | 6 | 12 | DarkWall_Metal |
| Wall_Entry_R | 6 | 12 | DarkWall_Metal |
| Ceiling_Main | 1 | 2 | DarkCeiling_Metal |
| Ceiling_Entry | 1 | 2 | EntryCeiling_Metal |
| Stage_Platform | 6 | 12 | StageSurface_Metal |
| Stage_Edge | 6 | 12 | StageEdge_Metal |
| DJ_Booth | 6 | 12 | BoothMetal_Metal |
| Stage_Screen | 6 | 12 | Screen_Unlit |
| DanceFloor_Tier1 | 6 | 12 | Tier1_Metal |
| Origin_Focal | 10 | 24 | OriginSurface_Metal |
| Origin_Ring | 10 | 24 | OriginRing_Unlit |
| Spawn_Marker | 10 | 24 | SpawnMarker_Unlit |
| Columns_L | 56 | 126 | ColumnStone_Metal |
| Columns_R | 56 | 126 | ColumnStone_Metal |
| Stage_Frame | 18 | 36 | FrameMetal_Metal |
| Totem_L | 38 | 68 | TotemStone_Metal |
| Totem_R | 38 | 68 | TotemStone_Metal |
| Backdrop_Relief | 64 | 160 | ReliefGlow_Unlit |
| Ceiling_Beams | 36 | 72 | BeamConcrete_Metal |
| Floor_FlowGuides | 36 | 72 | FlowGuide_Unlit |
| **total** | **447** | **990** | **18 unique** |

### budget check
| metric | used | limit | headroom |
|---|---|---|---|
| polys per object (max) | 64 | 50,000 | 99.9% |
| total tris | 990 | — | extreme headroom |
| materials per object | 1 | 2 | 50% |
| total materials | 18 | — | ok |
| lights | 10 | — | ok |
| meshes | 26 | — | ok |
| file size | 146 kb | 6 gb | 99.99% |

---

## research-informed decisions

based on VR venue design research (Horizon Worlds, VRChat, spatial design papers):

- **ceiling height 7m** — VR sense of vertical presence requires taller spaces than real-world clubs; Meta's Music Valley uses large-scale environments
- **stage elevation 1.5m** — avatar eye height ~1.6m means a 0.6m stage puts performer at chest level; 1.5m puts them clearly above crowd
- **entry corridor** — funneling from 6m-wide / 3.5m-tall corridor into 20m-wide / 7m-tall room creates a reveal moment; common pattern in VR venue design
- **spawn point 7m from stage** — research suggests 5-8m for good VR viewing distance; too close breaks scale, too far loses intimacy
- **video screen vs backdrop** — no video livestreaming available to Horizon Worlds creators (first-party Meta feature only); screen is built video-ready for Meta creator program access
- **front-row tier** — slight elevation differentiates zones without blocking sightlines; real-world concert VIP pit concept

---

## known limitations
- no video streaming currently — requires Meta creator program partnership
- no audience seating — standing-only venue per nightclub concept
- no textures — procedural materials only (could add in future iteration)
- no audio integration — Sound Recorder Gizmo supports up to 20 min loops
- no scripting/interactivity — static geometry only (Horizon handles scripting in-world)
- spawn marker is visual only — actual spawn points set in Horizon Worlds editor

---

## exports
- `world/fbx/pg_origin_club_final.fbx` — 146 kb (rebuild deliverable)
- `world/pg_origin_club.blend` — source file
