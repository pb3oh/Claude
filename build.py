#!/usr/bin/env python3
"""Static site generator for idyourself.com modern redesign.

Produces a directory-based URL tree matching the real idyourself.com paths:

  /                                       (home)
  /about-us/                              (about)
  /meet-the-crew/                         (team)
  /join-our-team/                         (careers)
  /policies/                              (policies)
  /blog/                                  (blog)
  /contact-us/                            (contact)
  /services/                              (services hub)
  /services/custom-apparel/
  /services/company-merch/
  /services/incentives-and-gifts/
  /services/warehousing-and-custom-kitting/
  /services/online-stores/
  /services/creative-services/
  /services/large-format-printing/
  /services/print-collateral-and-packaging/
  /pay-online/                            (external-style info page)

Run:  python3 build.py
"""

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent

# Base URL path the site is served from.
# GitHub Pages project site: "/Claude"
# Root domain (e.g. idyourself.com): ""
BASE = "/Claude"

def u(path: str) -> str:
    """Prefix a site-absolute path with BASE. Pass-through for external URLs and anchors."""
    if path.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
        return path
    if not path.startswith('/'):
        return path
    return BASE + path if BASE else path

# ---------------------------------------------------------------------------
# Company data
# ---------------------------------------------------------------------------
PHONE_DISPLAY = "877-303-1049"
PHONE_TEL     = "+18773031049"
EMAIL         = "info@idyourself.com"
ADDRESS_HTML  = (
    "PO Box 432<br/>"
    "6146 N Croatan Hwy<br/>"
    "Kitty Hawk, NC 27949"
)
SHOP_URL      = "https://shop.idyourself.com/"

# ---------------------------------------------------------------------------
# Navigation definition (matches the real idyourself.com top menu)
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    ("Home",         "/",               "home"),
    ("About",        "/about-us/",      "about"),
    ("What We Do",   "/services/",      "services"),
    ("News + Blog",  "/blog/",          "blog"),
    ("Shop",         SHOP_URL,          "shop"),
    ("Contact",      "/contact-us/",    "contact"),
]

SERVICES = [
    ("custom-apparel",                  "Custom Apparel"),
    ("company-merch",                   "Company Merch"),
    ("incentives-and-gifts",            "Incentives &amp; Gifts"),
    ("warehousing-and-custom-kitting",  "Warehousing &amp; Custom Kitting"),
    ("online-stores",                   "Online Stores"),
    ("creative-services",               "Creative Services"),
    ("large-format-printing",           "Large Format Printing"),
    ("print-collateral-and-packaging",  "Print Collateral &amp; Packaging"),
]

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
def nav_html(current_key: str) -> str:
    links = []
    for label, url, key in NAV_ITEMS:
        attrs = ''
        if key == current_key:
            attrs = ' aria-current="page"'
        target = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
        links.append(f'<a href="{url}"{target}{attrs}>{label}</a>')
    return (
        '<nav class="nav__links" aria-label="Primary">\n        '
        + '\n        '.join(links) +
        '\n      </nav>'
    )

def header_html(current_key: str) -> str:
    return dedent(f"""\
      <header class="nav" data-nav>
        <div class="nav__inner container">
          <a class="brand" href="/">
            <span class="brand__mark" aria-hidden="true">id</span>
            <span class="brand__word"><b>id</b>entifyyourself</span>
          </a>
          {nav_html(current_key)}
          <div class="nav__cta">
            <a class="btn btn--accent" href="/pay-online/">Pay Online</a>
            <a class="btn btn--solid" href="/contact-us/#quote">Get started <span aria-hidden="true">&rarr;</span></a>
          </div>
          <button class="nav__burger" aria-label="Open menu" data-burger><span></span><span></span><span></span></button>
        </div>
      </header>
    """)

def service_footer_links() -> str:
    out = []
    for slug, label in SERVICES[:6]:
        out.append(f'        <a href="/services/{slug}/">{label}</a>')
    return '\n'.join(out)

def footer_html() -> str:
    return dedent(f"""\
      <footer class="footer">
        <div class="container footer__grid">
          <div class="footer__brand">
            <a class="brand brand--light" href="/">
              <span class="brand__mark" aria-hidden="true">id</span>
              <span class="brand__word"><b>id</b>entifyyourself</span>
            </a>
            <p>Branded. Marketing. Solutions. Family-owned on the Outer Banks &mdash; serving brands nationwide since 2003.</p>
          </div>
          <div class="footer__col">
            <h4>What We Do</h4>
    {service_footer_links()}
            <a href="/services/">See all services</a>
          </div>
          <div class="footer__col">
            <h4>Company</h4>
            <a href="/about-us/">About</a>
            <a href="/meet-the-crew/">Meet the Crew</a>
            <a href="/join-our-team/">Join Our Team</a>
            <a href="/policies/">Policies</a>
            <a href="/blog/">News &amp; Blog</a>
            <a href="{SHOP_URL}" target="_blank" rel="noopener">Shop &#8599;</a>
          </div>
          <div class="footer__col footer__col--contact">
            <h4>Contact</h4>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
            <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
            <p>{ADDRESS_HTML}</p>
            <p>Mon &ndash; Fri &middot; 8:30a &ndash; 5p ET</p>
          </div>
        </div>
        <div class="container footer__bar">
          <span>&copy; <span data-year></span> Identify Yourself, LLC &middot; All rights reserved</span>
          <span><a href="/policies/">Policies</a> &middot; <a href="/contact-us/">Contact</a></span>
        </div>
      </footer>
    """)

