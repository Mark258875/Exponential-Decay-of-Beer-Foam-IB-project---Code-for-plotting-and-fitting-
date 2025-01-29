import matplotlib.pyplot as plt
import csv
import argparse
import time
import itertools



def plot_live_points(file_paths):
    """
    Reads multiple CSV files, skips the header in each, and plots the first and last columns dynamically with unique colors for each file.

    Parameters:
    - file_paths: List of file paths to the CSV files containing the data

    python plotPoints.py -f beer1.csv beer2.csv    
    """
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_title("FOAM Height in Time (3 brands)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Foam Height (cm)")
    ax.grid(True, linestyle='--', alpha=0.5)

    color_cycle = itertools.cycle(['blue', 'green', 'red', 'purple', 'orange', 'brown', 'cyan', 'magenta'])
    count = 1

    for file_path in file_paths:
        color = next(color_cycle)  # Get the next color from the cycle
        x_points = []
        y_points = []


        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header line

            for row in reader:
                

                try:
                    # Extract the first (x) and last (y) columns
                    x = float(row[0])  # First column
                    y = float(row[-1])  # Last column
                    
                    # Append to data points
                    x_points.append(x)
                    y_points.append(y)

                    

                    # Plot the current data for this file
                    ax.scatter(x_points, y_points, marker='o', color=color, label=f"Brand{count}"if len(x_points) == 1 else "")
                    plt.pause(0.5)  # Pause for half a second to simulate live plotting
                
                except ValueError:
                    print(f"Skipping row with invalid data: {row}")
                    continue
                except IndexError:
                    print("Skipping incomplete row.")
                    continue
        count+=1

    ax.legend()
    plt.ioff()  # Turn off interactive mode
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic plotting from multiple CSV files.")
    parser.add_argument('-f', '--files', type=str, nargs='+', required=True, help="Paths to the source CSV files")
    args = parser.parse_args()

    plot_live_points(args.files)
