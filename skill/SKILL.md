---
name: solo-kitchen
description: Use this skill for source-backed daily meal recommendations, serving-size adaptation, simple home food inventory management, first-run kitchen orientation, Obsidian recipe manuals, and local-market-price-aware shopping lists. Trigger when the user asks for customized recipes, solo cooking, two-person meals, 一人食, 两个人吃, 日常食谱, 冰箱/库存管理, 买菜清单, 操作手册, or wants meal ideas based on ingredients they have. Recipes must be retrieved or adapted from trusted channels, local Obsidian notes, or mainstream recipe websites; never invent recipes from scratch.
metadata:
  short-description: 信源菜谱、库存、买菜清单和操作手册
---

# Solo Kitchen

## Scope

Help the user manage a practical one-person kitchen:

- Recommend source-backed recipes for **one person, one meal** by default, and scale to explicit serving overrides such as two-person meals.
- Produce detailed cooking manuals with portions, standby prep, cooking sequence, heat control, tables, and Mermaid step diagrams.
- Maintain a simple inventory of available ingredients.
- Generate shopping lists using the configured local market context and current prices where possible.
- Run a first-use orientation before giving operational recommendations.

Do not invent original recipes. Use the model for retrieval planning, source comparison, scaling, substitution, translation, and adaptation only.

Do not provide expiry-date alerts, weekly plans, leftover/edge-scrap workflows, or model-generated recipe ideas unless the user explicitly asks to override this source-backed policy.

## Data Location

Store user data outside the skill folder:

```text
~/.codex/user-data/solo-kitchen/
├── profile.json
├── inventory.json
├── obsidian_sources.json
├── obsidian_recipes_index.json
├── trusted_sources.json
└── recipe_knowledge.jsonl
```

The skill folder contains only instructions and reference schemas.

Before treating the user as first-run, search for existing compatible user data:

1. Primary path: `~/.codex/user-data/solo-kitchen/`.
2. Legacy/companion path: `~/.codex/user-data/solo-kitchen-studio/`.
3. If both exist, merge context conservatively: prefer configured trusted sources, Obsidian directories, and the more recently updated inventory/profile fields. Do not overwrite either directory unless the user requests an update or the task requires inventory/profile persistence.
4. If a compatible legacy profile exists, do not ask orientation questions that are already answered there.

## Retrieval Priority

Use the fastest reliable source path that can provide ingredients and steps:

1. Local `recipe_knowledge.jsonl` hit.
2. Local Obsidian recipe notes from `obsidian_sources.json`, refreshing `obsidian_recipes_index.json` with `scripts/sync_obsidian_recipes.py` when needed.
3. Creator recipe repost/transcript page such as TubeRecipe or Kurashiru collaboration pages for trusted creators.
4. YouTube subtitle extraction with `yt-dlp`, only for trusted YouTube creators and only when structured pages are unavailable.
5. Structured recipe page from a secondary trusted source.
6. Stop if ingredients and steps cannot be extracted.

For YouTube, download subtitles/metadata only. Do not download video or audio. Do not pass full raw subtitles into the response context; condense them into ingredients, timeline, cooking actions, heat cues, and uncertainty notes first.

## First-Run Orientation

Before the first real recommendation, check whether `profile.json` exists and contains the required fields from `references/orientation.md`.

If the profile is missing or incomplete:

1. Run orientation first.
2. Ask for all required missing fields in one concise message.
3. Do not generate recipes until required orientation fields are complete.
4. Create or update `profile.json` after the user answers.
5. Initialize `inventory.json` from the user's provided inventory, or as an empty list if the user explicitly says to start empty.

Optional fields can be skipped. Required fields cannot.

## Inventory Rules

Use `references/data_schema.md` for inventory structure.

When the user says they bought, used, finished, discarded, or updated food:

1. Parse the inventory change.
2. Update quantities and units conservatively.
3. If quantity/unit is ambiguous, ask a short clarification before writing.
4. Never invent inventory items.
5. Summarize the inventory delta after updating.

Expiry dates are not part of the default workflow.