HEAD_TPL = dedent("""\
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>{title}</title>
      <meta name="description" content="{desc}" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
      <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="/assets/css/styles.css" />
    </head>
    <body class="theme-dark">
      <a class="skip" href="#main">Skip to content</a>
""")

TAIL_TPL = dedent("""\
      <script src="/assets/js/main.js" defer></script>
    </body>
    </html>
""")

def _apply_base(html: str) -> str:
    if not BASE:
        return html
    return (
        html
        .replace('href="/', f'href="{BASE}/')
        .replace('src="/', f'src="{BASE}/')
    )

def render(path: str, title: str, desc: str, current: str, body: str) -> None:
    """Write a single page to disk at `path` (directory). The page becomes {path}/index.html."""
    html = (
        HEAD_TPL.format(title=title, desc=desc) +
        header_html(current) +
        '  <main id="main">\n' +
        body +
        '\n  </main>\n' +
        footer_html() +
        TAIL_TPL
    )
    html = _apply_base(html)
    p = ROOT / path.strip('/')
    p.mkdir(parents=True, exist_ok=True)
    (p / 'index.html').write_text(html, encoding='utf-8')
    print('wrote', path + 'index.html' if path.endswith('/') else path + '/index.html')

def render_root(title: str, desc: str, current: str, body: str) -> None:
    """Special case: home page writes to /index.html."""
    html = (
        HEAD_TPL.format(title=title, desc=desc) +
        header_html(current) +
        '  <main id="main">\n' +
        body +
        '\n  </main>\n' +
        footer_html() +
        TAIL_TPL
    )
    html = _apply_base(html)
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    print('wrote /index.html')

# ---------------------------------------------------------------------------
# Page body helpers
# ---------------------------------------------------------------------------
def page_hero(eyebrow: str, headline_html: str, lede_html: str) -> str:
    return dedent(f"""\
        <section class="page-hero">
          <div class="container">
            <p class="eyebrow" data-reveal><span class="dot"></span> {eyebrow}</p>
            <h1 class="display" data-reveal>{headline_html}</h1>
            <p class="lede" data-reveal>{lede_html}</p>
          </div>
        </section>
    """)

def cta_band(headline_html: str, primary_label: str, primary_href: str,
             secondary_label: str = "", secondary_href: str = "") -> str:
    secondary = ''
    if secondary_label:
        secondary = f'<a href="{secondary_href}" class="btn btn--link">{secondary_label} <span aria-hidden="true">&rarr;</span></a>'
    return dedent(f"""\
        <section class="cta section">
          <div class="container cta__inner">
            <h2 class="display" data-reveal>{headline_html}</h2>
            <div class="cta__actions" data-reveal>
              <a href="{primary_href}" class="btn btn--accent btn--lg">{primary_label}</a>
              {secondary}
            </div>
          </div>
        </section>
    """)

