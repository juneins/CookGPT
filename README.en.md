# CookGPT

[中文说明](README.md)

A solo cooking skill for developers who keep forgetting dinner is a thing.

CookGPT looks for recipes from sources you trust, then turns them into a one-person cooking plan based on your pantry, tools, taste, budget, and time. Not a mood-board recipe. Not a vague "cook until done" summary. Something you can actually follow while standing in the kitchen.

## Why this exists

I made CookGPT because deciding what to eat after a full day of coding is weirdly exhausting.

Takeout is easy, until your body starts filing complaints. Cooking is not that hard either, but the small decisions pile up: what to buy, how much to buy, what is already in the fridge, whether the recipe is reliable, how to scale a four-person recipe down to one, whether your pan is big enough, and whether half an onion is about to become fridge archaeology.

CookGPT tries to take some of that friction out.

You give it a kitchen profile and your current inventory. It finds source-backed recipes, scales them down, writes the shopping list, lays out the prep, explains the heat, and tells you what to update in inventory after dinner.

## Who this is for

- vibe coders, developers, designers, and makers living alone
- indie hackers, one-person companies (OPCs), and tiny-team founders
- people who want fewer takeout nights without making cooking a second job
- beginners who are still figuring out what "medium heat" means
- people with goals like fat loss, muscle gain, lower sugar, allergies, or food restrictions
- anyone who mostly cooks for one, but occasionally needs to turn it into dinner for two or something a little more date-night friendly

This project is not trying to turn you into a chef. Think of it more like a kitchen ops assistant: fewer decisions, less waste, a better chance of eating a real meal.

## What it does

### Starts from trusted recipes

CookGPT does not make up recipes by default. It tries to work from:

- locally cached, verified recipes
- your Obsidian recipe notes
- trusted YouTube creators
- recipe pages with clear ingredients and steps
- any other sources you explicitly add to `trusted_sources.json`

If a page is just photos, comments, vibes, or missing the actual steps, it should not be treated as a real recipe source.

### Turns recipes into kitchen instructions

Plenty of recipes are tasty. Fewer are easy to cook from.

CookGPT breaks a recipe into:

- one-person ingredient amounts
- prep work
- the order of actions once the stove is on
- heat level for each step
- doneness cues
- a shopping list
- a Mermaid flowchart

For a multi-dish meal, it can also plan the timing. Do the things that can sit first. Leave seafood, steak, pasta, and other fussy stuff closer to serving time.

### Keeps a simple inventory

You can say:

```text
I bought 6 eggs, 2 tomatoes, and a bag of spinach.
```

Or:

```text
I used 2 eggs and 1 tomato tonight.
```

CookGPT keeps a basic kitchen inventory and uses it when suggesting recipes. The point is to avoid starting from zero every time, and to stop random leftovers from quietly dying in the fridge.

### Handles YouTube recipes

Some of the best recipes are buried in videos. Videos are great for learning, but terrible when your hands are wet and you need to rewind 17 seconds.

CookGPT can use subtitles and metadata from trusted YouTube creators to extract ingredients, sequence, heat cues, and key moves. By default, it only downloads subtitles and metadata. No video or audio.

If the subtitles are too messy or the recipe cannot be recovered clearly, it should stop instead of filling in the blanks with plausible nonsense.

### Adapts to your actual kitchen

Only have a rice cooker? One pan? No oven? Hate washing dishes today? Put that in your profile.

You can also add health and diet goals: fat loss, muscle gain, high protein, less oil, less salt, lower sugar, allergies, religious restrictions, ingredients you dislike.

CookGPT can use those constraints when picking and scaling recipes. It is not a doctor or dietitian. It is for everyday meal execution, not medical advice.

## A small example

It is 8:30 PM. A Vibe Coder closes the editor after a day of prompts, bugs, and too many tabs. The problem is not philosophical. He is hungry.

He tells CookGPT:

