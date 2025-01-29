import matplotlib.pyplot as plt
import csv
import argparse

def plot_points(file_path, connect_points):
    """
    Reads a CSV file, skips the header, and plots the first and last columns as points.
    Optionally connects the points with lines.

    Parameters:
    - file_path: Path to the CSV file containing the data
    - connect_points: Boolean indicating whether to connect the points with lines
    """
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

            except ValueError:
                print(f"Skipping row with invalid data: {row}")
                continue
            except IndexError:
                print("Skipping incomplete row.")
                continue

    # Plot the points
    if connect_points:
        # Connect the points with a line
        plt.plot(x_points, y_points, marker='o', color='red', label='Foam Data')
    else:
        # Display points without connecting them
        plt.scatter(x_points, y_points, color='red', label='Foam Data - Brand 3')

    # Adjust the size of the labels and title
    plt.title("FOAM Height in Time ", fontsize=16)  # Title font size
    plt.xlabel("Time (s)", fontsize=14)  # X-axis label font size
    plt.ylabel("Foam Height (cm)", fontsize=14)  # Y-axis label font size
    
    # Adjust the size of the tick labels
    plt.xticks(fontsize=12)  # X-axis tick labels font size
    plt.yticks(fontsize=12)  # Y-axis tick labels font size
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot points from a CSV file.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path to the source CSV file")
    parser.add_argument('-c', '--connect', action='store_true', help="Connect the dots with lines")
    args = parser.parse_args()

    plot_points(args.file, args.connect)