def related_services(exclude_slug: str) -> str:
    tiles = []
    for slug, label in SERVICES:
        if slug == exclude_slug:
            continue
        tiles.append(
            f'<a class="svc" href="/services/{slug}/" data-reveal>'
            f'<div class="svc__num">&rarr;</div>'
            f'<h3>{label}</h3>'
            f'<span class="svc__link">Explore <span aria-hidden="true">&rarr;</span></span>'
            f'</a>'
        )
    return dedent(f"""\
        <section class="services section">
          <div class="container">
            <div class="section__head">
              <div class="section__eyebrow" data-reveal><span class="num">&mdash;</span> More from Identify Yourself</div>
              <h2 class="h-display" data-reveal>Related <em>services</em></h2>
            </div>
            <div class="services__grid">
              {''.join(tiles)}
            </div>
          </div>
        </section>
    """)

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
HOME_BODY = dedent("""\
    <section class="hero">
      <div class="container hero__inner">
        <p class="eyebrow" data-reveal><span class="dot"></span> Branded. Marketing. Solutions.</p>
        <h1 class="hero__wordmark" data-reveal>
          <span class="line"><b>id</b>entify</span>
          <span class="line">yourself<span class="accent-dot">.</span></span>
        </h1>
        <p class="lede" data-reveal>Custom apparel, company merch, creative + print &mdash; sourced, designed and delivered from our Outer Banks studio since 2003.</p>
        <div class="hero__cta" data-reveal>
          <a href="/contact-us/#quote" class="btn btn--accent btn--lg">Start a project</a>
          <a href="/services/" class="btn btn--link">See what we do <span aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </section>

    <section class="marquee" aria-hidden="true">
      <div class="marquee__track">
        <span>Custom Apparel</span><span>&bull;</span>
        <span>Company Merch</span><span>&bull;</span>
        <span>Incentives &amp; Gifts</span><span>&bull;</span>
        <span>Warehousing &amp; Kitting</span><span>&bull;</span>
        <span>Online Stores</span><span>&bull;</span>
        <span>Creative Services</span><span>&bull;</span>
        <span>Large Format Printing</span><span>&bull;</span>
        <span>Print &amp; Packaging</span><span>&bull;</span>
        <span>Custom Apparel</span><span>&bull;</span>
        <span>Company Merch</span><span>&bull;</span>
        <span>Incentives &amp; Gifts</span><span>&bull;</span>
        <span>Warehousing &amp; Kitting</span><span>&bull;</span>
      </div>
    </section>

    <section class="services section">
      <div class="container">
        <div class="section__head">
          <div class="section__eyebrow" data-reveal><span class="num">01</span> What we do</div>
          <h2 class="h-display" data-reveal>One team. <em>Every</em> branded touchpoint.</h2>
          <p class="section__lede" data-reveal>From a single tee to a nationwide company store, we run the whole play &mdash; sourcing, design, production, warehousing, shipping.</p>
        </div>
        <div class="services__grid">
""") + ''.join(
    f'          <a class="svc" href="/services/{slug}/" data-reveal>'
    f'<div class="svc__num">{i+1:02d}</div>'
    f'<h3>{label}</h3>'
    f'<span class="svc__link">Explore <span aria-hidden="true">&rarr;</span></span>'
    f'</a>\n'
    for i, (slug, label) in enumerate(SERVICES)
) + dedent("""\
        </div>
      </div>
    </section>

    <section class="feature section">
      <div class="container feature__grid">
        <div class="feature__copy">
          <div class="section__eyebrow" data-reveal><span class="num">02</span> Who we are</div>
          <h2 class="h-display" data-reveal>Family-owned on the <em>Outer Banks</em>. Shipping nationwide.</h2>
          <p data-reveal>We&rsquo;re a small, senior crew that treats every order like our name is on the box &mdash; because it is. No middlemen, no surprise fees, no missed dates.</p>
          <a href="/about-us/" class="btn btn--solid" data-reveal>About Identify Yourself <span aria-hidden="true">&rarr;</span></a>
        </div>
        <figure class="feature__visual" data-reveal>
          <div class="feature__card">
            <div class="chip">By the numbers</div>
            <div class="feature__meta">
              <span>Founded</span><strong>2003</strong>
              <span>Home base</span><strong>Kitty Hawk, NC</strong>
              <span>Service model</span><strong>Full-service</strong>
              <span>Ship coverage</span><strong>All 50 states</strong>
              <span>Programs run</span><strong>Apparel, merch, print, stores</strong>
              <span>Promise</span><strong>On-brand, on-time</strong>
            </div>
          </div>
        </figure>
      </div>
    </section>
""") + cta_band(
    "Have a brief?<br/>Let&rsquo;s <em>make it</em>.",
    "Request a quote", "/contact-us/#quote",
    "Or call 877-303-1049", "tel:+18773031049"
)

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
ABOUT_BODY = page_hero(
    "About",
    "Branded. Marketing.<br/><em>Solutions.</em>",
    "Identify Yourself is a family-owned, full-service branded merchandise company based on the Outer Banks of North Carolina. Since 2003 we&rsquo;ve been helping teams show up in the world with work that looks like them."
) + dedent("""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">Small shop. <em>Big</em> shop floor.</h2>
          <p>We started Identify Yourself with a simple idea: branded merch deserves the same craft and care as the campaign it supports. Two decades later we&rsquo;re still proving it &mdash; one tee, one mug, one kitted welcome box at a time.</p>
          <p>Our clients range from local Outer Banks favorites to national brands running coast-to-coast employee programs. What they share is a preference for direct quotes, real samples and a partner who picks up the phone.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Full-service means <span class="accent">full</span>-service.</h2>
          <p>Sourcing, design, decoration, warehousing, kitting, fulfillment &mdash; it all lives under one roof. That means no finger-pointing, no surprise handoffs, and no &ldquo;let me loop in my vendor&rdquo; emails.</p>
          <p>Need a company store? Built in-house. Need a 50-SKU swag closet shipped on demand? Running already. Need a large-format banner for tomorrow&rsquo;s grand opening? Press is warm.</p>
        </div>
      </section>
    </div>

    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="values">
          <div class="value" data-reveal>
            <div class="num">01</div>
            <h3>Branded.</h3>
            <p>We obsess over how the logo sits, how the garment feels, how the kit opens. Taste is a strategy.</p>
          </div>
          <div class="value" data-reveal>
            <div class="num">02</div>
            <h3>Marketing.</h3>
            <p>Merch is a medium. We design programs that earn wear time, shelf space, and real brand lift.</p>
          </div>
          <div class="value" data-reveal>
            <div class="num">03</div>
            <h3>Solutions.</h3>
            <p>One partner from brief to doorstep. You call, we answer, it ships.</p>
          </div>
        </div>
      </div>
    </section>
""") + cta_band(
    "Want to meet the <em>crew</em>?",
    "Meet the crew", "/meet-the-crew/",
    "Or join the crew", "/join-our-team/"
)

