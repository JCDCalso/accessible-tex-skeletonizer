import argparse

def to_list(title_list_txt_file):
    with open(title_list_txt_file, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    return lines


def main():
    # Create Parser, add arguments, parse arguments, create funct descrip.
    my_desc = "Loads text of slide titles (each on new line) and creates a python list object."
    parser = argparse.ArgumentParser(description=my_desc)

    parser.add_argument("title_list_txt_file", type=str, help="path to .txt file")
    # Add additional arguments...

    args = parser.parse_args()

    # Continue with main function and call other functions
    title_list = to_list(args.title_list_txt_file)

    #print(title_list)

# Run main function if running script directly

if __name__ == "__main__":
    main()

# If this file, jc.py, is imported, you would call it using
# import jc (needs to be in the same directory or alter the path)
# use function by calling jc.function(...,...)
