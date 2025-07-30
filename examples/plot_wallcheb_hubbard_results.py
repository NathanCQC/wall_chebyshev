#!/usr/bin/env python3
"""
This script reads the Wall-Cheb Hubbard results CSV and plots energy vs polynomial order (m).
It also draws a horizontal line for the true ground state energy.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_results(csv_path: str, output_path: str, true_energy: float) -> None:
    # Read the results
    df = pd.read_csv(csv_path)
    # Use first column as x (order) and second as y (energy)
    x = df.iloc[:, 0].to_numpy()
    y = df.iloc[:, 1].to_numpy()
    

    print(f"x: {x}")
    print(f"y: {y}")

    # Plot energy vs polynomial order
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Projected Energy')

    # Draw horizontal line for true energy
    plt.axhline(y=true_energy, color='r', linestyle='--', label='True Ground State Energy')

    # Labels and title
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.title('Wall-Cheb Hubbard: Energy vs Polynomial Order')
    plt.legend()
    plt.grid(True)
    # Set y-axis limits so energy increases from top to bottom (inverted axis)
    # Range: from -0.9 (highest) down to just below true ground state energy
    lower_limit = true_energy - 0.1
    upper_limit = -0.9
    plt.ylim(lower_limit, upper_limit)

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Plot saved to: {output_path}")


if __name__ == '__main__':
    # Determine paths
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, 'wallcheb_hubbard_results_old.csv')
    output_file = os.path.join(script_dir, 'energy_vs_polynomial_order.png')
    TRUE_ENERGY = -1.5615528128088303

    plot_results(csv_file, output_file, TRUE_ENERGY)
