import csv
from collections import defaultdict, Counter

# ---------- Species rules encoded ----------
SPECIES = [
    "Hurracurra Bird",
    "Medieval Bluetit",
    "Flanking Blackfinch",
    "Rusty Goldhammer",
    "Red Firefinch",
    "Sticky Wolfthroat"
]

def is_palindrome(path):
    return path == path[::-1]

def load_flocks(filename):
    flocks = defaultdict(list)
    with open(filename) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            fid = int(row[0])
            path = list(map(int, row[1].split()))
            flocks[fid].append(path)
    return flocks

# ----------------------------------------------------------
# Species identification logic
# ----------------------------------------------------------

def classify_flocks(flocks, temperatures):
    
    # --- Step 1: compute basic stats per flock ---
    info = {}
    
    for fid, paths in flocks.items():
        starts = {p[0] for p in paths}
        ends   = {p[-1] for p in paths}
        pal    = all(is_palindrome(p) for p in paths)
        same   = len({tuple(p) for p in paths}) == 1
        bops   = set(x for p in paths for x in p)
        
        # Compute average temperature along all routes
        temps = []
        for p in paths:
            for bop in p:
                if bop in temperatures:
                    temps.append(temperatures[bop])
        avg_temp = sum(temps) / len(temps) if temps else 0
        
        info[fid] = {
            "palindrome": pal,
            "all_same": same,
            "start_end_same": (len(starts)==1 and len(ends)==1 and starts == ends),
            "bops": bops,
            "avg_temp": avg_temp,
            "prefix": tuple(paths[0][: min(len(p) for p in paths)])
        }
    
    # ---------------------------------------------------
    # Step 2: Identify Medieval Bluetit (largest palindrome flock)
    # ---------------------------------------------------
    pal_flocks = [fid for fid,v in info.items() if v["palindrome"]]
    bluetit = max(pal_flocks, key=lambda f: len(info[f]["bops"]))
    
    # ---------------------------------------------------
    # Step 3: Identify Sticky Wolfthroat (palindrome subset of Bluetit)
    # ---------------------------------------------------
    wolf = None
    for fid in pal_flocks:
        if fid != bluetit and info[fid]["bops"].issubset(info[bluetit]["bops"]):
            wolf = fid
            break

    # ---------------------------------------------------
    # Step 4: Identify Flanking Blackfinch (identical loop, not palin)
    # ---------------------------------------------------
    blackfinch = None
    for fid, v in info.items():
        if fid not in (bluetit, wolf) and v["all_same"] and not v["palindrome"]:
            blackfinch = fid
            break

    # ---------------------------------------------------
    # Step 5: Identify Rusty Goldhammer
    # largest common prefix, non identical, non palindrome
    # ---------------------------------------------------
    gold = None
    max_prefix = -1
    for fid, v in info.items():
        if fid in (bluetit, wolf, blackfinch):
            continue
        if not v["all_same"] and not v["palindrome"]:
            plen = len(v["prefix"])
            if plen > max_prefix:
                max_prefix = plen
                gold = fid

    # ---------------------------------------------------
    # Step 6: Remaining two flocks → Firefinch vs Hurracurra by temperature
    # Hurracurra = hotter
    # ---------------------------------------------------
    remaining = [fid for fid in flocks if fid not in (bluetit, wolf, blackfinch, gold)]
    f1, f2 = remaining

    if info[f1]["avg_temp"] > info[f2]["avg_temp"]:
        hurr = f1
        fire = f2
    else:
        hurr = f2
        fire = f1

    # ---------------------------------------------------
    # Final mapping
    # ---------------------------------------------------
    result = {
        bluetit: "Medieval Bluetit",
        wolf: "Sticky Wolfthroat",
        blackfinch: "Flanking Blackfinch",
        gold: "Rusty Goldhammer",
        hurr: "Hurracurra Bird",
        fire: "Red Firefinch"
    }

    return result


# ----------------------------------------------------------
# Helper to run classification for any level_3_X.in
# ----------------------------------------------------------

def solve_level3(input_file, temperature_file, output_file):
    flocks = load_flocks(input_file)
    
    # load temperatures
    temperatures = {}
    with open(temperature_file) as f:
        r = csv.reader(f)
        next(r)
        for bop, temp, _ in r:
            temperatures[int(bop)] = float(temp)
    
    result = classify_flocks(flocks, temperatures)

    # write CSV output
    with open(output_file, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Flock ID", "Species"])
        for fid in sorted(result):
            w.writerow([fid, result[fid]])

    print(f"Saved: {output_file}")


# ----------------------------------------------------------
# Example usage:
solve_level3("lvl3/in/level_3_a.in", "lvl3/in/all_data_from_level_1.in", "lvl3/out/level_3_a_test.out")
solve_level3("lvl3/in/level_3_b.in", "lvl3/in/all_data_from_level_1.in", "lvl3/out/level_3_b_test.out")
solve_level3("lvl3/in/level_3_c.in", "lvl3/in/all_data_from_level_1.in", "lvl3/out/level_3_c_test.out")
# ----------------------------------------------------------