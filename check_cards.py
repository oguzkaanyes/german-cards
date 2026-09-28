#!/usr/bin/env python3
"""Checks for cards.json (see rules.md).

  python3 check_cards.py WORD [WORD ...]   which words are already in cards.json
  python3 check_cards.py --validate        validate every card against the rules
"""
import json
import re
import sys
from pathlib import Path

CARDS = Path(__file__).with_name("cards.json")
LANGS = ["de", "tr", "en", "uk", "ar", "it"]
TYPES = {"noun", "verb", "adjective", "adverb", "phrase"}
SOURCES = {"notes", "book"}


def normalize(text):
    """Comparable key: lowercase, no article or 'sich', umlauts spelled out, single spaces."""
    t = text.strip().lower()
    t = re.sub(r"^(der|die|das)\s+", "", t)
    t = re.sub(r"^sich\s+", "", t)
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    return re.sub(r"[\s-]+", " ", t).strip()


def load():
    return json.loads(CARDS.read_text(encoding="utf-8"))["cards"]


def check_words(words):
    index = {}
    for c in load():
        # The plural is matched too, in case a word from the photo was not reduced to its singular.
        keys = {normalize(c.get("word", "")), normalize(c.get("id", "").replace("-", " "))}
        if c.get("plural"):
            keys.add(normalize(c["plural"]))
        for key in keys:
            index.setdefault(key, []).append(c)

    new = 0
    for w in words:
        hits = index.get(normalize(w), [])
        if hits:
            found = ", ".join(
                f"{c['id']} ({c.get('source')}, {c.get('type')}{', ' + c['article'] if c.get('article') else ''}, {c.get('date')})"
                for c in hits
            )
            print(f"VAR   {w}  ->  {found}")
        else:
            new += 1
            print(f"YENİ  {w}")
    print(f"\n{len(words)} kelime: {new} yeni, {len(words) - new} zaten var")


def validate():
    cards = load()
    errors, ids = [], set()
    for c in cards:
        i = c.get("id")
        if not i or not re.fullmatch(r"[a-z0-9-]+", i):
            errors.append(f"{i}: id geçersiz")
        if i in ids:
            errors.append(f"{i}: id tekrar ediyor")
        ids.add(i)
        if c.get("source") not in SOURCES:
            errors.append(f"{i}: source geçersiz (notes/book olmalı)")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c.get("date") or ""):
            errors.append(f"{i}: date eksik/hatalı")
        if c.get("type") not in TYPES:
            errors.append(f"{i}: type geçersiz")
        if c.get("type") == "noun" and c.get("article") not in ("der", "die", "das"):
            errors.append(f"{i}: isimde article yok")
        if c.get("type") != "noun" and c.get("article") is not None:
            errors.append(f"{i}: isim olmayan kartta article var")
        for field in ("meaning", "example"):
            for lang in LANGS:
                if not (c.get(field) or {}).get(lang):
                    errors.append(f"{i}: {field}.{lang} eksik")
        if c.get("type") == "verb":
            forms = c.get("forms") or {}
            for k in ("praesens", "praeteritum", "perfekt"):
                if not forms.get(k):
                    errors.append(f"{i}: forms.{k} eksik")
            if not c.get("note"):
                errors.append(f"{i}: fiilde note (Rektion) eksik")
        elif "forms" in c:
            errors.append(f"{i}: fiil olmayan kartta forms var")
        if c.get("reflexive") != c.get("word", "").startswith("sich "):
            errors.append(f"{i}: reflexive ile word uyuşmuyor")

    # Same word written twice under different ids (e.g. "Rahmen" and "rahmen-2"), in either list.
    seen = {}
    for c in cards:
        key = (normalize(c.get("word", "")), c.get("type"))
        if key in seen:
            errors.append(f"{c.get('id')}: aynı kelime zaten var ({seen[key]})")
        seen.setdefault(key, c.get("id"))

    print(f"{len(cards)} kart kontrol edildi")
    print("\n".join(errors) or "Hata yok")
    return not errors


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--validate"]:
        sys.exit(0 if validate() else 1)
    if not args or args[0].startswith("-"):
        print(__doc__.strip())
        sys.exit(2)
    check_words(args)