# ---------------------------------------------------------------------------
# MEET THE CREW
# ---------------------------------------------------------------------------
TEAM_BODY = page_hero(
    "Meet the Crew",
    "The people<br/>behind the <em>press</em>.",
    "A small, senior team of sourcing, design, production and fulfillment pros &mdash; all under one roof in Kitty Hawk, NC."
) + dedent("""\
    <div class="container">
      <section class="values" style="margin-top:2rem;">
        <div class="value" data-reveal>
          <div class="num">&mdash;</div>
          <h3>Leadership</h3>
          <p>Second-generation ownership. Still answering the phones, still walking the shop floor every day.</p>
        </div>
        <div class="value" data-reveal>
          <div class="num">&mdash;</div>
          <h3>Account + Project</h3>
          <p>Your day-to-day partners. Senior enough to make the call, hands-on enough to catch the detail.</p>
        </div>
        <div class="value" data-reveal>
          <div class="num">&mdash;</div>
          <h3>Creative + Production</h3>
          <p>In-house designers, decorators and fulfillment techs. If we touch it, we own it.</p>
        </div>
      </section>
    </div>
""") + cta_band(
    "Like what you see?<br/><em>Join us.</em>",
    "See open roles", "/join-our-team/"
)

# ---------------------------------------------------------------------------
# JOIN OUR TEAM
# ---------------------------------------------------------------------------
CAREERS_BODY = page_hero(
    "Careers",
    "Come make <em>cool stuff</em><br/>on the Outer Banks.",
    "We&rsquo;re always curious to meet makers, production pros, designers and account folks who care about the craft as much as we do."
) + dedent(f"""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">What it&rsquo;s like here.</h2>
          <p>Small crew, big shop floor, first-name basis with everyone. You&rsquo;ll work directly with clients and with the press. Your ideas get built, not shelved.</p>
          <p>We value curiosity, ownership and plain-spoken communication. Titles matter less than the work.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Open <span class="accent">roles</span>.</h2>
          <p>We hire when the right person shows up. If any of these sound like you, send a note &mdash; we&rsquo;ll make time.</p>
          <ul class="list">
            <li>Account + Program Management</li>
            <li>Production + Decoration</li>
            <li>Warehouse + Kitting</li>
            <li>Design + Creative</li>
            <li>E-commerce + Online Stores</li>
          </ul>
          <p><a class="btn btn--solid" href="mailto:{EMAIL}?subject=Careers%20at%20Identify%20Yourself">Email us your story <span aria-hidden="true">&rarr;</span></a></p>
        </div>
      </section>
    </div>
""") + cta_band(
    "Prefer to chat <em>live</em>?",
    "Call 877-303-1049", f"tel:{PHONE_TEL}",
    f"Or email {EMAIL}", f"mailto:{EMAIL}"
)

# ---------------------------------------------------------------------------
# POLICIES
# ---------------------------------------------------------------------------
POLICIES_BODY = page_hero(
    "Policies",
    "Plain-English<br/><em>policies</em>.",
    "Terms, privacy, returns and ordering expectations &mdash; all in one place."
) + dedent("""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">Ordering &amp; quotes</h2>
          <p>Every project starts with a written quote. Prices include decoration, setup and standard ground freight unless noted. Artwork proofs are required before production begins.</p>
          <h2 class="h-display" style="margin-top:2rem;">Turnaround</h2>
          <p>Standard turnaround is 10&ndash;14 business days after proof approval. Rush available on most projects &mdash; just ask.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Returns &amp; <span class="accent">remakes</span></h2>
          <p>Custom-decorated goods are not resalable, so we don&rsquo;t accept returns for buyer&rsquo;s remorse. If we made a mistake &mdash; wrong art, wrong color, defective goods &mdash; we remake it, full stop.</p>
          <h2 class="h-display" style="margin-top:2rem;">Privacy</h2>
          <p>We only collect the information needed to quote, produce and ship your order. We don&rsquo;t sell data. We don&rsquo;t share client lists.</p>
        </div>
      </section>
    </div>
""") + cta_band(
    "Questions about a <em>specific</em> policy?",
    "Contact us", "/contact-us/"
)

