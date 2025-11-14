def sort_bop(input_file: str, output_file: str):
    data = []

    # Read and parse CSV (skip header)
    with open(input_file, "r") as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            bop = int(parts[0])
            temp = float(parts[1])
            hum = float(parts[2])
            data.append((bop, temp, hum))

    # Sort: temp desc, hum asc, bop asc
    data.sort(key=lambda x: (-x[1], x[2], x[0]))

    # Extract sorted BOP IDs
    result = " ".join(str(row[0]) for row in data)

    # Write output
    with open(output_file, "w") as f:
        f.write(result)


# Example usage
if __name__ == "__main__":
    sort_bop("ccc25/lvl1/in/level_1_a.in", "ccc25/lvl1/out/level_1_a_sol.txt")
    sort_bop("ccc25/lvl1/in/level_1_b.in", "ccc25/lvl1/out/level_1_b_sol.txt")
    sort_bop("ccc25/lvl1/in/level_1_c.in", "ccc25/lvl1/out/level_1_c_sol.txt")
    sort_bop("ccc25/lvl1/in/level_1_d.in", "ccc25/lvl1/out/level_1_d_sol.txt")
    sort_bop("ccc25/lvl1/in/level_1_e.in", "ccc25/lvl1/out/level_1_e_sol.txt")
