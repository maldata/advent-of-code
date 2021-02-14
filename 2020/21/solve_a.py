#!/usr/bin/env python3
import re

from itertools import combinations

from recipe import Recipe


def get_unmapped_ingredients(ingredients, ingredient_map):
    f = filter(lambda x: x not in ingredient_map, ingredients)
    return list(f)


def get_unmapped_allergens(allergens, allergen_map):
    f = filter(lambda x: x not in allergen_map, allergens)
    return list(f)


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    lines = [line.strip() for line in all_lines]
    recipes = [Recipe(line) for line in lines]

    all_ingredients = []
    all_allergens = []
    ingredient_map = {}   # keys = ingredients, values = allergens
    allergen_map = {}     # keys = allergens,   values = ingredients

    for recipe in recipes:
        all_ingredients = all_ingredients + recipe.get_ingredients()
        all_allergens = all_allergens + recipe.get_allergens()

    all_ingredients = list(set(all_ingredients))
    all_allergens = list(set(all_allergens))

    all_combos = list(combinations(recipes, 2))
    while len(allergen_map) != len(all_allergens):
        for combo in all_combos:
            r1 = combo[0]
            r2 = combo[1]
            shared_ing = r1.get_shared_ingredients(r2)
            shared_alg = r1.get_shared_allergens(r2)

            print()
            print('shared ing: {0}'.format(shared_ing))
            print('shared alg: {0}'.format(shared_alg))
            print()
            
            unmapped_ing = get_unmapped_ingredients(shared_ing, ingredient_map)
            unmapped_alg = get_unmapped_allergens(shared_alg, allergen_map)
            
            if len(unmapped_ing) == 1 and len(unmapped_alg) == 1:
                ingredient_map[unmapped_ing[0]] = unmapped_alg[0]
                allergen_map[unmapped_alg[0]] = unmapped_ing[0]
                print('unmapped ingredient / allergen: {0} / {1}'.format(shared_ing, shared_alg))

        for recipe in recipes:
            unmapped_ing = get_unmapped_ingredients(recipe.get_ingredients(), ingredient_map)
            unmapped_alg = get_unmapped_allergens(recipe.get_allergens(), allergen_map)

            if len(unmapped_ing) == 1 and len(unmapped_alg) == 1:
                ingredient_map[unmapped_ing[0]] = unmapped_alg[0]
                allergen_map[unmapped_alg[0]] = unmapped_ing[0]
                print('unmapped ingredient / allergen: {0} / {1}'.format(shared_ing, shared_alg))

    print(allergen_map)


if __name__ == '__main__':
    main()
