#!/usr/bin/env python3
import re

from recipe import Recipe


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
    mapped_ings = set([])
    mapped_algs = set([])
    unmapped_ings = set(all_ingredients)
    unmapped_algs = set(all_allergens)

    while len(allergen_map) < len(all_allergens):
        for alg in all_allergens:
            # If this allergen has already been mapped, skip it.
            if alg in mapped_algs:
                continue
            
            # Get all recipes containing this allergen
            f = filter(lambda r: alg in r.get_allergens(), recipes)
            recipes_containing_alg = list(f)
            print('{0} is in {1} recipes'.format(alg, len(recipes_containing_alg)))
            
            # Get the intersection of all ingredients in those recipes
            inter = set(all_ingredients)
            for r in recipes_containing_alg:
                inter = inter.intersection(r.get_ingredients())
                print('intersection of all ingredients: {0}'.format(list(inter)))

            # Remove all mapped ingredients from the intersection
            inter = inter - mapped_ings
                
            if len(inter) == 1:
                ing = list(inter)[0]
                print('Locking {0} to {1}'.format(alg, ing))
                ingredient_map[ing] = alg
                allergen_map[alg] = ing
                mapped_ings = mapped_ings.union(set([ing]))
                mapped_algs = mapped_algs.union(set([alg]))
                
            print('--------------------------')

    print(allergen_map)
    all_allergens.sort()
    print(all_allergens)
    sorted_ings = []
    for alg in all_allergens:
        sorted_ings = sorted_ings + [allergen_map[alg]]

    print(sorted_ings)

    canonical_list = ','.join(sorted_ings)
    print(canonical_list)
        

if __name__ == '__main__':
    main()
