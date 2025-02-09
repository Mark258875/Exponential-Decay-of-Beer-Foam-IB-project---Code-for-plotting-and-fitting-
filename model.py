import matplotlib.pyplot as plt
import csv
import argparse
import numpy as np
import math
import os

def plot_points(file_path, connect_points, exp_params, save_data):
    """
    Reads a CSV file, skips the header, and plots the first and last columns as points.
    Optionally connects the points with lines.
    If exp_params is provided, also plots y = A * exp(B * x) + C.
    If save_data is True, saves a new CSV file with columns: [time, actual, fitted].
    
    Parameters:
    - file_path: Path to the CSV file containing the data
    - connect_points: Boolean indicating whether to connect the points with lines
    - exp_params: A tuple/list of three floats [A, B, C] for the exponential function:
                  y = A * exp(B * x) + C
                  or None if the user does not want to plot the exponential function.
    - save_data: Boolean indicating whether to save the new CSV file.
    """
    x_points = []
    y_points = []

    # 1) Read data from the CSV
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header line

        for row in reader:
            try:
                x = float(row[0])  # First column
                y = float(row[-1]) # Last column
                x_points.append(x)
                y_points.append(y)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
                continue
            except IndexError:
                print("Skipping incomplete row.")
                continue

    # 2) Plot the data points
    if connect_points:
        plt.plot(x_points, y_points, marker='o', color='red', label='Foam Data')
    else:
        plt.scatter(x_points, y_points, color='blue', label='Foam Data - Brand 1')

    # 3) If exp_params is provided, plot the exponential function
    if exp_params is not None and len(exp_params) == 3:
        A, B, C = exp_params
        # Generate 5000 points to get a nearly continuous curve
        x_min, x_max = min(x_points), max(x_points)
        x_exp = np.linspace(x_min, x_max, 5000)
        y_exp = A * np.exp(B * x_exp) + C
        
        # Plot as tiny dots (marker='.') to give a 'continuous' look
        plt.plot(x_exp, y_exp, 'b.', markersize=1,color="black", 
                 label=f"Exp: y = {A} * e^({B} x) + {C}")

    # 4) Save data to a new CSV if requested
    if save_data:
        # Separate out directory, base file name, and extension
        directory, base_filename = os.path.split(file_path)
        filename, ext = os.path.splitext(base_filename)
        # Construct new filename: filename_fitted_output.csv
        new_filename = f"{filename}_fitted_output.csv"
        output_file = os.path.join(directory, new_filename)

        with open(output_file, 'w', newline='') as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(["Time", "Actual Value", "Fitted Value"])

            if exp_params is not None and len(exp_params) == 3:
                A, B, C = exp_params
                for x, y in zip(x_points, y_points):
                    fitted = A * math.exp(B * x) + C
                    writer.writerow([x, y, fitted])
            else:
                # If no exponential parameters, just leave fitted column empty
                for x, y in zip(x_points, y_points):
                    writer.writerow([x, y, ""])

        print(f"Data saved to {output_file}.")

    # 5) Customize and show the plot
    plt.title("FOAM Height in Time", fontsize=16)
    plt.xlabel("Time (s)", fontsize=14)
    plt.ylabel("Foam Height (cm)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot points from a CSV file.")
    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help="Path to the source CSV file"
    )
    parser.add_argument(
        '-c', '--connect',
        action='store_true',
        help="Connect the dots with lines"
    )
    parser.add_argument(
        '--exp',
        nargs=3,
        type=float,
        metavar=('A', 'B', 'C'),
        help="If provided, plots the exponential function: y = A * exp(B * x) + C"
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help="If provided, saves a CSV file with columns: [time, actual value, fitted value]"
    )

    args = parser.parse_args()

    plot_points(
        file_path=args.file,
        connect_points=args.connect,
        exp_params=args.exp,
        save_data=args.save
    )
