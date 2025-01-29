import matplotlib.pyplot as plt
import csv
import argparse
import numpy as np
import sympy as sp



def plot_points(file_path, line_function=None):
    """
    Reads a CSV file, skips the header, and plots the first and last columns as points.
    Optionally, plots a user-defined line function, adds vertical lines to it,
    and calculates the distances of points above and below the line.
    
    Parameters:
    - file_path: Path to the CSV file containing the data
    - line_function: String representing the line function in terms of 'x' (optional)

    python scaledLNY.py -f beer1.csv -l "0.0033335*x + 2.8" 

    ln(y)  ... linear function
    """
    x_points = []
    y_points = []

    # Parse the line function using sympy if it's provided
    line_expr = None
    x = sp.symbols('x')
    if line_function:
        line_expr = sp.sympify(line_function)

    distance_above = 0  # Distance above the line
    distance_below = 0  # Distance below the line
    sum_squares = 0 

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header line

        for row in reader:
            try:
                # Extract the first (x) and last (y) columns
                x_val = float(row[0])  # First column
                y_val = float(row[-1])  # Last column

                y_ln = np.log(y_val)
                # Append to data points
                x_points.append(x_val)
                y_points.append(y_ln)

            except ValueError:
                print(f"Skipping row with invalid data: {row}")
                continue
            except IndexError:
                print("Skipping incomplete row.")
                continue

    # Plot the Points
    plt.scatter(x_points, y_points, color='red', label='Foam Data - Brand 3')

    if line_expr:
        # Generate x values for the line
        x_line = np.linspace(min(x_points), max(x_points), 100)
        
        # Evaluate the line function at the given x values
        y_line = [float(line_expr.evalf(subs={x: xi})) for xi in x_line]

        # Plot the line
        plt.plot(x_line, y_line, color='red', linestyle='-', label=f'Line: y =  {line_function}')

        # Adding vertical lines from points to the line function
        for x_p, y_p in zip(x_points, y_points):
            y_line_val = float(line_expr.evalf(subs={x: x_p}))  # y-value from the line function
            distance = y_p - y_line_val  # Calculate the signed distance

            if distance > 0:
                distance_above += distance
                sum_squares += distance*distance
            else:
                distance_below += abs(distance)
                sum_squares += distance*distance

            # Plot vertical line
            plt.plot([x_p, x_p], [y_p, y_line_val], linestyle='solid', color='gray', alpha=0.8)
        
        # Plot the distances on the graph
        plt.text(
            0.05, 0.20, f"Distance Above: {distance_above:.4f}",
            fontsize=12, ha='left', va='bottom', transform=plt.gca().transAxes,
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
        )
        plt.text(
            0.05, 0.15, f"Distance Below: {distance_below:.4f}",
            fontsize=12, ha='left', va='bottom', transform=plt.gca().transAxes,
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
        )
        plt.text(
            0.05, 0.10,  # Adjusted y-coordinate for bottom placement
            f"Total (A-B): {(distance_above - distance_below):.4f}", 
            fontsize=12, ha='left', va='bottom', 
            transform=plt.gca().transAxes, 
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round, pad=0.5')
        )
        plt.text(
            0.05, 0.05,  # Adjusted y-coordinate for bottom placement
            f"Area of squares: {(sum_squares):.4f}", 
            fontsize=12, ha='left', va='bottom', 
            transform=plt.gca().transAxes, 
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round, pad=0.5')
        )
        
    # Adjust the size of the labels and title
    plt.title("FOAM Height in TIME - scaled ln(y)", fontsize=20)  # Title font size
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
    parser = argparse.ArgumentParser(description="Plot points from a CSV file and optionally plot a user-defined line function.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Path to the source CSV file")
    parser.add_argument('-l', '--line', type=str, help="Line function (in terms of x) to plot, e.g. '2*x + 3' (optional)")
    args = parser.parse_args()

    plot_points(args.file, args.line)
