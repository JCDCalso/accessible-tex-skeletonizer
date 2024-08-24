import argparse

def function(a, b):
    return a+b

def main():
    # Create Parser, add arguments, parse arguments, create funct descrip.
    my_desc = ""
    # Create the parser
    parser = argparse.ArgumentParser(description=my_desc)



    parser.add_argument("a", type=str, help="Argument a is ____")
    # Add additional arguments...

    args = parser.parse_args()

    # Continue with main function and call other functions
    x = function(args.a, args.b)
    ...

# Run main function if running script directly

if __name__ == "__main__":
    main()

# If this file, jc.py, is imported, you would call it using
# import jc (needs to be in the same directory or alter the path)
# use function by calling jc.function(...,...)
