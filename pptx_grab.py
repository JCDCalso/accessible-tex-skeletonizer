from pptx import Presentation
import argparse

def count_slides(pres) -> int:
    return len(pres.slides)

def grab_title_if_exists(slide) -> str:
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text:
            # Check if the shape is the title
            if shape == slide.shapes.title:
                return shape.text_frame.text
    return ""

def iterate_thru_slides(pres, *funcs):
    return [ [func(slide) for func in funcs]
            for slide in pres.slides ]
#    results = []
#    for slide in pres:
#        for func in funcs:
#            results.append(func(slide))
#    return results

def slide_titles_to_text(pres, filename):
    data = iterate_thru_slides(pres, grab_title_if_exists)
    with open(filename, 'w') as file:
        for sublist in data:
            line = ' '.join(map(str, sublist))  # Each item to string and join with spaces
            file.write(line + '\n')  # Write each sublist as a line in the file
    print("Data saved to" + str(filename) + ".txt")


def main():
    # Create Parser, add arguments, parse arguments, create funct descrip.
    my_desc = "A function for grabbing certain basic elements from pptx"
    
    parser = argparse.ArgumentParser(description = my_desc)

    parser.add_argument("prs_filepath", type=str, help="Path to presentation file.")
    # Add additional arguments...

    args = parser.parse_args()

    # Continue with main function and call other functions
        # only slide_titles_to_text currently, plan on expanding in future
    filename = args.prs_filepath + "-slide_titles.txt"
    
    pres = Presentation(args.prs_filepath)

    slide_titles_to_text(pres, filename)

# Run main function if running script directly
if __name__ == "__main__":
    main()

# If this file, jc.py, is imported, you would call it using
# import jc (needs to be in the same directory or alter the path)
# use function by calling jc.function(...,...)