# ---------------------------------------------------------------------------
# BLOG
# ---------------------------------------------------------------------------
BLOG_POSTS = [
    ("Merch that actually gets worn", "A field guide to picking garments people keep in the rotation."),
    ("Building a company store that scales", "Lessons from running 80+ programs &mdash; and what we&rsquo;d tell a first-timer."),
    ("Kitting, done right", "Why the unboxing matters as much as the swag inside."),
    ("Print isn&rsquo;t dead &mdash; it&rsquo;s just better", "Paper stocks, finishes and the small touches that elevate collateral."),
    ("Sustainable sourcing, without the greenwash", "What to ask your promo partner before you order anything &lsquo;eco.&rsquo;"),
    ("Large format, done fast", "How we turn tradeshow banners in 48 hours (and when you shouldn&rsquo;t)."),
]

BLOG_BODY = page_hero(
    "News + Blog",
    "Notes from<br/>the <em>shop floor</em>.",
    "Ideas, case studies and the occasional press-break rant. No fluff."
) + dedent("""\
    <section class="section" style="padding-top:2rem;">
      <div class="container">
        <div class="blog-grid">
""") + ''.join(
    f'          <article class="blog-card" data-reveal>\n'
    f'            <div class="blog-card__chip">Journal</div>\n'
    f'            <h3>{title}</h3>\n'
    f'            <p>{excerpt}</p>\n'
    f'            <a href="/contact-us/" class="blog-card__link">Ask about this <span aria-hidden="true">&rarr;</span></a>\n'
    f'          </article>\n'
    for title, excerpt in BLOG_POSTS
) + dedent("""\
        </div>
      </div>
    </section>
""") + cta_band(
    "Got a <em>story idea</em>?",
    "Pitch us", "/contact-us/"
)

# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------
CONTACT_BODY = page_hero(
    "Contact",
    "Let&rsquo;s make<br/><em>something</em>.",
    "Quote requests, project briefs, quick hellos &mdash; all welcome. We reply within one business day, usually faster."
) + dedent(f"""\
    <div class="container">
      <section class="contact-grid" id="quote">
        <form class="quote-form" data-reveal data-quote-form>
          <div class="row">
            <div class="field">
              <label for="name">Your name</label>
              <input id="name" name="name" required autocomplete="name" />
            </div>
            <div class="field">
              <label for="company">Company</label>
              <input id="company" name="company" autocomplete="organization" />
            </div>
          </div>
          <div class="row">
            <div class="field">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" required autocomplete="email" />
            </div>
            <div class="field">
              <label for="phone">Phone (optional)</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" />
            </div>
          </div>
          <div class="row">
            <div class="field">
              <label for="service">What can we help with?</label>
              <select id="service" name="service">
                <option>Custom Apparel</option>
                <option>Company Merch</option>
                <option>Incentives &amp; Gifts</option>
                <option>Warehousing &amp; Kitting</option>
                <option>Online Stores</option>
                <option>Creative Services</option>
                <option>Large Format Printing</option>
                <option>Print Collateral &amp; Packaging</option>
                <option>Not sure yet</option>
              </select>
            </div>
            <div class="field">
              <label for="budget">Estimated budget</label>
              <select id="budget" name="budget">
                <option>Under $2.5k</option>
                <option>$2.5k &ndash; $10k</option>
                <option>$10k &ndash; $50k</option>
                <option>$50k+</option>
                <option>Not sure</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="brief">Tell us about the project</label>
            <textarea id="brief" name="brief" placeholder="Audience, timeline, quantities, goals &mdash; anything you have so far."></textarea>
          </div>
          <div class="submit">
            <button type="submit" class="btn btn--accent btn--lg">Send the brief <span aria-hidden="true">&rarr;</span></button>
            <small>We reply within one business day.</small>
          </div>
        </form>

        <aside class="contact-info" data-reveal>
          <div class="block">
            <h3>General</h3>
            <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
            <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
            <p>Mon &ndash; Fri &middot; 8:30a &ndash; 5p ET</p>
          </div>
          <div class="block">
            <h3>Studio</h3>
            <p>{ADDRESS_HTML}</p>
          </div>
          <div class="block">
            <h3>Shop online</h3>
            <p><a href="{SHOP_URL}" target="_blank" rel="noopener">shop.idyourself.com &#8599;</a></p>
            <p>Stock Outer Banks gear, ready to ship.</p>
          </div>
          <div class="block">
            <h3>Pay an invoice</h3>
            <p><a href="/pay-online/">Pay online &rarr;</a></p>
          </div>
        </aside>
      </section>
    </div>
""") + cta_band(
    "Prefer a <em>call</em>?<br/>So do we.",
    PHONE_DISPLAY, f"tel:{PHONE_TEL}",
    EMAIL, f"mailto:{EMAIL}"
)

