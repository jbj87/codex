# Breakfast Multimodal Agent Starter

This starter kit provides a lightweight multimodal agent skeleton that helps
suggest breakfast recipes based on ingredients you have on hand. The initial
implementation is rule-based but includes a placeholder for integrating a
vision model to detect ingredients from a fridge photo.

## Features

- Suggests breakfast recipes based on ingredient matches.
- Summarizes available ingredients by category.
- Includes a stub for vision-based ingredient recognition.

## Getting Started

```bash
python -m src.breakfast_agent
```

Enter a comma-separated list of ingredients when prompted.

## Multimodal Upgrade Path

The `VisionIngredientRecognizer` class is a placeholder. Replace its `detect`
method with a call to a multimodal model (for example, a vision-capable LLM)
that returns ingredient labels from an input image. Combine those labels with
user-provided ingredient lists before calling `BreakfastAgent.suggest`.
