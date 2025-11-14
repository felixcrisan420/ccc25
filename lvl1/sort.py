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
    sort_bop("lvl1/level_1_a.in", "lvl1/level_1_a_sol.txt")
    #sort_bop("lvl1/level_2_a.in", "lvl1/level_2_a_sol.txt")
    #sort_bop("lvl1/level_3_a.in", "lvl1/level_3_a_sol.txt")
    #sort_bop("lvl1/level_4_a.in", "lvl1/level_4_a_sol.txt")
    #sort_bop("lvl1/level_5_a.in", "lvl1/level_5_a_sol.txt")