# ---------------------------------------------------------------------------
# PAY ONLINE
# ---------------------------------------------------------------------------
PAY_BODY = page_hero(
    "Pay Online",
    "Pay an <em>invoice</em>,<br/>the easy way.",
    "Secure online payment for Identify Yourself invoices. Have your invoice number handy."
) + dedent(f"""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">How it works</h2>
          <ol class="list list--ordered">
            <li>Grab the invoice number from your PDF or email.</li>
            <li>Click the pay button and enter your details on our secure portal.</li>
            <li>You&rsquo;ll get a receipt by email within minutes.</li>
          </ol>
          <p><a class="btn btn--accent btn--lg" href="mailto:{EMAIL}?subject=Pay%20Online%20%E2%80%94%20Invoice%20">Request pay link <span aria-hidden="true">&rarr;</span></a></p>
          <p><small>Don&rsquo;t have your invoice? <a href="mailto:{EMAIL}">Email billing</a> and we&rsquo;ll resend it.</small></p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Other ways to <span class="accent">pay</span></h2>
          <p><strong>ACH / Wire:</strong> Preferred for orders over $5k. Ask us for bank details.</p>
          <p><strong>Check:</strong> Payable to Identify Yourself, LLC. Mail to:</p>
          <p>{ADDRESS_HTML}</p>
          <p><strong>Net terms:</strong> Available for approved accounts &mdash; ask your account manager.</p>
        </div>
      </section>
    </div>
""") + cta_band(
    "Need a <em>hand</em> with billing?",
    f"Email {EMAIL}", f"mailto:{EMAIL}",
    PHONE_DISPLAY, f"tel:{PHONE_TEL}"
)

# ---------------------------------------------------------------------------
# SERVICES HUB
# ---------------------------------------------------------------------------
SERVICES_HUB_BODY = page_hero(
    "What We Do",
    "Eight ways we<br/>put your brand <em>to work</em>.",
    "Apparel, merch, print, creative, warehousing, online stores &mdash; all in-house, all accountable to one team."
) + dedent("""\
    <section class="services section">
      <div class="container">
        <div class="services__grid">
""") + ''.join(
    f'          <a class="svc" href="/services/{slug}/" data-reveal>'
    f'<div class="svc__num">{i+1:02d}</div>'
    f'<h3>{label}</h3>'
    f'<span class="svc__link">Explore <span aria-hidden="true">&rarr;</span></span>'
    f'</a>\n'
    for i, (slug, label) in enumerate(SERVICES)
) + dedent("""\
        </div>
      </div>
    </section>
""") + cta_band(
    "Not sure which fits?<br/><em>We&rsquo;ll help.</em>",
    "Request a quote", "/contact-us/#quote",
    "Or call 877-303-1049", f"tel:{PHONE_TEL}"
)

