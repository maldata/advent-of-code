#!/usr/bin/env python3
import re


class Recipe:
    def __init__(self, input_str):
        m = re.match('(.+)\(contains (.+)\)', input_str)
        ingredient_str = m.group(1)
        ingredient_str = ingredient_str.strip()
        allergen_str = m.group(2)
        allergen_str = allergen_str.strip()

        ingredients = [i.strip() for i in ingredient_str.split(' ')]
        allergens = [a.strip() for a in allergen_str.split(',')]
        
        self._ingredients = set(ingredients)
        self._allergens = set(allergens)
        
    def get_ingredients(self):
        return list(self._ingredients)

    def get_allergens(self):
        return list(self._allergens)

    def get_unmapped_ingredients(self, ingredient_map):
        # TODO
        return []
    
    def get_unmapped_allergens(self, allergen_map):
        # TODO
        return []
