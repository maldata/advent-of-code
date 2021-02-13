#!/usr/bin/env python3
class Allergen:
    def __init__(self, name_str):
        self._name = name_str
        self._ingredient = None

    @property
    def name(self):
        return self._name

    @property
    def ingredient(self):
        return self._ingredient

    @ingredient.setter
    def ingredient(self, value):
        if self._ingredient is None:
            self._ingredient = value