# ---------------------------------------------------------------------------
# SERVICE DETAIL PAGES
# ---------------------------------------------------------------------------
SERVICE_CONTENT = {
    "custom-apparel": {
        "title": "Custom Apparel",
        "eyebrow": "Custom Apparel",
        "headline": "Tees, hoodies,<br/>hats &mdash; <em>elevated</em>.",
        "lede": "Screen print, embroidery, DTG, patches, heat transfer &mdash; we match the decoration to the garment, not the other way around.",
        "what": "From a single run of team tees to a full seasonal apparel program, we source the right blank, decorate it in-house, and ship it sized and packed the way you need.",
        "how": "We start with fit and feel &mdash; the garment has to be something people want to wear. Then we spec the decoration: screen print for punchy color, embroidery for logos that last, DTG for complex art in small runs.",
        "bullets": [
            "Screen printing &mdash; plastisol, water-based, discharge",
            "Embroidery &mdash; flat, 3D puff, appliqu&eacute;, patches",
            "DTG + DTF for short runs and photo-real art",
            "Soft-hand heat transfers and numbered athleticwear",
            "Premium brands: Comfort Colors, Champion, Carhartt, District, Bella+Canvas &mdash; plus mills on request",
        ],
    },
    "company-merch": {
        "title": "Company Merch",
        "eyebrow": "Company Merch",
        "headline": "Merch that <em>earns</em><br/>its place in the drawer.",
        "lede": "Thoughtful, on-brand swag that people actually keep. Drinkware, tech, bags, office, headwear &mdash; curated and custom-sourced.",
        "what": "We curate merch programs for employee onboarding, events, customer gifting and everyday brand presence. Every item is sourced with the logo, the audience and the use case in mind.",
        "how": "Tell us the brief &mdash; we come back with a tight short list of options, real samples on request, and one quote that includes decoration and freight. No mystery SKUs.",
        "bullets": [
            "Drinkware, bags, tech, office, outdoor, headwear",
            "Sustainable and recycled options on request",
            "In-house decoration &mdash; laser, pad print, screen, embroidery",
            "Kitting + branded packaging available",
            "Nationwide shipping, same day for rush",
        ],
    },
    "incentives-and-gifts": {
        "title": "Incentives & Gifts",
        "eyebrow": "Incentives &amp; Gifts",
        "headline": "Gifts that say<br/><em>thank you</em>, loud and clear.",
        "lede": "Client gifts, employee milestones, VIP sends &mdash; custom curated, beautifully packaged, delivered on the day you want.",
        "what": "From a single executive gift to a 2,000-person sales incentive program, we design the experience end-to-end &mdash; product, packaging, note card, delivery window.",
        "how": "Budget, audience, occasion, tone. Give us those and we&rsquo;ll come back with tiered options. Approve, we build, we ship.",
        "bullets": [
            "Tiered gift programs (bronze/silver/gold)",
            "Custom boxes, branded wrap, handwritten-style notes",
            "On-demand sends for new hires, closed deals, anniversaries",
            "Gift card fulfillment, denomination-matched",
            "Global shipping for distributed teams",
        ],
    },
    "warehousing-and-custom-kitting": {
        "title": "Warehousing & Custom Kitting",
        "eyebrow": "Warehousing &amp; Custom Kitting",
        "headline": "Your merch closet,<br/>run like a <em>warehouse</em>.",
        "lede": "We hold the inventory, pick the kits, print the slips, ship the boxes &mdash; so you don&rsquo;t have to.",
        "what": "Pallets come into our Outer Banks facility and leave as branded kits on your schedule. SKU-level visibility, on-demand reorders, real humans on the account.",
        "how": "We set up the SKUs, photograph everything, put it behind a private portal or online store, and fulfill orders as they come in. You get reports, we get it out the door.",
        "bullets": [
            "SKU intake, photography, bin management",
            "Custom kit assembly &mdash; welcome boxes, event kits, VIP sends",
            "Print-on-demand collateral inserts",
            "Private storefronts or API-fed order drops",
            "Returns + restocking handled in-house",
        ],
    },
    "online-stores": {
        "title": "Online Stores",
        "eyebrow": "Online Stores",
        "headline": "A branded <em>store</em><br/>without the headaches.",
        "lede": "Company stores, fundraiser shops, event merch sites &mdash; built, hosted and fulfilled end-to-end by us.",
        "what": "We build and run private company stores and public-facing fundraiser / event sites. Orders come in, we pick / produce / ship, you get the reporting.",
        "how": "Two flavors: <em>on-demand</em> (no inventory, produced per order) and <em>pre-buy</em> (we hold stock, ship same-day). We&rsquo;ll help you pick based on volume and SKU mix.",
        "bullets": [
            "Private employee stores with SSO / allowance codes",
            "Public pop-up stores for events + fundraisers",
            "On-demand or held-stock fulfillment",
            "Integrated decoration &mdash; no external vendors",
            "Clear reporting: orders, spend, top SKUs",
        ],
    },
    "creative-services": {
        "title": "Creative Services",
        "eyebrow": "Creative Services",
        "headline": "In-house <em>creative</em><br/>that understands production.",
        "lede": "Logo work, brand systems, campaign art, packaging design &mdash; designed with the decoration method already in mind.",
        "what": "Our designers don&rsquo;t hand off files that can&rsquo;t be printed. Every piece of creative we produce is ready for the press it&rsquo;s going to.",
        "how": "Brief, moodboard, concepts, refinement, production-ready files. Simple, predictable, fast.",
        "bullets": [
            "Logo design + brand identity systems",
            "Merch line design and campaign art",
            "Packaging + box art",
            "Sales collateral and pitch decks",
            "Production-ready files: Pantone-specced, press-ready",
        ],
    },
    "large-format-printing": {
        "title": "Large Format Printing",
        "eyebrow": "Large Format Printing",
        "headline": "Big prints.<br/>Big <em>presence</em>.",
        "lede": "Banners, signs, wall graphics, window clings, tradeshow displays &mdash; fast turns from our in-house presses.",
        "what": "Indoor and outdoor large-format for events, retail, wayfinding and brand installations. UV-stable inks, rigid and flexible substrates.",
        "how": "Send the art (or we&rsquo;ll design it). We proof, print, finish and ship &mdash; or deliver and install locally on the Outer Banks.",
        "bullets": [
            "Vinyl banners, mesh banners, pole banners",
            "Rigid signs: coroplast, PVC, aluminum, Dibond",
            "Wall and window graphics, floor decals",
            "Tradeshow + retractable displays",
            "48-hour rush on most pieces",
        ],
    },
    "print-collateral-and-packaging": {
        "title": "Print Collateral & Packaging",
        "eyebrow": "Print Collateral &amp; Packaging",
        "headline": "Print with a <em>point of view</em>.",
        "lede": "Brochures, business cards, lookbooks, branded boxes, hang-tags, stickers &mdash; offset and digital from a press-side team.",
        "what": "Short-run and long-run print for every touchpoint that leaves your office. Specialty stocks, finishes, die-cuts and embellishments welcome.",
        "how": "We&rsquo;ll help you spec stock, finish and bindery based on the job. Expect real press proofs on anything that matters.",
        "bullets": [
            "Business cards, letterhead, envelopes",
            "Brochures, lookbooks, sales sheets, postcards",
            "Custom mailer and shipper boxes",
            "Labels, stickers, hang-tags, belly bands",
            "Foil, emboss, spot UV, die-cut, soft-touch",
        ],
    },
}

