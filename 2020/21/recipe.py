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

    def get_shared_ingredients(self, r2):
        i1 = set(self.get_ingredients())
        i2 = set(r2.get_ingredients())
        shared = i1.intersection(i2)
        return list(shared)

    def get_shared_allergens(self, r2):
        i1 = set(self.get_allergens())
        i2 = set(r2.get_allergens())
        shared = i1.intersection(i2)
        return list(shared)
