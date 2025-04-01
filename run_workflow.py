#!/usr/bin/env python3

"""
The following workflow was started on March 19, year of our lord two thousand and twenty-five.

Notes for learning: input() always returns strings, even if numbers inputted.
    you will need to cast int(input("Enter an int: "))
"""

import argparse
import subprocess
import os
import sys

# For tab autocomplete
try:
    import readline
    import rlcompleter
    readline.parse_and_bind("tab: complete")
except ImportError:
    pass  # Tab completion won't be available on this platform

readline.parse_and_bind("tab: complete")

def step_1_export_images():
    input("\nStep 1: Please export your slide deck as individual PNG images. Press Enter when done...")

def check_and_install_package(module_name, package_name=None):
    """
    Will check for module_name like pptx or jinja2, and install the package package_name using pip
    if not found.
    """
    package_name = package_name or module_name
    print(f"Checking for required package \"{module_name}.\"")
    try:
        __import__(module_name)
        print(f"Package \"{module_name}\" imported.")
    except ImportError:
        print(f"Required package \"{module_name}\" not found.")

        choice = input(f"Would you like to try installing the package \"{package_name}\" using pip? [y/N]: "
            ).strip().lower()

        if choice == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"Successfully installed '{package_name}'.")
            except subprocess.CalledProcessError:
                print(f"Failed to install \"{package_name}\". Please install it manually. Exiting...")
                sys.exit(1)
        else:
            print(f"You will need to install \"{package_name}\" before continuing.\n \
                Please install \"{package_name}\" and rerun this script.")
            sys.exit(1)

def step_2_generate_elements_list_txt(pptx_path):
    print(f"\nStep 2: Generating slide titles from: {pptx_path}")

    if not os.path.exists(pptx_path):
        print("Error: PPTX file not found at the provided path.")
        sys.exit(1)

    try:
        subprocess.run(["python", "pptx_elements_to_list.py", pptx_path], check=True)
        print("Slide titles extracted successfully. \n \
            Manually review the .txt file before continuing with this script.")
    except subprocess.CalledProcessError:
        print("Error: Something went wrong while running pptx_elements_to_list.py.")
        sys.exit(1)

def step_3_prepare_jinja_tex_template():
    input("\nStep 3: Prepare the specially formatted .tex template. Press Enter when done...")

def step_4_render_document(txt_path, template_path):
    print(f"\n Step 4: Rendering output document. ")
    if not os.path.exists(txt_path):
        print("Error: Could not find the .txt file.")
        sys.exit(1)
    if not os.path.exists(template_path):
        print("Error: Could not find the .tex template file.")
        sys.exit(1)

    subprocess_cmd = ["python", "txt_to_template_rendering.py", txt_path, template_path]

    # Options:
    #   Output name
    output_name = input("Optional: Enter a name for the output .tex file \
                            (or press Enter to use default): ").strip()
    if output_name:
        subprocess_cmd += ["--output_name", output_name]
        print(f"Rendered document will be named {output_name}.tex")

    #   Image Naming Options:
    use_custom_images = input("Optional: Use custom image prefix/suffix or format? \
                                Default is slide.###.png [y/N]: ").strip().lower()
    if use_custom_images == 'y':
        prefix = input("Enter image filename prefix (or press Enter to skip): ").strip()
        suffix = input("Enter image file extension (e.g., .png, .pdf) (or press Enter to skip): ").strip()
        num_format = input("Enter number format (e.g., 03 for leading zeros, d for plain integer): ").strip()

        if prefix:
            subprocess_cmd += ["--prefix", prefix]
        if suffix:
            subprocess_cmd += ["--suffix", suffix]
        if num_format:
            subprocess_cmd += ["--num_format", num_format]

    # Run the command
    try:
        subprocess.run(subprocess_cmd, check=True)
        print("Template rendered successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to render the template.")
        sys.exit(1)




def main():
    parser = argparse.ArgumentParser(
        description=    "Interactive workflow for generating an accessible \
                        LaTeX skeleton from a slide deck."
    )

    #parser.add_argument("--pptx", help="Path to the .pptx slide deck", required=True)

    # We'll add arguments here later
    args = parser.parse_args()

    # Start the workflow
    print("=== Accessible TeX Skeletonizer ===")
    step_1_export_images()

    # Step 2: Pull Titles (in future +other elements) from Pptx.
    # Dependency check here before we continue
    check_and_install_package("pptx", "python-pptx")
    #step_2_generate_elements_list_txt(args.pptx)
    pptx_path = input("Enter the path to your .pptx file: ").strip()
    step_2_generate_elements_list_txt(pptx_path)

    # Step 3: Prepare jinja tex template. 
    # Dependency check for jinja
    step_3_prepare_jinja_tex_template()
    check_and_install_package("jinja2", "Jinja2")

    # Step  4: Render
    #       4a: prompt for files
    #       4b: options
    #       4c: complete render
    element_list_txt_path = input("Enter the path to your .txt file: ").strip()
    jinja_template_tex_path = input("Enter the path to your template .tex file: ").strip()

    step_4_render_document(element_list_txt_path, jinja_template_tex_path)


    print("End of up to check_and_install_package 2")


if __name__ == "__main__":
    main()

