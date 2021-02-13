#!/usr/bin/env python3
import re

from itertools import combinations

from recipe import Recipe


def get_unmapped_ingredients(ingredients, ingredient_map):
    """
    Of the ingredients given, pick out the ones that are not yet
    contained in the given map
    """
    # TODO
    return []


def get_unmapped_allergens(allergens, allergen_map):
    # TODO
    return []


def get_shared_ingredients(r1, r2):
    i1 = set(r1.get_ingredients())
    i2 = set(r2.get_ingredients())
    shared = i1.intersection(i2)
    return list(shared)


def get_shared_allergens(r1, r2):
    i1 = set(r1.get_allergens())
    i2 = set(r2.get_allergens())
    shared = i1.intersection(i2)
    return list(shared)


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

    print(all_ingredients)
    print(all_allergens)

    # - Find two recipes that share exactly one unmapped ingredient and one
    #   unmapped allergen
    # - The shared ingredient maps to the allergen
    # - If a recipe contains one unmapped ingredient and one unmapped allergen
    all_combos = list(combinations(recipes, 2))
    while len(allergen_map) == len(all_allergens):
        for combo in all_combos:
            r1 = combo[0]
            r2 = combo[1]
            shared_ing = get_shared_ingredients(r1, r2)
            shared_alg = get_shared_allergens(r1, r2)
            unmapped_ing = get_unmapped_ingredients(shared_ing, ingredient_map)
            unmapped_alg = get_unmapped_allergens(shared_alg, allergen_map)
            if len(unmapped_ing) == 1 and len(unmapped_alg) == 1:
                ingredient_map[unmapped_ing[0]] = unmapped_alg[0]
                allergen_map[unmapped_alg[0]] = unmapped_ing[0]

        for recipe in recipes:
            unmapped_ing = recipe.get_unmapped_ingredients(ingredient_map)
            unmapped_alg = recipe.get_unmapped_allergens(allergen_map)
            if len(unmapped_ing) == 1 and len(unmapped_alg) == 1:
                ingredient_map[unmapped_ing[0]] = unmapped_alg[0]
                allergen_map[unmapped_alg[0]] = unmapped_ing[0]

    print(allergen_map)


if __name__ == '__main__':
    main()
