#!/usr/bin/env python3
"""Выжимка идей из спарсенных рилсов через Claude API.

Читает data/reels.json (результат parse_reels.py), для каждого рилса
формулирует главную идею / формат / хук, затем делает общую сводку:
повторяющиеся темы и что переиспользовать на Архстоянии 2026
(тема фестиваля: «Маршрут перестроен», стройка арт-объекта).

Нужен: export ANTHROPIC_API_KEY=...
"""
import json
import os
import sys
from pathlib import Path

import anthropic

DATA = Path(__file__).parent / "data" / "reels.json"
OUT = Path(__file__).parent / "data" / "ideas_from_my_reels.md"
MODEL = "claude-sonnet-5"
BATCH = 30  # рилсов на один запрос

SYSTEM = (
    "Ты — продюсер коротких видео. Тебе дают спарсенные рилсы (caption, "
    "статистика). По каждому сформулируй по-русски: 1) главную идею одной "
    "фразой; 2) формат (влог, туториал, бэкстейдж, тренд, storytime…); "
    "3) хук — чем цепляет первые 2 секунды. Пиши сжато, маркдауном."
)

FINAL = (
    "Ниже — разборы всех рилсов (моих и сохранённых). Сделай сводку:\n"
    "1. Топ-5 повторяющихся тем и форматов.\n"
    "2. Что из этого заходит лучше всего (по лайкам/просмотрам).\n"
    "3. Как переиспользовать эти форматы на фестивале Архстояние 2026 "
    "(Никола-Ленивец, тема «Маршрут перестроен», я строю арт-объект) — "
    "5–7 конкретных идей рилсов в моём стиле.\n"
)


def fmt(r):
    stats = f"{r.get('likes') or '?'} лайков, {r.get('views') or '?'} просмотров"
    return (f"- [{r['source']}] @{r.get('author') or 'me'} ({stats})\n"
            f"  caption: {r['caption'][:600] or '(без текста)'}")


def ask(client, prompt, system=SYSTEM):
    resp = client.messages.create(
        model=MODEL, max_tokens=4000, system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Задайте ANTHROPIC_API_KEY")
    if not DATA.exists():
        sys.exit(f"Нет {DATA} — сначала запустите parse_reels.py")

    reels = json.loads(DATA.read_text(encoding="utf-8"))
    client = anthropic.Anthropic()
    sections = []

    for i in range(0, len(reels), BATCH):
        chunk = reels[i:i + BATCH]
        print(f"Разбираю рилсы {i + 1}–{i + len(chunk)} из {len(reels)}…")
        prompt = "Разбери эти рилсы:\n\n" + "\n".join(fmt(r) for r in chunk)
        sections.append(ask(client, prompt))

    print("Делаю общую сводку…")
    summary = ask(client, FINAL + "\n\n" + "\n\n".join(sections), system=None)

    OUT.write_text(
        "# Идеи из моих рилсов\n\n## Сводка\n\n" + summary +
        "\n\n## Разбор по рилсам\n\n" + "\n\n".join(sections) + "\n",
        encoding="utf-8",
    )
    print(f"Готово → {OUT}")


if __name__ == "__main__":
    main()