def service_body(slug: str) -> str:
    d = SERVICE_CONTENT[slug]
    bullets = '\n'.join(f'            <li>{b}</li>' for b in d['bullets'])
    return page_hero(d['eyebrow'], d['headline'], d['lede']) + dedent(f"""\
        <div class="container">
          <section class="about-grid">
            <div data-reveal>
              <div class="section__eyebrow"><span class="num">01</span> What we do</div>
              <h2 class="h-display">{d['title']}, <em>end-to-end</em>.</h2>
              <p>{d['what']}</p>
              <h2 class="h-display" style="margin-top:2rem;">How it works</h2>
              <p>{d['how']}</p>
            </div>
            <div data-reveal>
              <div class="section__eyebrow"><span class="num">02</span> Capabilities</div>
              <h2 class="h-display" style="color: var(--cream);">What&rsquo;s <span class="accent">included</span>.</h2>
              <ul class="list">
    {bullets}
              </ul>
              <p style="margin-top:1.5rem;"><a class="btn btn--accent" href="/contact-us/#quote">Quote this service <span aria-hidden="true">&rarr;</span></a></p>
            </div>
          </section>
        </div>
    """) + related_services(slug) + cta_band(
        f"Ready to brief a <em>{d['title'].lower()}</em> project?",
        "Request a quote", "/contact-us/#quote",
        f"Or call {PHONE_DISPLAY}", f"tel:{PHONE_TEL}"
    )

# ---------------------------------------------------------------------------
# DRIVER
# ---------------------------------------------------------------------------
def build() -> None:
    render_root(
        "Identify Yourself &mdash; Branded. Marketing. Solutions.",
        "Custom apparel, company merch, creative and print from a family-owned, full-service branded merchandise team on the Outer Banks of NC since 2003.",
        "home", HOME_BODY,
    )
    render("/about-us/",
        "About &mdash; Identify Yourself",
        "Identify Yourself is a family-owned full-service branded merchandise company based on the Outer Banks of NC. Here&rsquo;s who we are.",
        "about", ABOUT_BODY)
    render("/meet-the-crew/",
        "Meet the Crew &mdash; Identify Yourself",
        "Meet the small, senior crew behind Identify Yourself &mdash; sourcing, design, production and fulfillment under one roof.",
        "about", TEAM_BODY)
    render("/join-our-team/",
        "Join Our Team &mdash; Identify Yourself",
        "Open roles and careers at Identify Yourself on the Outer Banks of North Carolina.",
        "about", CAREERS_BODY)
    render("/policies/",
        "Policies &mdash; Identify Yourself",
        "Ordering, turnaround, returns, remakes and privacy policies at Identify Yourself.",
        "about", POLICIES_BODY)
    render("/blog/",
        "News + Blog &mdash; Identify Yourself",
        "Notes, case studies and ideas from the Identify Yourself shop floor.",
        "blog", BLOG_BODY)
    render("/contact-us/",
        "Contact &mdash; Identify Yourself",
        "Start a project, request a quote, or just say hello. Identify Yourself is listening.",
        "contact", CONTACT_BODY)
    render("/pay-online/",
        "Pay Online &mdash; Identify Yourself",
        "Pay an Identify Yourself invoice online. Secure portal, fast receipts.",
        "home", PAY_BODY)

    # Services hub + detail pages
    render("/services/",
        "What We Do &mdash; Identify Yourself",
        "Custom apparel, company merch, incentives, warehousing, online stores, creative, large format and print &mdash; all in-house.",
        "services", SERVICES_HUB_BODY)
    for slug, label in SERVICES:
        render(f"/services/{slug}/",
            f"{SERVICE_CONTENT[slug]['title']} &mdash; Identify Yourself",
            f"{SERVICE_CONTENT[slug]['title']} services at Identify Yourself &mdash; sourced, produced and shipped by one in-house team.",
            "services", service_body(slug))
    print("\nBuild complete.")

if __name__ == "__main__":
    build()