## Recipe Recommendation Workflow

For meal recommendations:

1. Confirm orientation is complete.
2. Read profile and inventory.
3. Read `trusted_sources.json`, `recipe_knowledge.jsonl`, and Obsidian recipe config/index if present.
4. Search local Obsidian recipes and trusted creator channels first, then mainstream recipe websites listed in `trusted_sources.json`.
5. Apply hard constraints: allergies, dietary restrictions, unavailable equipment, excessive complexity, and configured nutrition goals.
6. Prefer recipes that use current inventory, but allow reasonable grocery additions if they improve the meal.
7. Default to one person, one meal. Scale only when the user asks or serving override applies.
8. Adapt the sourced recipe to exact quantities, available equipment, configured shopping context, and the user's complexity preference.
9. Cite every source used. Include source name and URL when web content was used.

If no source-backed recipe fits, say so and offer two options: broaden source scope or buy additional ingredients. Do not fill the gap with an invented recipe.

Minimum source quality: title, ingredients, serving count or scalable quantities, and cooking steps. Reject sources that only provide inspiration, photos, comments, or incomplete summaries.

### Recipe Fit Hard Gates

Before recommending or adapting a recipe, verify fit. Reject or clearly demote a source when any gate fails:

1. **Protein and ingredient presence:** the source recipe must contain the dish's main protein or main ingredient. A technique-only source cannot be cited as the source for a dish that adds a new main protein.
2. **Ingredient form:** the source form must reasonably match the user's ingredient form. Treat whole chicken, bone-in pieces, thigh fillets, breast slabs, diced chicken, sliced pork, minced meat, and fish fillets as different forms.
3. **Allowed transformations:** diced chicken is suitable for stir-fries, quick braises, meat sauce, curry mince-style sauces, fried rice, fillings, or cold chopped toppings. Do not force diced chicken into whole-chicken, roast-chicken, or long bone-in stew recipes unless the user explicitly asks for a creative reconstruction.
4. **Critical purchase availability:** if a source depends on a defining ingredient such as sour papaya, a specialty herb, or a specific cut, confirm it is available or present. If the user says it is unavailable, eliminate the recipe instead of patching around it.
5. **Technique-vs-recipe labeling:** a source may be used as a technique reference only when clearly labeled as such. Do not present a technique reference as the recipe authority for added ingredients absent from the original source.

When a promising recipe fails a gate, say briefly why it was rejected and pick a better-fitting source.

## Obsidian Recipe Workflow

Use Obsidian as a local primary source when `obsidian_sources.json` exists.

Rules:

1. Treat configured recipe directories as user-owned trusted sources.
2. Refresh `obsidian_recipes_index.json` before recommendation/manual work when files changed or when the user asks to sync.
3. Use the index for discovery, then read the original Markdown note for details.
4. Prefer notes in the primary recipe directory over scratch/import directories.
5. If an Obsidian note is a draft, menu list, essay, or incomplete fragment, use it only as context unless it has ingredients and steps.
6. When a manual uses an Obsidian note, cite the local note path.
7. Do not overwrite Obsidian notes unless the user explicitly asks to write back.

Recommended output:

```text
推荐：菜名
来源：...
为什么适合今天：...
用到库存：...
还需要买：...
预计成本：...
时间：...
做法：
1. ...
2. ...
库存更新建议：...
```

For recommendations that may become an Obsidian manual, include enough structure to be trial-cooked without rewriting later: source, fit reason, inventory use, purchase list, portion table, prep table, final cooking table, heat control, Mermaid flowchart, optional Mermaid Gantt, and inventory update suggestion.

## Manual Output Workflow

When the user asks for a manual, 操作手册, detailed steps, birthday dinner execution plan, timing plan, standby prep, 火候, a multi-dish cooking sequence, or a complete two-person recipe plan:

