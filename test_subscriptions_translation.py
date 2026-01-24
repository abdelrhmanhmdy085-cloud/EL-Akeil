#!/usr/bin/env python3
"""Test script to verify all translation keys exist in subscriptions.html"""

import json
import re

# Load translation files
with open('src/Frontend/assets/lang/en.json', 'r', encoding='utf-8') as f:
    en_keys = set(json.load(f).keys())

with open('src/Frontend/assets/lang/ar.json', 'r', encoding='utf-8') as f:
    ar_keys = set(json.load(f).keys())

# Read subscriptions.html
with open('src/Frontend/subscriptions.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all data-i18n attributes
pattern = r'data-i18n="([^"]+)"'
html_keys = set(re.findall(pattern, html_content))

print("=" * 60)
print("SUBSCRIPTION TRANSLATION AUDIT")
print("=" * 60)

print(f"\n✓ Total data-i18n attributes found: {len(html_keys)}")
print(f"✓ English translation keys: {len(en_keys)}")
print(f"✓ Arabic translation keys: {len(ar_keys)}")

# Check missing translations
missing_en = html_keys - en_keys
missing_ar = html_keys - ar_keys

if missing_en:
    print(f"\n❌ MISSING IN ENGLISH: {missing_en}")
else:
    print("\n✓ All HTML keys found in English translations")

if missing_ar:
    print(f"\n❌ MISSING IN ARABIC: {missing_ar}")
else:
    print("\n✓ All HTML keys found in Arabic translations")

# List all subscription-related keys
sub_keys = [k for k in html_keys if 'plan' in k or 'subscription' in k or 'benefit' in k or 'faq' in k]
print(f"\n📋 Subscription Keys Used ({len(sub_keys)}):")
for key in sorted(sub_keys):
    status = "✓" if key in en_keys and key in ar_keys else "❌"
    print(f"   {status} {key}")

print("\n" + "=" * 60)
