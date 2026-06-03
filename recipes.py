"""
Модуль для управления рецептами.
Содержит классы Ingredient, Recipe, ShoppingList, DietaryRecipe.
"""

from collections import defaultdict


class Ingredient:
    """Класс, представляющий ингредиент рецепта."""
    
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self._quantity = None
        self.quantity = quantity
        self.unit = unit
    
    @property
    def quantity(self) -> float:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: float):
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Количество должно быть положительным")
        
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        
        self._quantity = value
    
    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    
    def __hash__(self) -> int:
        return hash((self.name, self.unit))


class Recipe:
    """Класс, представляющий рецепт блюда."""
    
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []
    
    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    
    @staticmethod
    def is_valid_ratio(ratio: float) -> bool:
        try:
            return ratio > 0
        except TypeError:
            return False
    
    def scale(self, ratio: float) -> 'Recipe':
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")
        
        scaled_ingredients = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            for ing in self.ingredients
        ]
        return Recipe(self.title, scaled_ingredients)
    
    def __len__(self) -> int:
        return len(self.ingredients)
    
    def __str__(self) -> str:
        ingredients_str = "\n".join(f"  - {ing}" for ing in self.ingredients)
        return f"{self.title}:\n{ingredients_str}"


class ShoppingList:
    """Класс, представляющий список покупок."""
    
    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))
    
    def remove_recipe(self, title: str):
        self._items = [(ing, rt) for ing, rt in self._items if rt != title]
    
    def get_list(self) -> list:
        totals = defaultdict(float)
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            totals[key] += ingredient.quantity
        
        result = [Ingredient(name, qty, unit) for (name, unit), qty in totals.items()]
        result.sort(key=lambda ing: ing.name)
        return result
    
    def __add__(self, other: 'ShoppingList') -> 'ShoppingList':
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list


class DietaryRecipe(Recipe):
    """Класс, представляющий диетический рецепт."""
    
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    
    def scale(self, ratio: float) -> 'DietaryRecipe':
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(scaled_recipe.title, self.diet_type, scaled_recipe.ingredients)
    
    def __str__(self) -> str:
        return f"[{self.diet_type}] {super().__str__()}"


if __name__ == "__main__":
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    
    pizza = Recipe("Пицца Маргарита", [flour, cheese])
    print(pizza)
    
    vegan_pizza = DietaryRecipe("Пицца", "веган", [flour])
    print(vegan_pizza)