import scrape_schema_recipe
from urllib.parse import urlparse
from unidecode import unidecode
from fractions import Fraction
import pandas as pd
import unicodedata
import re


# https://stackoverflow.com/a/49440661 - Detect if fraction in unicode
def fraction_finder(s):
    for c in s:
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        if name.startswith('VULGAR FRACTION'):
            return True
        else:
            return False


def process_url(url):

    # Check for hellofresh
    domain = urlparse(url).netloc
    if "hellofresh" in domain:
        recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
        recipe = recipe_list[0]

        # Return list of ingredients
        return recipe['recipeIngredient']
    else:
        print("Not a Hello Fresh domain")
        return


def combine_ingredients(ingredients):

    col_names = ['Amount', 'Measurement', 'Ingredient']
    all_list = []

    for ingredient in ingredients:
        regex = r"(^(.*?)[\s])((.*?)[\s])(.*)"  # Regex to match each string in list for columns
        match = re.match(regex, ingredient, re.M | re.I)

        if match is not None:  # Sometimes we get only one ingredient like salt or pepper

            is_fraction = fraction_finder(match.group(1))
            if is_fraction:
                match_1 = float(sum(Fraction(x) for x in unidecode(match.group(1)).split()))
                ing_list = [match_1, match.group(3), match.group(5)]
            else:
                ing_list = [match.group(1), match.group(3), match.group(5)]
            all_list.append(ing_list)

    df = pd.DataFrame(all_list, columns=col_names)
    df['Amount'] = pd.eval(df['Amount'].fillna(1000.0))
    df["Amount"] = pd.to_numeric(df["Amount"])  # Convert the amount column to numeric so we can add together

    print(df)
    df = df.groupby(['Ingredient', 'Measurement'], sort=False, as_index=False).sum()

    return df
