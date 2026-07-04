# Breed portrait generation — prompt package

For running through ChatGPT or Gemini's image generation. Produces 60 images: 10 breeds × 6 variants each, so the same breed never looks identical twice on repeat matches.

You don't need a separate JSON manifest — the file naming convention below *is* the manifest. The app reads it directly.

---

## 1. Style guide — paste once, reuse for every image

If your tool supports a standing system instruction or "remember this for the rest of the conversation" setup, paste this once at the start. Otherwise, prepend it to every individual prompt.

```
Modern naturalist field-guide illustration style: flat color blocks, clean
confident linework, minimal shading. Limited, muted color palette anchored
on dusty teal and warm amber/tan tones plus warm neutral grays — avoid
saturated or cartoonish colors. Single animal, centered in frame, portrait
orientation (4:5 aspect ratio, taller than wide). Head-and-shoulders crop,
facing camera, similar scale and zoom across the whole series. Soft,
uncluttered, single-tone or very subtly textured background — no busy
scenes, no props. Confident, warm, slightly playful character expression
— not cartoonish, not photorealistic. No text, no logos, no watermarks,
no border baked into the image.
```

---

## 2. Variant lines — 6 per breed

Each breed gets all 6 of these. They're the only thing that changes between variants — subject and style stay fixed.

| # | Pose | Lighting | Background |
|---|------|----------|------------|
| 1 | Front-facing | Soft morning light | Warm terracotta |
| 2 | Slight 3/4 turn left | Warm afternoon light | Cool sage-green |
| 3 | Slight 3/4 turn right | Even overcast light | Warm gray |
| 4 | Front-facing | Warm afternoon light | Cool teal-gray |
| 5 | Slight 3/4 turn left | Soft diffused light | Neutral cream |
| 6 | Slight 3/4 turn right | Soft morning light | Warm amber-gray |

---

## 3. How to assemble one prompt

**[Style guide]** + **[breed's subject block, below]** + **[one variant line, written as a sentence]**

Worked example — Maine Coon, variant 1:

> Modern naturalist field-guide illustration style: flat color blocks, clean confident linework, minimal shading. Limited, muted color palette anchored on dusty teal and warm amber/tan tones plus warm neutral grays — avoid saturated or cartoonish colors. Single animal, centered in frame, portrait orientation (4:5 aspect ratio). Head-and-shoulders crop, facing camera, soft uncluttered background, no props, no text, no watermarks, no border. Confident, warm, slightly playful expression — not cartoonish, not photorealistic.
>
> A Maine Coon with strikingly large, expressive round eyes — emphasize the oversized eyes as the standout feature, broad jaw.
>
> Pose and lighting: front-facing, soft morning light, warm terracotta background.

Most image tools generate one image per request, so you'll run this 6 times per breed (60 total), swapping in the next variant line each time. If your tool can produce a multi-image set in one go, even better — just feed it all 6 variant lines at once for a given breed.

---

## 4. Subject blocks — all 10 breeds

Each emphasizes the exact trait the app's scoring engine actually measures for that breed, so the art stays honest to what the algorithm is doing.

**french_bulldog** — French Bulldog, dog
> A French Bulldog with a distinctly short, flat muzzle and a moderately broad, round face — emphasize the compressed brachycephalic snout as the standout feature.

**labrador_retriever** — Labrador Retriever, dog
> A Labrador Retriever with a notably wide, sturdy jaw — emphasize the broad jawline as the standout feature, friendly open expression.

**golden_retriever** — Golden Retriever, dog
> A Golden Retriever with an especially wide, warm smiling mouth — emphasize the broad mouth and gentle upward eye tilt as standout features.

**german_shepherd** — German Shepherd, dog
> A German Shepherd with a notably narrow, elongated face — emphasize the long lupine muzzle and alert eyes as standout features.

**dachshund** — Dachshund, dog
> A Dachshund with an unusually long, elongated snout — emphasize the long nose as the standout feature, narrow face.

**maine_coon** — Maine Coon, cat
> A Maine Coon with strikingly large, expressive round eyes — emphasize the oversized eyes as the standout feature, broad jaw.

**ragdoll** — Ragdoll, cat
> A Ragdoll with a gentle, sleepy downward eye tilt — emphasize the soft downward-angled large eyes as the standout feature.

**exotic_shorthair** — Exotic Shorthair, cat
> An Exotic Shorthair with an unusually round, flat face — emphasize the round brachycephalic face and flattened nose as standout features.

**devon_rex** — Devon Rex, cat
> A Devon Rex with a distinctive upturned, elfin eye tilt — emphasize the upward-angled large eyes and dramatic forehead-to-jaw taper as standout features.

**abyssinian** — Abyssinian, cat
> An Abyssinian with a narrow, fine-boned nose — emphasize the slender refined nose and narrow jaw as standout features, alert expression.

---

## 5. Technical specs

- **Aspect ratio:** 4:5 portrait (e.g. 1024×1280). Close is fine — the app crops with `object-fit: cover`, so minor deviation won't break anything.
- **Format:** JPG. No transparency needed since every shot has a solid/textured background.

---

## 6. File naming — exact, this is what the app reads

```
{breed_id}_{variant_number}.jpg
```

Breed ids (must match exactly — lowercase, underscores, no spaces):

```
french_bulldog, labrador_retriever, golden_retriever, german_shepherd,
dachshund, maine_coon, ragdoll, exotic_shorthair, devon_rex, abyssinian
```

Example: `maine_coon_1.jpg` through `maine_coon_6.jpg`, `french_bulldog_1.jpg` through `french_bulldog_6.jpg`, and so on for all 10 — 60 files total.

---

## 7. When you're done

Put all 60 files in a folder named `images`, placed directly next to `face-to-creature-matcher.html` (same folder level, not inside a subfolder of subfolders). Then let me know and I'll wire up the code to pick a random variant from that folder every time someone matches to that breed, so the same breed never looks identical twice in a row.

I'm holding off on touching `BREED_IMAGE_URLS` until those files actually exist — no point pointing the app at images that aren't there yet.
