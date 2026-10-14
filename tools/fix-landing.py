#!/usr/bin/env python3
"""Kotak Wayang landing fixes: perf, contrast, a11y, slop, semantics.
Idempotent-ish: asserts each expected token found. Run from repo root.
"""
import re, sys, os

P = "index.html"
s = open(P, encoding="utf-8").read()
orig = s


def sub(old, new, count=1, label=""):
    global s
    n = s.count(old)
    assert n == count, f"[{label}] expected {count} occurrence(s), found {n}: {old[:70]!r}"
    s = s.replace(old, new)
    print(f"  ok  {label}")


# ─────────────── 1. ASSET REFERENCES → webp ───────────────
print("1) asset refs")
s = re.sub(r"BrandLogo/(\d+)\.png", r"BrandLogo/\1.webp", s)
s = re.sub(r"images-testimoni/([A-Za-z0-9]+)\.png", r"images-testimoni/\1.webp", s)
print("  ok  BrandLogo/*.webp + images-testimoni/*.webp")

sub('src="img-logo/KW-3D.png"', 'src="img-logo/KW-3D.webp"', 1, "footer logo webp")
sub('src="img-logo/KW-icon.png"', 'src="img-logo/KW-icon.webp"', 1, "nav logo webp")
sub('content="image/png"', 'content="image/webp"', 1, "og:image:type")
sub('content="https://kotakwayangstudio.vercel.app/img-logo/kwtumbnail.png"',
    'content="https://kotakwayangstudio.vercel.app/img-logo/kwtumbnail.png"', 2, "og/twitter image keep png")


# ─────────────── 2. PRELOAD HERO CRITICALS ───────────────
print("2) preload")
sub('    <link rel="preconnect" href="https://fonts.googleapis.com" />',
    '''    <link rel="preload" as="image" href="img-logo/KW-icon.webp" type="image/webp" fetchpriority="high" />
    <link rel="preload" as="image" href="images-testimoni/C1.webp" type="image/webp" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />''', 1, "preload hero assets")


# ─────────────── 3. CONTRAST TOKENS ───────────────
print("3) contrast")
sub("""            --primary-violet: #8B5CF6;
            --primary-dark: #7C3AED;
            --secondary-pink: #F472B6;""",
    """            --primary-violet: #8B5CF6;
            --primary-dark: #7C3AED;
            --primary-deep: #6D28D9;
            --secondary-pink: #F472B6;
            --secondary-pink-deep: #DB2777;""", 1, "add deep tokens")

sub("""        .btn-candy {
            background: var(--primary-violet);
            color: var(--surface-white);""",
    """        .btn-candy {
            background: var(--primary-dark);
            color: var(--surface-white);""", 1, "btn-candy 5.7:1")

sub("""        .cta-banner {
            background: var(--primary-violet);""",
    """        .cta-banner {
            background: var(--primary-dark);""", 1, "cta-banner 5.7:1")

sub("""        .service-card:nth-child(1) .service-icon-wrapper {
            background: var(--secondary-pink);""",
    """        .service-card:nth-child(1) .service-icon-wrapper {
            background: var(--secondary-pink-deep);""", 1, "service icon 1")

sub("""        .process-card:nth-child(2) .process-step-pill {
            background: var(--secondary-pink);""",
    """        .process-card:nth-child(2) .process-step-pill {
            background: var(--secondary-pink-deep);""", 1, "process pill 2")

sub("""        .why-card:nth-child(4) .why-icon {
            background: var(--secondary-pink);""",
    """        .why-card:nth-child(4) .why-icon {
            background: var(--secondary-pink-deep);""", 1, "why icon 4")

sub("""        .modal-close:hover {
            background: var(--secondary-pink);""",
    """        .modal-close:hover {
            background: var(--secondary-pink-deep);""", 1, "modal close hover")

sub('style="background:var(--secondary-pink); color:white;"',
    'style="background:var(--secondary-pink-deep); color:white;"', 1, "pill END-TO-END")

sub('style="background:var(--primary-violet); color:white;"',
    'style="background:var(--primary-deep); color:white;"', 2, "pills SEAMLESS/BUILT")

# floating sticker white-on-pink handled by --secondary-pink-deep above
sub("""            bottom: 15px;
            left: -15px;
            background: var(--secondary-pink);""",
    """            bottom: 15px;
            left: -15px;
            background: var(--secondary-pink-deep);""", 1, "sticker-sales contrast")


