#!/usr/bin/env python3
import re

from recipe import Recipe


def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    lines = [line.strip() for line in all_lines]
    recipes = [Recipe(line) for line in lines]

    # - Find two recipes that share exactly one unmapped ingredient and one
    #   unmapped allergen
    # - The shared ingredient maps to the allergen
    # - If a recipe contains one unmapped ingredient and one unmapped allergen
    all_allergens = None  # get a list of all allergens
    allergen_map = {}     # keys = allergens,   values = ingredients
    ingredient_map = {}   # keys = ingredients, values = allergens
    


if __name__ == '__main__':
    main()
