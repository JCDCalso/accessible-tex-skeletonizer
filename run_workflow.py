#!/usr/bin/env python3

"""
The following workflow was started on March 19, year of our lord two thousand and twenty-five.

Notes for learning: input() always returns strings, even if numbers inputted.
    you will need to cast int(input("Enter an int: "))
"""

import argparse

def step_1_export_images():
    input("\nStep 1: Please export your slide deck as individual PNG images. Press Enter when done...")

def main():
    parser = argparse.ArgumentParser(
        description="Interactive workflow for generating an accessible LaTeX skeleton from a slide deck."
    )

    # We'll add arguments here later
    args = parser.parse_args()

    # Start the workflow
    print("=== Accessible TeX Skeletonizer ===")
    step_1_export_images()

if __name__ == "__main__":
    main()

