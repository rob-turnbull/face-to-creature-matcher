# Morphing Phase Spec — Face-to-Creature Matcher

**Status:** Draft v1.0 — 2026-07-07 **Owner:** Rob Turnbull **Purpose of this document:** Complete build spec for the landmark-based morph feature. Written so any agent or developer can resume work from this file alone. Update the Status Log at the bottom whenever work stops.


## 1. Goal

Given a user's face (already captured via MediaPipe Face Mesh in the app) and their matched breed portrait, render a geometric morph between the two — the user's facial features migrate toward the breed's feature positions while the images cross-dissolve. Controlled by a slider from 0 (fully human) to 1 (fully breed).

Non-goals for this phase: video export, morphing between two breeds, animated auto-play (nice-to-have, Phase M3).

## 2. Constraints

- **Client-side only.** No server, no uploads. Face data never leaves the browser. Same architecture as the rest of the app. 

- **Single-file friendly.** Morph engine ships inside `index.html` like everything else. No new runtime libraries. 

- **Existing assets:** `pet-dataset.json` v2.0.0 (50 breeds), `images/\{breed\_id\}\_1.jpg` through `\_6.jpg` (six portrait variants per breed, ~450–510 px wide). Variant 1 is the frontal pose on every sheet — the morph targets variant 1 only. 

## 3. The correspondence problem

MediaPipe provides 468 landmarks on the human face. Breed portraits have zero. There is no reliable client-side landmark model for stylized pet illustrations. Solution: define a small shared point schema, annotate each breed's variant-1 portrait once (auto-seeded, human-verified), and downsample the human's 468 MediaPipe points to the same schema at runtime.

## 4. Shared point schema (24 points)

Semantic correspondence, not anatomical. Cat ears map to the human upper-head region — this is what makes the morph read as "growing ears."

| **\#** | **ID** | **Description** | **MediaPipe index (human)** |
| :-: | :-: | :-: | :-: |
| 0 | left\_eye\_outer | outer corner, viewer's left eye | 33 |
| 1 | left\_eye\_inner | inner corner | 133 |
| 2 | left\_eye\_top | upper lid apex | 159 |
| 3 | left\_eye\_bottom | lower lid | 145 |
| 4 | right\_eye\_inner | inner corner | 362 |
| 5 | right\_eye\_outer | outer corner | 263 |
| 6 | right\_eye\_top | upper lid apex | 386 |
| 7 | right\_eye\_bottom | lower lid | 374 |
| 8 | nose\_bridge | between the eyes | 168 |
| 9 | nose\_tip | tip / nose leather center | 1 |
| 10 | nose\_left | left nostril / leather edge | 98 |
| 11 | nose\_right | right nostril / leather edge | 327 |
| 12 | mouth\_left | left mouth corner | 61 |
| 13 | mouth\_right | right mouth corner | 291 |
| 14 | mouth\_top | upper lip center / philtrum base | 0 |
| 15 | chin | chin tip / lower jaw center | 152 |
| 16 | jaw\_left | left jaw corner | 172 |
| 17 | jaw\_right | right jaw corner | 397 |
| 18 | cheek\_left | left face contour at eye level | 234 |
| 19 | cheek\_right | right face contour at eye level | 454 |
| 20 | ear\_left\_base | left ear base / human temple | 54 |
| 21 | ear\_left\_tip | left ear tip / human upper-forehead-left | 103 |
| 22 | ear\_right\_base | right ear base / right temple | 284 |
| 23 | ear\_right\_tip | right ear tip / upper-forehead-right | 332 |

Plus 8 fixed boundary points at canvas corners and edge midpoints (identical in both point sets) so the triangulation covers the full frame. Total mesh: 32 points.

**Triangulation is precomputed and hardcoded.** Because the point set is fixed, run Delaunay once offline on a reference layout and ship the triangle index list as a constant (~50 triangles). No Delaunay code ships to the client. If a user's extreme geometry produces a flipped (negative-area) triangle, render it anyway — artifacts at slider extremes are acceptable for v1.

