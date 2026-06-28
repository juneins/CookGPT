# Data Schemas

Store personal data in `~/.codex/user-data/solo-kitchen/`.

## profile.json

```json
{
  "version": 1,
  "default_serving": {
    "people": 1,
    "meals": 1,
    "serving_overrides": []
  },
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
  "optional": {
    "body_profile": {
      "sex": "",
      "age": "",
      "height_cm": "",
      "weight_kg": "",
      "body_context": ""
    },
    "nutrition_goals": [],
    "meal_times": [],
    "preferred_protein_sources": [],
    "preferred_carb_sources": [],
    "food_texture_preferences": [],
    "notes": ""
  }
}
```

## inventory.json

```json
{
  "version": 1,
  "items": [
    {
      "name": "",
      "category": "vegetable | fruit | meat | seafood | egg_dairy | staple | seasoning | drink | frozen | other",
      "quantity": 0,
      "unit": "",
      "storage": "room_temp | fridge | freezer | other",
      "purchase_date": "",
      "notes": ""
    }
  ]
}
```

`purchase_date` is optional context only. Do not use it for expiry reminders unless the user explicitly asks.

## trusted_sources.json

```json
{
  "version": 1,
  "source_policy": {
    "default_recommendation_mode": "source_backed_only",
    "forbid_model_generated_recipes": true,
    "use_trusted_sources_for_every_recommendation": true,
    "fallback_when_no_source_match": "ask_to_broaden_sources_or_change_ingredients",
    "require_citations_when_using_web": true,
    "verify_urls_before_citing": true,
    "retrieval_priority": [
      "recipe_knowledge",
      "structured_recipe_page",
      "creator_repost_or_transcript_page",
      "youtube_subtitles_with_ytdlp",
      "stop_if_incomplete"
    ]
  },
  "sources": [
    {
      "name": "",
      "platform": "YouTube | website | book | other",
      "language": "",
      "url": "",
      "trust_level": "primary | secondary",
      "cuisine_or_style": [],
      "notes": ""
    }
  ]
}
```

Use `url: ""` until the exact channel/page has been verified or provided by the user.

## obsidian_sources.json

```json
{
  "version": 1,
  "vault_path": "",
  "primary_recipe_dir": "",
  "recipe_dirs": [],
  "index_path": "",
  "sync_policy": {
    "refresh_before_recommendation": true,
    "read_original_note_for_manual": true,
    "write_back_requires_explicit_user_request": true
  },
  "notes": ""
}
```

## obsidian_recipes_index.json

Generated index. Do not edit manually.

```json
{
  "version": 1,
  "vault_path": "",
  "generated_at": "",
  "recipe_dirs": [],
  "notes": [
    {
      "title": "",
      "path": "",
      "relative_path": "",
      "mtime": "",
      "size_bytes": 0,
      "wikilinks": [],
      "signals": {
        "has_ingredients": false,
        "has_steps": false,
        "looks_like_menu": false,
        "looks_like_recipe": false
      },
      "preview": ""
    }
  ]
}
```

## recipe_knowledge.jsonl

One JSON object per line. Store only source-backed recipes.

```json
{
  "version": 1,
  "source": {
    "name": "",
    "platform": "",
    "url": "",
    "verified_date": "YYYY-MM-DD",
    "retrieval_method": "recipe_knowledge | structured_recipe_page | creator_repost_or_transcript_page | youtube_subtitles_with_ytdlp | user_provided"
  },
  "recipe": {
    "title": "",
    "original_servings": "",
    "ingredients": [],
    "method_summary": [],
    "heat_control_notes": [],
    "standby_prep_notes": [],
    "tags": [],
    "complexity": "low | medium | high",
    "equipment": []
  },
  "extraction_quality": {
    "has_ingredients": true,
    "has_steps": true,
    "has_heat_cues": true,
    "uncertainty_notes": []
  },
  "adaptation_notes": {
    "suitable_for_user": true,
    "one_person_adjustment": "",
    "nutrition_notes": "",
    "inventory_matches": [],
    "shopping_needed": []
  }
}
```

Do not store copied full recipe text. Store concise extracted facts and adaptation notes.

## Inventory Update Examples

User: `我买了 6 个鸡蛋、2 个番茄、一盒牛奶`

Expected update:

```json
{
  "items_added_or_updated": [
    {"name": "鸡蛋", "quantity": 6, "unit": "个"},
    {"name": "番茄", "quantity": 2, "unit": "个"},
    {"name": "牛奶", "quantity": 1, "unit": "盒"}
  ]
}
```

User: `今晚用了两个鸡蛋和一个番茄`

Expected update:

```json
{
  "items_decremented": [
    {"name": "鸡蛋", "quantity": 2, "unit": "个"},
    {"name": "番茄", "quantity": 1, "unit": "个"}
  ]
}
```
