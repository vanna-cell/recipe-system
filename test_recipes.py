"""
Тесты для классов рецептов.
"""

import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


class TestIngredient:
    """Тесты для класса Ingredient."""
    
    def test_creation(self):
        ingredient = Ingredient("Мука", 500.0, "г")
        assert ingredient.name == "Мука"
        assert ingredient.quantity == 500.0
        assert ingredient.unit == "г"
    
    def test_quantity_must_be_positive(self):
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Мука", -100, "г")
        
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Мука", 0, "г")
    
    def test_str_method(self):
        ingredient = Ingredient("Мука", 500.0, "г")
        assert str(ingredient) == "Мука: 500.0 г"
    
    def test_eq_method(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 1000.0, "г")
        ing3 = Ingredient("Сахар", 500.0, "г")
        
        assert ing1 == ing2
        assert ing1 != ing3


class TestRecipe:
    """Тесты для класса Recipe."""
    
    def test_creation(self):
        recipe = Recipe("Пицца")
        assert recipe.title == "Пицца"
        assert recipe.ingredients == []
    
    def test_add_ingredient_new(self):
        recipe = Recipe("Пицца")
        ingredient = Ingredient("Мука", 500.0, "г")
        recipe.add_ingredient(ingredient)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 500.0
    
    def test_add_ingredient_existing(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500.0, "г"))
        recipe.add_ingredient(Ingredient("Мука", 300.0, "г"))
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 800.0
    
    def test_scale_returns_new_instance(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        scaled = recipe.scale(2)
        assert scaled is not recipe
        assert scaled.title == recipe.title
    
    def test_scale_multiplies_quantities(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        scaled = recipe.scale(2.5)
        assert scaled.ingredients[0].quantity == 1250.0
    
    def test_scale_invalid_ratio(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        with pytest.raises(ValueError, match="положительным"):
            recipe.scale(-1)
    
    def test_len_method(self):
        recipe = Recipe("Пицца", [
            Ingredient("Мука", 500.0, "г"),
            Ingredient("Сыр", 200.0, "г")
        ])
        assert len(recipe) == 2


class TestShoppingList:
    """Тесты для класса ShoppingList."""
    
    def test_add_recipe(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        shopping_list.add_recipe(recipe, 2)
        assert len(shopping_list._items) == 1
        assert shopping_list._items[0][0].quantity == 1000.0
    
    def test_add_recipe_invalid_portions(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        with pytest.raises(ValueError, match="положительным"):
            shopping_list.add_recipe(recipe, -1)
    
    def test_remove_recipe(self):
        shopping_list = ShoppingList()
        pizza = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        pasta = Recipe("Паста", [Ingredient("Мука", 300.0, "г")])
        shopping_list.add_recipe(pizza, 1)
        shopping_list.add_recipe(pasta, 1)
        shopping_list.remove_recipe("Пицца")
        assert len(shopping_list._items) == 1
        assert shopping_list._items[0][1] == "Паста"
    
    def test_remove_recipe_nonexistent(self):
        shopping_list = ShoppingList()
        pizza = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        shopping_list.add_recipe(pizza, 1)
        shopping_list.remove_recipe("Борщ")
        assert len(shopping_list._items) == 1
    
    def test_get_list_aggregates_ingredients(self):
        shopping_list = ShoppingList()
        pizza = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        bread = Recipe("Хлеб", [Ingredient("Мука", 300.0, "г")])
        shopping_list.add_recipe(pizza, 1)
        shopping_list.add_recipe(bread, 1)
        result = shopping_list.get_list()
        assert len(result) == 1
        assert result[0].quantity == 800.0
    
    def test_get_list_sorted_by_name(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Сборный", [
            Ingredient("Сыр", 200.0, "г"),
            Ingredient("Мука", 500.0, "г"),
            Ingredient("Яйца", 3.0, "шт")
        ])
        shopping_list.add_recipe(recipe, 1)
        result = shopping_list.get_list()
        names = [ing.name for ing in result]
        assert names == sorted(names)
    
    def test_add_operator(self):
        list1 = ShoppingList()
        list2 = ShoppingList()
        pizza = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
        pasta = Recipe("Паста", [Ingredient("Сыр", 200.0, "г")])
        list1.add_recipe(pizza, 1)
        list2.add_recipe(pasta, 1)
        combined = list1 + list2
        assert len(combined._items) == 2
        assert len(list1._items) == 1
        assert len(list2._items) == 1


class TestDietaryRecipe:
    """Тесты для класса DietaryRecipe."""
    
    def test_creation(self):
        recipe = DietaryRecipe("Пицца", "веган")
        assert recipe.title == "Пицца"
        assert recipe.diet_type == "веган"
    
    def test_scale_returns_dietary_recipe(self):
        recipe = DietaryRecipe("Пицца", "веган", [Ingredient("Мука", 500.0, "г")])
        scaled = recipe.scale(2)
        assert isinstance(scaled, DietaryRecipe)
        assert scaled.diet_type == "веган"
    
    def test_str_method(self):
        recipe = DietaryRecipe("Пицца", "веган", [Ingredient("Мука", 500.0, "г")])
        assert str(recipe).startswith("[веган]")