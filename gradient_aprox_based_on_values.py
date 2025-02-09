import csv
import math
import os
import statistics

def generate_pairwise_calc(input_file):
    """
    Reads a CSV file (skipping header) where:
      - First column = time (t)
      - Last  column = H(t)

    For every pair (t_i, H_i), (t_j, H_j) with i < j, computes:
      val_ij = [-ln(H_i) + ln(H_j)] / (t_j - t_i)
             =  (ln(H_j) - ln(H_i)) / (t_j - t_i)

    Writes out a new CSV that includes [t_i, H_i, t_j, H_j, val_ij] for
    each pair, plus the overall average and median of val_ij.
    """
    t_points = []
    h_points = []

    # --- 1) Read the input CSV ---
    with open(input_file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        for row in reader:
            if not row:  # skip empty rows
                continue
            try:
                t = float(row[0])      # time
                H = float(row[-1])     # height
                t_points.append(t)
                h_points.append(H)
            except (ValueError, IndexError):
                # skip rows that can't be parsed
                continue

    # If we have fewer than 2 data points, there's nothing to do
    if len(t_points) < 2:
        print("Not enough data points to compute pairwise differences.")
        return

    # --- 2) Compute pairwise values ---
    pairwise_values = []  # store val_ij for each valid pair
    pairwise_rows   = []  # store rows for output CSV

    n = len(t_points)
    for i in range(n):
        for j in range(i+1, n):
            t_i, H_i = t_points[i], h_points[i]
            t_j, H_j = t_points[j], h_points[j]

            # We can only take log of positive values
            if H_i <= 0 or H_j <= 0:
                continue
            # Also skip if times are the same (avoid zero in denominator)
            if t_i == t_j:
                continue

            # Calculate the value
            val_ij = (math.log(H_j) - math.log(H_i)) / (t_j - t_i)
            pairwise_values.append(val_ij)

            # Collect row data
            pairwise_rows.append([t_i, H_i, t_j, H_j, val_ij])

    if not pairwise_values:
        print("No valid pairs found (check for H(t) > 0 or distinct times).")
        return

    # --- 3) Compute average and median ---
    avg_val = statistics.mean(pairwise_values)
    med_val = statistics.median(pairwise_values)

    # --- 4) Write out a new CSV file ---
    # We'll form an output file name by appending "_pairwise_calc.csv"
    directory, filename = os.path.split(input_file)
    base, ext = os.path.splitext(filename)
    output_filename = base + "_pairwise_calc.csv"
    output_path = os.path.join(directory, output_filename)

    with open(output_path, 'w', newline='') as out_f:
        writer = csv.writer(out_f)
        # Write header:
        writer.writerow(["t_i", "H_i", "t_j", "H_j", "Value"])

        # Write each pair row
        for row_data in pairwise_rows:
            writer.writerow(row_data)

        # Leave a blank line or not, as you prefer
        writer.writerow([])
        # Write average and median
        # e.g., put them on separate rows
        writer.writerow(["Average", "", "", "", avg_val])
        writer.writerow(["Median", "", "", "", med_val])

    print(f"Created '{output_path}' with {len(pairwise_values)} pairwise results.")
    print(f"Average = {avg_val}")
    print(f"Median  = {med_val}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate a CSV file with pairwise calculations of "
                    "(-ln(H_i) + ln(H_j)) / (t_j - t_i)."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Input CSV file path with time and height data."
    )
    args = parser.parse_args()

    generate_pairwise_calc(args.file)
