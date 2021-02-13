#!/usr/bin/env python3
class Ingredient:
    def __init__(self, name_str):
        self._name = name_str
        self._allergen = None

    @property
    def name(self):
        return self._name

    @property
    def allergen(self):
        return self._allergen

    @allergen.setter
    def allergen(self, value):
        if self._allergen is None:
            self._allergen = value
