#!/usr/bin/env python3
"""Парсер рилсов: свои + сохранённые.

Два источника:
  1. Живой Instagram через instaloader (нужна сессия: --login).
  2. Официальный экспорт данных Instagram в JSON (--export путь).

Результат — data/reels.json со списком записей:
  {"source": "own"|"saved", "shortcode", "url", "date", "caption",
   "likes", "views", "author"}
"""
import argparse
import json
import sys
from pathlib import Path

OUT = Path(__file__).parent / "data" / "reels.json"


def record(source, shortcode, date, caption, likes=None, views=None, author=None):
    return {
        "source": source,
        "shortcode": shortcode,
        "url": f"https://www.instagram.com/reel/{shortcode}/" if shortcode else None,
        "date": date,
        "caption": (caption or "").strip(),
        "likes": likes,
        "views": views,
        "author": author,
    }


def scrape_live(user, only, limit):
    import instaloader

    L = instaloader.Instaloader(
        download_pictures=False, download_videos=False,
        download_video_thumbnails=False, save_metadata=False,
        post_metadata_txt_pattern="",
    )
    try:
        L.load_session_from_file(user)
    except FileNotFoundError:
        sys.exit(f"Нет сохранённой сессии. Сначала: python parse_reels.py --login {user}")

    profile = instaloader.Profile.from_username(L.context, user)
    out = []

    if only in ("own", "all"):
        print("Читаю ваши рилсы…")
        for i, post in enumerate(profile.get_posts()):
            if i >= limit:
                break
            if not post.is_video:
                continue
            out.append(record(
                "own", post.shortcode, post.date_utc.isoformat(),
                post.caption, post.likes, post.video_view_count, user,
            ))
            print(f"  own {len(out)}: {post.shortcode}")

    if only in ("saved", "all"):
        print("Читаю сохранённые…")
        n = 0
        for post in profile.get_saved_posts():
            if n >= limit:
                break
            if not post.is_video:
                continue
            n += 1
            out.append(record(
                "saved", post.shortcode, post.date_utc.isoformat(),
                post.caption, post.likes, post.video_view_count,
                post.owner_username,
            ))
            print(f"  saved {n}: {post.shortcode} (@{post.owner_username})")

    return out


def parse_export(export_dir):
    """Разбор официального экспорта Instagram (формат JSON)."""
    root = Path(export_dir)
    out = []

    # Свои рилсы: your_instagram_activity/media/reels.json (или posts)
    for name in ("reels.json", "posts_1.json"):
        for f in root.rglob(name):
            data = json.loads(f.read_text(encoding="utf-8"))
            items = data if isinstance(data, list) else next(
                (v for v in data.values() if isinstance(v, list)), [])
            for item in items:
                media = item.get("media", [item])
                for m in media:
                    title = m.get("title") or item.get("title") or ""
                    ts = m.get("creation_timestamp")
                    out.append(record("own", None, ts, fix_encoding(title)))

    # Сохранённые: saved/saved_posts.json
    for f in root.rglob("saved_posts.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        for item in data.get("saved_saved_media", []):
            title = item.get("title", "")
            href = (item.get("string_map_data", {})
                    .get("Saved on", {}).get("href", ""))
            shortcode = None
            if "/reel/" in href or "/p/" in href:
                shortcode = href.rstrip("/").split("/")[-1]
            rec = record("saved", shortcode, None, "", author=fix_encoding(title))
            rec["url"] = href or rec["url"]
            out.append(rec)

    return out


def fix_encoding(s):
    """Instagram-экспорт кодирует кириллицу как latin-1 mojibake."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--login", metavar="USER", help="создать сессию instaloader и выйти")
    ap.add_argument("--user", help="юзернейм для парсинга (нужна сессия)")
    ap.add_argument("--export", help="путь к распакованному экспорту Instagram")
    ap.add_argument("--only", choices=["own", "saved", "all"], default="all")
    ap.add_argument("--limit", type=int, default=200, help="максимум постов на источник")
    args = ap.parse_args()

    if args.login:
        import instaloader
        L = instaloader.Instaloader()
        L.interactive_login(args.login)
        L.save_session_to_file()
        print("Сессия сохранена. Теперь: python parse_reels.py --user", args.login)
        return

    if args.export:
        out = parse_export(args.export)
    elif args.user:
        out = scrape_live(args.user, args.only, args.limit)
    else:
        ap.error("нужен --user, --export или --login")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nГотово: {len(out)} записей → {OUT}")


if __name__ == "__main__":
    main()
