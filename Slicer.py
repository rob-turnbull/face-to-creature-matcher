from PIL import Image
import numpy as np, os

def find_cut(arr, axis, expected, window=25):
    h, w = arr.shape[:2]
    scores = []
    if axis == 'col':
        for x in range(max(1, expected-window), min(w-1, expected+window+1)):
            diffs = np.abs(arr[:, x].astype(float) - arr[:, x-1].astype(float)).mean(axis=1)
            scores.append(((diffs > diffs.mean()*1.2).mean(), x))
    else:
        for y in range(max(1, expected-window), min(h-1, expected+window+1)):
            diffs = np.abs(arr[y].astype(float) - arr[y-1].astype(float)).mean(axis=1)
            scores.append(((diffs > diffs.mean()*1.2).mean(), y))
    return sorted(scores, reverse=True)[0][1]

def find_band(sat, center, window=15, thresh=45):
    start, end = center, center
    for i in range(center, max(0, center-window), -1):
        if sat[i] < thresh: start = i
        else: break
    for i in range(center, min(len(sat)-1, center+window)):
        if sat[i] < thresh: end = i
        else: break
    return start, end

def slice_sheet(path, breed_id):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    arr = np.array(img)
    col_sat = (arr.max(axis=2) - arr.min(axis=2)).mean(axis=0)
    row_sat = (arr.max(axis=2) - arr.min(axis=2)).mean(axis=1)
    c1 = find_cut(arr,'col',w//3); c2 = find_cut(arr,'col',2*w//3); r1 = find_cut(arr,'row',h//2)
    c1b = find_band(col_sat,c1); c2b = find_band(col_sat,c2); r1b = find_band(row_sat,r1)
    col_bounds = [(0,c1b[0]-1),(c1b[1]+1,c2b[0]-1),(c2b[1]+1,w-1)]
    row_bounds = [(0,r1b[0]-1),(r1b[1]+1,h-1)]
    os.makedirs("/mnt/user-data/outputs/images", exist_ok=True)
    v = 1
    for ry0,ry1 in row_bounds:
        for cx0,cx1 in col_bounds:
            img.crop((cx0,ry0,cx1+1,ry1+1)).save(
                f"/mnt/user-data/outputs/images/{breed_id}_{v}.jpg","JPEG",quality=92)
            v += 1
    print(f"{breed_id}: done")