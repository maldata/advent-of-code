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
        
