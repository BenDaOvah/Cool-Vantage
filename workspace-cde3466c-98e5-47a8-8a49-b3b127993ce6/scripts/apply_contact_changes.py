#!/usr/bin/env python3
"""Apply the hero-image swap + Contact Us rebuild across the static site."""
import glob
import re

PUB = "/home/z/my-project/public"
EMAIL = "info@coolvantageac.com"
report = []


def sub_in_file(path, pairs):
    html = open(path, encoding="utf-8").read()
    changed = []
    for old, new in pairs:
        if old in html:
            html = html.replace(old, new)
            changed.append(old[:60].replace("\n", " ") + " ...")
        elif new in html:
            changed.append("(already applied) " + new[:50])
        else:
            changed.append("!! NOT FOUND: " + old[:60])
    open(path, "w", encoding="utf-8").write(html)
    report.append((path, changed))


pages = [p for p in glob.glob(f"{PUB}/**/index.html", recursive=True)]

# --- 1) Global label changes on every page -------------------------------
for p in pages:
    subs = [
        # Contact tab -> Contact Us (header nav + footer link)
        ('href="/contact/">Contact</a>', 'href="/contact/">Contact Us</a>'),
        # Mobile action bar + CTA band buttons -> Contact us
        ('href="/contact/">Schedule service</a>', 'href="/contact/">Contact us</a>'),
        # Footer: add email under the phone (NAP consistency)
        ('<a href="tel:+14079206955">(407) 920-6955</a><br><span>Apopka, Florida',
         f'<a href="tel:+14079206955">(407) 920-6955</a><br>'
         f'<a href="mailto:{EMAIL}">{EMAIL}</a><br><span>Apopka, Florida'),
    ]
    sub_in_file(p, subs)

# --- 2) Home page: hero image swap + hero secondary button ----------------
sub_in_file(
    f"{PUB}/home/index.html",
    [
        ('src="/manus-storage/async-images/gCkQnNpfBvR2fZIoARb74h/image-1.webp"',
         'src="/assets/images/cool-vantage-hero.webp"'),
        ('href="/contact/">Schedule service <span>↗</span>',
         'href="/contact/">Contact us <span>↗</span>'),
    ],
)

# --- 3) Services hub: inquiry wording ------------------------------------
sub_in_file(
    f"{PUB}/services/index.html",
    [('href="/contact/">Call or send a service inquiry →',
      'href="/contact/">Get in touch →')],
)

# --- 4) Privacy page: form references -> phone/email wording -------------
sub_in_file(
    f"{PUB}/privacy/index.html",
    [
        ("Information submitted through a contact form is used to respond to "
         "the inquiry and is not sold as a mailing list.",
         "Information you share by phone or email is used to respond to your "
         "inquiry and is not sold as a mailing list."),
        ("If you contact the company through this site, the information you "
         "provide—such as your name, phone number, email address, location, "
         "and service details—may be used to respond.",
         "If you contact the company by phone or email, the information you "
         "provide—such as your name, phone number, email address, location, "
         "and service details—may be used to respond."),
    ],
)

# --- 5) Report ------------------------------------------------------------
for path, changes in report:
    name = path.replace(PUB + "/", "")
    flags = "".join("✓" if not c.startswith("!!") else "✗" for c in changes)
    print(f"{flags} {name}: {len(changes)} edits")

print("\nHero refs still pointing at old image-1 (expected: 3 other pages):")
for p in pages:
    html = open(p, encoding="utf-8").read()
    if "image-1.webp" in html:
        print("  -", p.replace(PUB + "/", ""))
