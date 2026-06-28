# Orientation Requirements

Run this before the first operational use of the skill.

## Required Fields

Collect these fields before generating recipes or shopping lists:

```json
{
  "location": {
    "country_or_region": "",
    "city": "",
    "district_or_area": ""
  },
  "shopping_channels": [],
  "budget": {
    "default_per_meal": "",
    "currency": ""
  },
  "dietary_constraints": {
    "allergies": [],
    "medical_or_religious_restrictions": [],
    "ingredients_to_avoid": []
  },
  "taste_preferences": {
    "liked_cuisines_or_flavors": [],
    "disliked_cuisines_or_flavors": [],
    "spice_level": ""
  },
  "cooking_setup": {
    "available_equipment": [],
    "staple_seasonings": []
  },
  "time_and_effort": {
    "usual_max_minutes": "",
    "complexity_preference": "",
    "cleanup_tolerance": "low | medium | high"
  },
  "initial_inventory_policy": "provided | start_empty"
}
```

## Optional Fields

Ask only if useful or if the user volunteers information:

```json
{
  "body_profile": {
    "sex": "",
    "age": "",
    "height_cm": "",
    "weight_kg": "",
    "body_context": ""
  },
  "serving_overrides": [],
  "nutrition_goals": [],
  "meal_times": [],
  "preferred_protein_sources": [],
  "preferred_carb_sources": [],
  "food_texture_preferences": [],
  "notes": ""
}
```

## First Message Template

Ask for missing required information in one message:

```text
第一次使用前我需要先补齐厨房档案。请按下面几项回答即可：

1. 你在哪个城市/区域买菜？
2. 常用买菜渠道是什么？比如菜市场、超市、生鲜电商、本地配送平台等。
3. 一顿饭默认预算多少？币种是什么？
4. 有过敏、忌口、宗教/医疗限制吗？
5. 喜欢和不喜欢的口味/菜系是什么？能吃辣到什么程度？
6. 你有哪些厨具？有哪些常备调料？
7. 平时一顿饭希望控制在多少分钟内？步骤复杂度和洗锅洗碗接受度如何？
8. 初始库存要现在录入，还是先从空库存开始？
```

Do not ask about expiry reminders, weekly planning, or leftovers by default.
