# build notes — primordial groove origin world

## status
**build complete** — all 3 phases finished

---

## phase 1 — functional club shell
**objective:** usable world fast — **complete**

### elements
- [x] floor — 20m x 15m plane, dark concrete
- [x] walls — 4 walls, 0.3m thick, 4m height
- [x] ceiling — flat plane at 4m
- [x] stage / dj booth — 6m x 4m raised platform (0.6m), booth desk, backdrop panel
- [x] origin focal area — octagonal disc (r=3m) with outer ring (r=3.3m)

### design decisions
- room dimensions: 20m x 15m x 4m — sized for ~30-40 avatars comfortably
- stage at back wall (negative y) — natural crowd flow toward it
- origin focal octagon centered in room — anchors the dance floor
- backdrop panel behind dj — future identity surface
- all materials use horizon worlds suffix naming convention

---

## phase 2 — identity pass
**objective:** primordial groove presence — **complete**

### elements
- [x] rhythmic wall columns — 6 per side (12 total), hexagonal tapered, merged per side
- [x] stage frame / proscenium — angular gateway with pillars, lintel, and inverted chevron
- [x] backdrop relief — concentric octagonal rings with radiating bars, emissive
- [x] sculptural totems — 2 symmetrical monoliths flanking stage (hex base + octagonal mid + icosphere cap)

### design decisions
- columns use hexagonal cross-section (6 verts) — minimal but distinct from walls
- columns merged into 2 meshes (left/right) — reduces draw calls
- stage frame creates visual hierarchy — marks the performance zone
- inverted chevron on lintel points downward — draws eye to dj
- backdrop relief uses concentric octagons — ripple/sound wave motif
- relief is emissive (ReliefGlow_Unlit) — visible focal point even in dim lighting
- totems are stacked primitives — primordial monolith aesthetic
- totems placed outside stage frame — flanking sentinels
- all identity elements are abstract, non-text — implicit branding per spec
- symmetry enforced throughout — left/right mirroring

---

## phase 3 — atmosphere pass
**objective:** immersion without performance loss — **complete**

### elements
- [x] lighting refinement — reworked 5 existing lights, added 3 new (8 total)
- [x] material polish — tuned roughness/metallic/emission across all 14 materials
- [x] spatial flow guides — 6 emissive floor strips radiating from origin
- [x] ceiling beams — 5 cross-beams for underground bunker depth

### lighting changes
| light | energy | color | purpose |
|---|---|---|---|
| Light_Stage | 800 | warm (1.0, 0.8, 0.6) | primary dj illumination |
| Light_Origin | 400 | cool blue (0.5, 0.6, 1.0) | dance floor focal |
| Light_Fill | 60 | muted purple (0.4, 0.35, 0.5) | ambient floor wash |
| Light_Left | 200 | deep purple (0.6, 0.25, 0.9) | left accent |
| Light_Right | 200 | deep purple (0.6, 0.25, 0.9) | right accent |
| Light_ColWash_L | 80 | warm (0.9, 0.6, 0.4) | left column graze |
| Light_ColWash_R | 80 | warm (0.9, 0.6, 0.4) | right column graze |
| Light_StageBack | 120 | dark purple (0.3, 0.15, 0.5) | silhouette depth |

### material polish summary
- floor: wet concrete look (IOR 1.45, roughness 0.88)
- walls: cooler, more absorbent (roughness 0.95)
- ceiling: near-black (roughness 0.98)
- booth: polished dark metal (roughness 0.3, metallic 0.9)
- frame: mirror-dark metal (roughness 0.25, metallic 0.95)
- emissives boosted: origin ring + relief glow at strength 5.0
- flow guides: subtle emissive (strength 2.0)

### design decisions
- warm/cool contrast: stage warm, origin cool, sides purple
- column wash lights low (1m) for dramatic uplight graze
- stage backlight creates silhouette depth behind dj
- fill light intentionally dim — darkness is the atmosphere
- flow guides use same octagonal language as origin (radial at 45deg)
- ceiling beams evenly spaced — reinforce rhythmic column motif
- 2 orphan materials cleaned up during export

### forbidden items (per spec) — confirmed absent
- no particle effects
- no heavy emissive materials (max emission strength = 5.0, used sparingly)
- no complex lighting rigs (8 point lights only)

---

## final geometry summary

| object | polys | tris | materials |
|---|---|---|---|
| Floor | 1 | 2 | DarkConcrete_Metal |
| Wall_Back | 6 | 12 | DarkWall_Metal |
| Wall_Front | 6 | 12 | DarkWall_Metal |
| Wall_Left | 6 | 12 | DarkWall_Metal |
| Wall_Right | 6 | 12 | DarkWall_Metal |
| Ceiling | 1 | 2 | DarkCeiling_Metal |
| Stage_Platform | 6 | 12 | StageSurface_Metal |
| DJ_Booth | 6 | 12 | BoothMetal_Metal |
| Stage_Backdrop | 6 | 12 | Backdrop_Unlit |
| Origin_Focal | 10 | 28 | OriginSurface_Metal |
| Origin_Ring | 10 | 28 | OriginRing_Unlit |
| Columns_Left | 48 | 120 | ColumnStone_Metal |
| Columns_Right | 48 | 120 | ColumnStone_Metal |
| Stage_Frame | 23 | 42 | FrameMetal_Metal |
| Backdrop_Relief | 64 | 160 | ReliefGlow_Unlit |
| Totem_L | 38 | 68 | TotemStone_Metal |
| Totem_R | 38 | 68 | TotemStone_Metal |
| Floor_FlowGuides | 36 | 72 | FlowGuide_Unlit |
| Ceiling_Beams | 30 | 60 | BeamConcrete_Metal |
| **total** | **389** | **854** | **14 unique** |

### budget check
| metric | used | limit | headroom |
|---|---|---|---|
| polys per object (max) | 64 | 50,000 | 99.9% |
| total tris | 854 | — | extreme headroom |
| materials per object | 1 | 2 | 50% |
| total materials | 14 | — | ok |
| lights | 8 | — | ok |
| meshes | 19 | — | ok |
| file size | 108.8 kb | 6 gb | 99.99% |

---

## known limitations
- no entry/exit markers — horizon worlds handles spawn points
- no audience seating or bar area — intentionally minimal
- no textures — procedural materials only (could add in future iteration)
- no audio integration — out of scope per agents.md
- columns are uniform height — could vary in future iteration

---

## exports
- `world/fbx/pg_origin_club_phase1.fbx` — 68.7 kb (phase 1 snapshot)
- `world/fbx/pg_origin_club_phase2.fbx` — 97.3 kb (phase 2 snapshot)
- `world/fbx/pg_origin_club_phase3.fbx` — 108.8 kb (phase 3 snapshot)
- `world/fbx/pg_origin_club_final.fbx` — 108.8 kb (final deliverable)
- `world/pg_origin_club.blend` — source file