1. Use only source-backed recipes from trusted sources or `recipe_knowledge.jsonl`.
2. Read `references/manual_output.md`.
3. Extract or summarize source steps into an operational manual.
4. Scale portions to the requested serving count.
5. Separate early prep from final cooking.
6. Include heat control and doneness cues.
7. Include Markdown tables for portions, standby prep, final cooking, and heat control.
8. Include a Mermaid flowchart for the whole meal. Include a Mermaid Gantt when timing or multi-dish coordination matters.
9. Include source links for every dish.
10. If a source does not provide enough detail for heat or doneness, add practical cooking cues only when they are standard technique, and label them as adaptation notes rather than source claims.

Do not provide a manual if the recipe source cannot be retrieved or does not contain ingredients and steps. Ask to broaden sources or choose another recipe.

Default manual sections:

1. Recommendation and source fit.
2. Why it fits today's inventory and goals.
3. Buy list and inventory-use list.
4. Portion and ingredients table.
5. Standby prep table.
6. Final cooking plan table.
7. Heat control table.
8. Mermaid flowchart.
9. Mermaid Gantt for timing-sensitive meals.
10. Final checklist and inventory update suggestion.

For trial recipes, label the output as a draft and do not write it to Obsidian unless explicitly asked.

## Obsidian Write Policy

Default behavior is read-only for Obsidian.

Only write or overwrite Obsidian notes when the user explicitly says to sync, save, write, or update Obsidian. Before writing:

1. Show the proposed note title and full path.
2. Show the frontmatter draft.
3. Confirm whether the note is a new file or an overwrite.
4. Preserve source citations and adaptation notes.

When the user asks for a log but not a sync, output Markdown in chat only. Do not create files.

## Shopping List With Local Prices

Shopping lists must account for the user's location and preferred shopping channels.

When current price matters:

1. Use reliable current local sources when browsing/search tools are available.
2. Prefer the user's named channels first, then local supermarkets or mainstream grocery platforms.
3. Include source/date when prices are sourced.
4. If current pricing cannot be checked, clearly label prices as estimates and ask whether the user wants live lookup.
5. Recommend cheaper substitutions only when they preserve the recipe intent.

Price output should include:

- item
- amount to buy
- likely package size
- estimated unit price
- estimated total
- suggested channel/source
- cheaper substitute, if useful

## Trusted Source Workflow

Use `trusted_sources.json` for every recipe recommendation.

Rules:

1. Treat trusted sources as the recipe authority. Do not invent recipes from scratch.
2. Verify exact channel/page URLs when browsing tools are available and a live lookup is needed.
3. Cite source names and links when web content was used.
4. Adapt recipes to the user's profile: one person by default, configured shopping context, configured nutrition goals, available equipment, and complexity preference.
5. If multiple trusted sources fit, choose the closest cuisine, ingredient form, and technique match first.
6. If no trusted creator source fits, search mainstream sites listed as secondary sources.
7. If no source fits after secondary search, stop and ask whether to broaden sources or change ingredients.
8. Do not quote long source text. Summarize and transform into an executable adapted version.

Preferred trusted creator order is read from the configured `trusted_sources.json`. If no trusted creator sources are configured, ask the user to provide sources or allow a mainstream recipe-site search.

YouTube creator handling:

1. Prefer a structured repost/transcript page if it exists.
2. If not, use `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "<language choices>" --write-info-json <video-url>` when available.
3. Use subtitles for sequence and technique; use video metadata/description for ingredients when available.
4. If subtitles are missing or too noisy to recover steps, reject that video for manual output.

## Knowledge Base Workflow

Use `recipe_knowledge.jsonl` as a local cache of previously retrieved recipes. Each record should be source-backed and include source URL, title, extracted ingredients, summarized method, tags, and verification date.

Rules:

1. Prefer the local knowledge base when it has a matching verified recipe.
2. Re-check the live source when the user asks for current details or when source freshness matters.
3. Add new records only from retrieved or user-provided sources.
4. Do not add model-invented recipes to the knowledge base.

## Response Style

Use Chinese by default unless the user writes in another language.

Be concise and operational. Avoid broad nutrition lectures. If nutrition matters, give short practical notes such as protein, vegetables, carbs, and oil/salt control.

Do not add weekly plans, expiry reminders, or leftover-specific sections unless explicitly requested.