## 5. Data format — `pet-landmarks.json`

```
`\{`

`  "version": "1.0.0",`

`  "schema": \["left\_eye\_outer", "left\_eye\_inner", "..."\],`

`  "breeds": \{`

`    "bengal": \{`

`      "image": "images/bengal\_1.jpg",`

`      "width": 482, "height": 542,`

`      "points": \[\[x0,y0\], \[x1,y1\], "... 24 pairs, pixel coords"\],`

`      "verified": true`

`    \}`

`  \}`

`\}`
```

`verified` flips to true only after a human has reviewed the points in the annotator. The app skips morphing for unverified breeds (falls back to plain portrait display).

## 6. Components

### 6.1 `seed\_landmarks.py` (offline, one-time)

Auto-generates first-pass points for all 50 variant-1 crops.

- **Geometric prior:** template point layout scaled to image dimensions. Portraits are same-style frontal compositions, so a template lands within ~10–15%. 

- **CV refinement:** eyes are high-saturation green/gold blobs against fur — detect via HSV threshold + blob centroid, snap the 8 eye points. Nose leather is a dark or pink center-line blob — snap points 8–11. Ear tips: topmost silhouette peaks left/right of center. 

- Output: `pet-landmarks.json` with all `verified: false`. 

- Dependencies: Pillow + numpy only (matches slicer.py environment). 

### 6.2 `landmark-annotator.html` (offline tool, style of landmark-validator.html)

- Loads `pet-landmarks.json` + portrait, draws draggable numbered points over the image. 

- Breed dropdown, prev/next, point snapping, zoom. 

- "Mark verified" checkbox per breed; "Export JSON" button downloads the updated file. 

- Keyboard: arrows nudge selected point 1px, shift+arrows 5px. 

### 6.3 Morph engine (JS, into `index.html`)

Standard Beier-free triangle morph:

1. Normalize: compute similarity transform (scale + translate) aligning the user's eye midpoint and inter-eye distance to the portrait's, on a shared square canvas (512×512). 

2. For slider value `t`: intermediate points `P\[i\] = (1-t)·human\[i\] + t·breed\[i\]`. 

3. Warp both images to P triangle-by-triangle: for each triangle, `ctx.save()`, clip to destination triangle path, `setTransform()` with the affine map from source triangle, `drawImage()`, `ctx.restore()`. 

4. Composite: draw warped human at alpha `(1-t)`, warped breed at alpha `t`. 

5. Render on `input` event from the slider — full redraw per frame is fine at 32 points / ~50 triangles. 

### 6.4 UI

- Morph panel on the result card, shown only when the matched breed is `verified` in pet-landmarks.json. 

- Slider 0–100, default 50. Label ends: "You" / breed display name. 

- "Save image" button — `canvas.toDataURL` download of the current frame. 

## 7. Phase plan

| **Phase** | **Scope** | **Definition of done** |
| :-: | :-: | :-: |
| **M1** | Schema locked, seeder run, annotator built, **one breed** (bengal) hand-verified, morph engine rendering user↔bengal with slider | Live morph works end-to-end for one breed on the deployed app |
| **M2** | Annotate/verify remaining 49 breeds in the annotator | All breeds `verified: true` |
| **M3** | Polish: save-image button, auto-play toggle, mobile touch QA | Optional |

M1 is the architecture; M2 is pure data entry that any session can resume. If time runs out mid-M1, the Status Log below says exactly where.

## 8. Risks / known issues

- Ear-tip correspondence is the most artistic-judgment-heavy mapping; expect to tune points 20–23 by eye during M1. 

- Profile-pose user photos will morph poorly — the schema assumes near-frontal capture, same as the matcher itself. No mitigation needed; the app already coaches frontal capture. 

- JPEG portraits have no alpha; background color blends into the morph. Acceptable for v1 — the portraits' flat backgrounds actually dissolve cleanly. 

## 9. Status log

| **Date** | **State** | **Next action** |
| :-: | :-: | :-: |
| 2026-07-07 | Spec drafted. No code yet. | Build seed\_landmarks.py |