# ─────────────── 4. FONT SIZES (11px floor) ───────────────
print("4) font sizes")
FIX = [
    # (line-anchored unique context, old, new, label)
    ("        .trusted-brand-item .brand-name {\n            font-family: var(--font-heading);\n            font-weight: 700;\n            font-size: 0.62rem;", "font-size: 0.62rem;", "font-size: 0.78rem;", "brand-name desktop"),
    ("        .testimonial-gallery-name {\n            font-family: var(--font-heading);\n            font-weight: 800;\n            font-size: 0.65rem;", "font-size: 0.65rem;", "font-size: 0.8rem;", "tst-name desktop"),
    ("        .testimonial-gallery-company {\n            font-size: 0.55rem;", "font-size: 0.55rem;", "font-size: 0.72rem;", "tst-company desktop"),
]
for ctx, old, new, label in FIX:
    assert ctx in s, f"ctx missing {label}"
    at = s.index(ctx)
    s = s[:at] + s[at:].replace(old, new, 1)
    print(f"  ok  {label}")

# generic sweep: any remaining < 0.72rem clamp to 0.72rem (11.5px)
before_n = len(re.findall(r"font-size:\s*0\.(?:[0-6]\d|7[01])rem", s))
s = re.sub(r"font-size:\s*0\.(?:[0-6]\d|7[01])rem", "font-size: 0.72rem", s)
print(f"  ok  swept {before_n} sub-11.5px sizes")


# ─────────────── 5. ICON-TILE-STACK → side-by-side + nested card borders ───────────────
print("5) icon tile stack / nested cards")
sub("""        .service-card {
            display: flex;
            flex-direction: column;
            height: 100%;
            padding: 1.5rem;
        }

        .service-icon-wrapper {
            width: 50px;
            height: 50px;
            border: 2px solid var(--border-dark);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            box-shadow: 3px 3px 0px var(--border-dark);
        }""",
    """        .service-card {
            display: grid;
            grid-template-columns: auto 1fr;
            column-gap: 0.9rem;
            align-items: center;
            height: 100%;
            padding: 1.5rem;
        }
        .service-card > .service-title {
            align-self: center;
            margin: 0;
        }
        .service-card > .service-desc {
            grid-column: 1 / -1;
            margin-top: 0.75rem;
        }

        .service-icon-wrapper {
            width: 50px;
            height: 50px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 3px 3px 0px var(--border-dark);
        }""", 1, "service-card grid")

sub("""            transition: transform var(--transition-bounce), box-shadow var(--transition-bounce);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }""",
    """            transition: transform var(--transition-bounce), box-shadow var(--transition-bounce);
            display: grid;
            grid-template-columns: auto 1fr;
            column-gap: 0.9rem;
            align-items: center;
        }
        .why-card > .why-card-desc {
            grid-column: 1 / -1;
            margin-top: 0.6rem;
        }""", 1, "why-card grid")

sub("""        .why-icon {
            width: 60px;
            height: 60px;
            border: 2px solid var(--border-dark);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 3px 3px 0px var(--border-dark);
            flex-shrink: 0;
            margin-bottom: 0.25rem;
        }""",
    """        .why-icon {
            width: 44px;
            height: 44px;
            border: 2px solid var(--border-dark);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 3px 3px 0px var(--border-dark);
            flex-shrink: 0;
        }""", 1, "why-icon size")

sub("""        .why-card-title {
            font-size: 1.1rem;
            margin: 0.25rem 0 0.1rem;
        }""",
    """        .why-card-title {
            font-size: 1.1rem;
            margin: 0;
        }""", 1, "why title margin")

sub("""            .why-card {
                padding: 0.7rem 0.5rem;
            }
            .why-icon {
                width: 36px;
                height: 36px;
            }
            .why-icon svg {
                width: 16px;
                height: 16px;
            }
            .why-card-title {
                font-size: 0.8rem;
            }
            .why-card-desc {
                font-size: 0.72rem;
            }""",
    """            .why-card {
                padding: 0.7rem 0.5rem;
                column-gap: 0.6rem;
            }
            .why-icon {
                width: 36px;
                height: 36px;
            }
            .why-icon svg {
                width: 16px;
                height: 16px;
            }
            .why-card-title {
                font-size: 0.8rem;
                text-align: left;
            }
            .why-card-desc {
                font-size: 0.72rem;
                text-align: left;
            }""", 1, "why-card mobile")


# ─────────────── 7. DUPLICATE SOCIAL-PROOF H2 ───────────────
print("7) duplicate H2")
sub("""                    <div class="pill-badge" style="background:var(--mint-green); color:var(--fg-slate);">OUR CLIENTS</div>
                    <h2 class="section-title">Trusted By</h2>""",
    """                    <div class="pill-badge" style="background:var(--mint-green); color:var(--fg-slate);">OUR CLIENTS</div>
                    <h2 class="section-title">Brands We've Worked With</h2>""", 1, "unique H2 #trusted")


# ─────────────── 8-10. modal a11y / dynamic img / js: done manually via patch tool ───────────────
print("8-10) modal a11y / imgs / js (manual)")


open(P, "w", encoding="utf-8").write(s)
print(f"\ndone. {len(orig)} -> {len(s)} bytes")
