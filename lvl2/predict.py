import pandas as pd
import numpy as np
import csv

# Fixed beta values learned from level_2_a (the correct model)
FIXED_BETA = np.array([
    14.3473443,
    0.00191624761,
    -0.000335060104,
    -0.0212146002,
    1.70182237,
    0.00963225317
])


def load_and_fix_level1(path):
    lvl1 = pd.read_csv(path)
    mask_f = lvl1["Temperature [°C]"] > 60
    lvl1.loc[mask_f, "Temperature [°C]"] = ((lvl1.loc[mask_f, "Temperature [°C]"] - 32) * 5/9)
    return lvl1


def load_level2(path):
    return pd.read_csv(path)


def try_train_regression(data, feature_cols):
    mask_missing = data["Bird Love Score [<3]"] == "missing"
    known = data[~mask_missing].copy()

    if known.empty:
        # NO TRAINING POSSIBLE
        return FIXED_BETA

    known["Bird Love Score [<3]"] = known["Bird Love Score [<3]"].astype(float)
    X = known[feature_cols].values
    y = known["Bird Love Score [<3]"].values

    Xd = np.hstack([np.ones((X.shape[0], 1)), X])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    return beta


def predict_missing(data, beta, feature_cols):
    mask_missing = data["Bird Love Score [<3]"] == "missing"
    missing = data[mask_missing].copy()

    X = missing[feature_cols].values
    Xd = np.hstack([np.ones((X.shape[0], 1)), X])

    y_pred = Xd @ beta
    y_pred = np.clip(y_pred, 0, 100)

    missing["Bird Love Score [<3]"] = np.round(y_pred, 2)

    return missing[["BOP", "Bird Love Score [<3]"]].sort_values("BOP")


def solve(level1_path, level2_path, out_path):
    lvl1 = load_and_fix_level1(level1_path)
    lvl2 = load_level2(level2_path)

    data = lvl2.merge(lvl1, on="BOP", how="left")

    feature_cols = [
        "Vegetation [%]",
        "Insects [g/m²]",
        "Urban Light [%]",
        "Temperature [°C]",
        "Humidity [%]",
    ]

    # Try training. If no known targets → automatically use FIXED_BETA.
    beta = try_train_regression(data, feature_cols)

    out = predict_missing(data, beta, feature_cols)

    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["BOP", "Bird Love Score [<3]"])
        for _, r in out.iterrows():
            w.writerow([int(r["BOP"]), f"{r['Bird Love Score [<3]']:.2f}"])


# Usage:
solve("lvl2/in/all_data_from_level_1.in", "lvl2/in/level_2_c.in", "lvl2/out/level_2_c.out")
