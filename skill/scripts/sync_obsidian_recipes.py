#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path


USER_DATA = Path.home() / ".codex" / "user-data" / "solo-kitchen"
CONFIG = USER_DATA / "obsidian_sources.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def note_signals(title, text, links):
    lower = text.lower()
    has_ingredients = any(k in text for k in ["材料", "食材", "Ingredients", "ingredients", "核心食材"])
    has_steps = any(k in text for k in ["做法", "步骤", "手順", "作り方", "料理", "先", "然后", "加入", "煎", "炒", "煮", "烤"])
    title_lower = title.lower()
    looks_like_menu = (
        any(k in title for k in ["献立", "菜单"])
        or "menu" in title_lower
        or len(links) >= 3
    )
    looks_like_recipe = has_steps and not looks_like_menu and not ("project" in lower and not has_ingredients)
    return {
        "has_ingredients": has_ingredients,
        "has_steps": has_steps,
        "looks_like_menu": looks_like_menu,
        "looks_like_recipe": looks_like_recipe,
    }


def preview(text, limit=360):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:8])[:limit]


def main():
    config = read_json(CONFIG)
    vault = Path(config["vault_path"]).expanduser()
    recipe_dirs = config.get("recipe_dirs", [])
    index_path = Path(config.get("index_path") or USER_DATA / "obsidian_recipes_index.json").expanduser()

    notes = []
    for recipe_dir in recipe_dirs:
        root = vault / recipe_dir
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            links = sorted(set(re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)))
            stat = path.stat()
            notes.append({
                "title": path.stem,
                "path": str(path),
                "relative_path": str(path.relative_to(vault)),
                "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "size_bytes": stat.st_size,
                "wikilinks": links,
                "signals": note_signals(path.stem, text, links),
                "preview": preview(text),
            })

    index = {
        "version": 1,
        "vault_path": str(vault),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "recipe_dirs": recipe_dirs,
        "notes": notes,
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"indexed {len(notes)} notes -> {index_path}")


if __name__ == "__main__":
    main()