```text
I have eggs, tomatoes, spinach, frozen shrimp, and rice.
I want a one-person dinner tonight. High protein, light on oil, done in 30 minutes, and ideally not too many dishes.
```

CookGPT should not just answer: "make tomato shrimp egg rice."

A useful response would:

- pick a recipe or technique with a real source
- scale it down to one person
- mark what inventory gets used and what is missing
- set the order: thaw shrimp, wash spinach, cut tomato, beat eggs
- explain the stove rhythm: cook tomato until saucy, stop shrimp once it turns opaque, do not overcook the eggs
- give heat cues: medium heat for tomato, lower heat to reduce, short cook time for shrimp
- generate a flowchart
- suggest the inventory update: eggs -2, tomato -1, shrimp -100g, spinach -1 handful

The dish name is not the main thing. The point is turning "what should I eat right now?" into a small set of actions.

## Setup

User data lives outside the skill folder. Create the data directory first:

```bash
mkdir -p ~/.codex/user-data/solo-kitchen/
```

Then copy the templates:

```bash
cp user-data-template/* ~/.codex/user-data/solo-kitchen/
```

The templates are:

```text
user-data-template/
├── profile.json
├── inventory.json
├── trusted_sources.json
├── obsidian_sources.json
├── obsidian_recipes_index.json
└── recipe_knowledge.jsonl
```

### profile.json

This is your kitchen profile. At minimum, fill in:

- where you shop for groceries
- your usual grocery channels
- default meal budget
- allergies, restrictions, and foods you avoid
- flavors and cuisines you like or dislike
- spice tolerance
- available equipment
- pantry seasonings
- how long you usually want to spend cooking
- how much complexity you can tolerate
- cleanup tolerance
- health goals, if any

The default serving is one person, one meal:

```json
{
  "default_serving": {
    "people": 1,
    "meals": 1
  }
}
```

### inventory.json

This is your current kitchen inventory. It can start empty:

```json
{
  "version": 1,
  "items": []
}
```

You do not need to log everything at once. Add things as you buy them. Subtract things as you cook.

### trusted_sources.json

This is where your recipe sources live.

They can be YouTube channels, recipe sites, books, your own notes, or anything else you trust. CookGPT should search these first.

If you do not want a site used, add it to the exclude list:

```json
{
  "name": "example source",
  "url_pattern": "example.com",
  "reason": "Do not use this as a trusted recipe source"
}
```

### obsidian_sources.json

If you keep recipes in Obsidian, configure your vault and recipe folders here.

The default policy is read-only. CookGPT should not write back to Obsidian unless you explicitly ask it to save, sync, or update notes.

### recipe_knowledge.jsonl

This is the local recipe cache.

Use it for verified recipe summaries: source, URL, verification date, ingredients, method summary, heat notes, and one-person adaptation notes.

Do not paste full recipe articles into it. Do not store recipes the model invented on the spot.

## Things you can ask

```text
Use solo-kitchen to recommend a one-person meal from my inventory. Include a shopping list and a flowchart.
```

```text
I have 30 minutes tonight. I want something high protein, low cleanup, and based on what I already have.
```

```text
Turn this YouTube recipe into a one-person cooking manual.
```

## Boundaries

CookGPT has a few hard rules:

- no made-up recipes by default
- use trusted sources first
- default to one person, one meal
- check real inventory before recommending
- keep user data outside the skill folder
- no weekly planning, leftover workflows, or expiry reminders unless asked
- no medical or dietitian-style advice

If there is not enough source material, it should ask whether to broaden the source scope instead of pretending it knows.

## Repo layout

```text
.
├── skill/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── user-data-template/
│   ├── profile.json
│   ├── inventory.json
│   ├── trusted_sources.json
│   ├── obsidian_sources.json
│   ├── obsidian_recipes_index.json
│   └── recipe_knowledge.jsonl
├── LICENSE
├── README.md
└── README.en.md
```

## License

MIT License. See [`LICENSE`](LICENSE).
