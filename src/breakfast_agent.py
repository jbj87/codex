"""Multimodal breakfast agent starter kit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class IngredientProfile:
    proteins: set[str]
    carbs: set[str]
    vegetables: set[str]
    dairy: set[str]
    extras: set[str]


@dataclass(frozen=True)
class Recipe:
    name: str
    required: set[str]
    optional: set[str]
    instructions: list[str]

    def matches(self, pantry: set[str]) -> bool:
        return self.required.issubset(pantry)

    def missing(self, pantry: set[str]) -> set[str]:
        return self.required.difference(pantry)


class BreakfastAgent:
    """A lightweight agent that suggests breakfast recipes based on ingredients."""

    def __init__(self, recipes: Iterable[Recipe]) -> None:
        self._recipes = list(recipes)

    def suggest(self, ingredients: Iterable[str]) -> list[Recipe]:
        pantry = {item.lower().strip() for item in ingredients if item.strip()}
        matches = [recipe for recipe in self._recipes if recipe.matches(pantry)]
        return sorted(matches, key=lambda recipe: recipe.name)

    def gaps(self, ingredients: Iterable[str]) -> dict[str, set[str]]:
        pantry = {item.lower().strip() for item in ingredients if item.strip()}
        return {
            recipe.name: recipe.missing(pantry)
            for recipe in self._recipes
            if recipe.missing(pantry)
        }


class VisionIngredientRecognizer:
    """Placeholder for a vision model that extracts ingredients from an image."""

    def __init__(self, model_name: str = "placeholder-vision-model") -> None:
        self.model_name = model_name

    def detect(self, image_path: str | Path) -> list[str]:
        """Stub detection routine.

        Replace this method with an actual multimodal model call that returns
        ingredient labels from the image.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        return []


def build_default_recipes() -> list[Recipe]:
    return [
        Recipe(
            name="avocado toast",
            required={"bread", "avocado"},
            optional={"egg", "salt", "pepper", "lemon"},
            instructions=[
                "Toast the bread.",
                "Mash avocado with salt, pepper, and lemon.",
                "Spread avocado on toast and top with a fried egg if available.",
            ],
        ),
        Recipe(
            name="veggie omelet",
            required={"egg"},
            optional={"spinach", "tomato", "onion", "cheese"},
            instructions=[
                "Whisk eggs with salt and pepper.",
                "Saute vegetables until tender.",
                "Pour eggs over vegetables, add cheese, fold, and cook until set.",
            ],
        ),
        Recipe(
            name="yogurt parfait",
            required={"yogurt"},
            optional={"granola", "berries", "honey", "nuts"},
            instructions=[
                "Layer yogurt with granola and fruit.",
                "Drizzle honey and add nuts for crunch.",
            ],
        ),
        Recipe(
            name="breakfast burrito",
            required={"tortilla", "egg"},
            optional={"beans", "cheese", "salsa", "spinach"},
            instructions=[
                "Scramble eggs and warm the tortilla.",
                "Fill with eggs and optional ingredients.",
                "Roll tightly and serve with salsa.",
            ],
        ),
    ]


def build_default_profile() -> IngredientProfile:
    return IngredientProfile(
        proteins={"egg", "beans", "turkey", "sausage", "bacon", "tofu"},
        carbs={"bread", "tortilla", "oats", "granola"},
        vegetables={"spinach", "tomato", "onion", "mushroom", "pepper"},
        dairy={"milk", "cheese", "yogurt", "butter"},
        extras={"avocado", "berries", "honey", "nuts"},
    )


def summarize_ingredients(ingredients: Iterable[str]) -> IngredientProfile:
    profile = build_default_profile()
    pantry = {item.lower().strip() for item in ingredients if item.strip()}
    return IngredientProfile(
        proteins=profile.proteins.intersection(pantry),
        carbs=profile.carbs.intersection(pantry),
        vegetables=profile.vegetables.intersection(pantry),
        dairy=profile.dairy.intersection(pantry),
        extras=profile.extras.intersection(pantry),
    )


def format_suggestions(recipes: list[Recipe]) -> str:
    if not recipes:
        return "No direct matches yet. Try adding more ingredients."
    lines = []
    for recipe in recipes:
        lines.append(f"- {recipe.name.title()}")
        for step in recipe.instructions:
            lines.append(f"  - {step}")
    return "\n".join(lines)


def main() -> None:
    ingredients = input(
        "Enter ingredients you have (comma-separated), or press Enter to skip: "
    )
    items = [item.strip() for item in ingredients.split(",") if item.strip()]
    recipes = build_default_recipes()
    agent = BreakfastAgent(recipes)
    suggestions = agent.suggest(items)
    print("\nSuggested recipes:")
    print(format_suggestions(suggestions))

    print("\nIngredient profile summary:")
    summary = summarize_ingredients(items)
    print(f"Proteins: {', '.join(sorted(summary.proteins)) or 'none'}")
    print(f"Carbs: {', '.join(sorted(summary.carbs)) or 'none'}")
    print(f"Vegetables: {', '.join(sorted(summary.vegetables)) or 'none'}")
    print(f"Dairy: {', '.join(sorted(summary.dairy)) or 'none'}")
    print(f"Extras: {', '.join(sorted(summary.extras)) or 'none'}")


if __name__ == "__main__":
    main()
