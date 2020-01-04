import argparse
import helloshopper
import time


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Text file with recipe urls separated by new lines")
    parser.add_argument('--output', help="Name of output file. Default is OurShoppingList.csv")
    args = parser.parse_args()

    ings = []  # Empty list of ingredients

    # Read text file with urls
    with open(args.filename) as file:
        for line in file:
            line = line.rstrip()  # Get URL
            print("Processing: %s" % line)
            ingredients = helloshopper.process_url(line)  # Return list of ingredients
            ings.extend(ingredients)  # Add ingredients to list
            print("Sleeping 7 seconds")
            time.sleep(7)  # Being nice to website and sleeping

    print("Combining ingredients")
    # Create empty Panda dataframe
    df = helloshopper.combine_ingredients(ings)  # Combine all ingredients
    print(df.head())

    # Output to csv
    print("Outputting to csv")
    if args.output:
        df.to_csv(args.output)
    else:
        df.to_csv('ShoppingList.csv', index=False)


if __name__ == "__main__":
    main()
