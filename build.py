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
PHONE_DISPLAY    = "877-303-1049"
PHONE_TEL        = "+18773031049"
PHONE_LOCAL      = "252-480-1433"
PHONE_LOCAL_TEL  = "+12524801433"
FAX_DISPLAY      = "252-261-4082"
EMAIL            = "info@idyourself.com"
ADDRESS_HTML     = (
    "PO Box 432<br/>"
    "6146 N Croatan Hwy<br/>"
    "Kitty Hawk, NC 27949"
)
SHOP_URL         = "https://shop.idyourself.com/"
PRODUCTS_URL     = "https://products.idyourself.com/"
SOCIAL_FACEBOOK  = "https://www.facebook.com/idyourself"
SOCIAL_LINKEDIN  = "https://www.linkedin.com/company/identify-yourself-llc"
SOCIAL_PINTEREST = "https://www.pinterest.com/idyourself"

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
    ("awards-and-recognition",          "Awards &amp; Recognition"),
    ("tradeshow-displays",              "Tradeshow Displays"),
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
            <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY} <small>(toll-free)</small></a>
            <a href="tel:{PHONE_LOCAL_TEL}">{PHONE_LOCAL} <small>(local)</small></a>
            <p style="color:var(--text-dim);font-size:.85rem;">Fax {FAX_DISPLAY}</p>
            <p>{ADDRESS_HTML}</p>
            <p style="margin-top:.75rem;">
              <a href="{SOCIAL_FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">FB</a> &middot;
              <a href="{SOCIAL_LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">LI</a> &middot;
              <a href="{SOCIAL_PINTEREST}" target="_blank" rel="noopener" aria-label="Pinterest">PIN</a>
            </p>
          </div>
        </div>
        <div class="container footer__bar">
          <span>&copy; <span data-year></span> Identify Yourself, LLC &middot; All rights reserved</span>
          <span><a href="/policies/">Policies</a> &middot; <a href="/contact-us/">Contact</a> &middot; <a href="{PRODUCTS_URL}" target="_blank" rel="noopener">Products &#8599;</a></span>
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
        <p class="lede" data-reveal>We&rsquo;re not checking your fingerprints or running background checks &mdash; we&rsquo;re your partner in <em>cracking the case</em> of brand identity. Creative full-service promotional products, apparel and marketing since 2003.</p>
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
    "We take big ideas<br/>and get them <em>off the ground</em>.",
    "Born in 2003 from an expertise in building brands, offering unique, quality promotional products, excellent service and customer-focused marketing &mdash; all from our office in Kitty Hawk, NC."
) + dedent("""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">Family owned. <em>Outer Banks</em> based.</h2>
          <p>We&rsquo;re a family owned and operated full-service promotional branding and marketing agency. We understand the challenges of getting brands to stand out &mdash; and we love solving them.</p>
          <p>Our team takes a thoughtful full-picture look at your business to determine which products, vendors and design do justice for your brand. No throwaway suggestions, no mystery markups.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Cracking the <span class="accent">case</span> of brand identity.</h2>
          <p>Promotional products, custom apparel, creative services, print, packaging, online stores, warehousing, kitting &mdash; every branded touchpoint under one roof.</p>
          <p>We showcase your business with creative promotional merchandise that gets people talking, remembering and connecting with your brand.</p>
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
    "A vibrant group of<br/><em>marketing-minded</em> folks.",
    "Our crew comes from a variety of sales and advertising backgrounds &mdash; each one adds their own unique perspective and talent into every project and order."
) + dedent("""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">Headquartered on the <em>Outer Banks</em>.</h2>
          <p>From our office in Kitty Hawk, NC, we support brands across the country. Small enough that you know who&rsquo;s working on your order, seasoned enough to run programs at scale.</p>
          <p>Full team roster, headshots and bios coming to this page soon. In the meantime, we&rsquo;d love to introduce ourselves in person &mdash; give us a call.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">What you can <span class="accent">expect</span> from us.</h2>
          <ul class="list">
            <li>Marketing-minded thinking on every project, not just order-taking</li>
            <li>Cross-functional perspective from sales, advertising and production backgrounds</li>
            <li>One senior partner from brief through shipment</li>
            <li>Direct, plain-spoken communication &mdash; no promo-industry jargon</li>
          </ul>
          <p style="margin-top:1.25rem;"><a class="btn btn--solid" href="/contact-us/#quote">Meet us on a call <span aria-hidden="true">&rarr;</span></a></p>
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
    "Order &amp; shipping<br/><em>information</em>.",
    "Everything you need to know about production timing, artwork requirements, cancellations and returns. No surprises."
) + dedent("""\
    <div class="container">
      <section class="about-grid">
        <div data-reveal>
          <h2 class="h-display">Production time</h2>
          <p>Standard production time is <strong>10 working days plus shipping time</strong> after art approval. Rush production is available on many items with additional charges applied.</p>
          <h2 class="h-display" style="margin-top:2rem;">Artwork</h2>
          <p>Black and white camera-ready artwork in <strong>PDF or EPS format with 300 dpi resolution or higher</strong> is required. Art charges will apply for cleaning up art, typesetting or creating new art.</p>
          <h2 class="h-display" style="margin-top:2rem;">Pricing</h2>
          <p>Pricing does not include shipping, proofs, or any artwork charges unless otherwise indicated. Written quotes are binding within their stated validity window.</p>
        </div>
        <div data-reveal>
          <h2 class="h-display" style="color: var(--cream);">Cancellations &amp; <span class="accent">returns</span></h2>
          <p><strong>Once an approved proof is received, there may be no cancellations on custom orders.</strong></p>
          <p>All custom orders are final sale, with no returns or exchanges without authorization on damaged or mis-shipped merchandise only.</p>
          <h2 class="h-display" style="margin-top:2rem;">Damaged or mis-shipped</h2>
          <p>If something arrives damaged or isn&rsquo;t what you ordered, reach out within 7 days and we&rsquo;ll make it right &mdash; remake, replace or refund.</p>
          <h2 class="h-display" style="margin-top:2rem;">Questions</h2>
          <p>When in doubt, call us. We&rsquo;d rather catch an issue up front than apologize for one later.</p>
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
    (
        "Parade Preparedness: Branded Swag &amp; Promotional Products for Parades",
        "While your float will leave a temporary visual, your group can really leave a lasting impression through custom branded promotional products that are memorable, useful, and don&rsquo;t have to be much more expensive than the usual candy.",
        "https://idyourself.com/blog/parade-preparedness-parade-promotional-products-branded-swag/",
    ),
    (
        "The Perceived Value of Promotional Products",
        "The power of promotional products is strong and the perceived value by your clients is there and the actual value on your bottom line is amazing. In the promo world, a company can spend less and get more.",
        "https://idyourself.com/blog/the-perceived-value-of-promotional-products/",
    ),
    (
        "Merch that actually gets worn",
        "A field guide to picking garments people keep in the rotation &mdash; fit, weight, hand-feel, decoration.",
        "/contact-us/",
    ),
    (
        "Building a company store that scales",
        "Lessons from years of running branded online stores &mdash; and what we&rsquo;d tell a first-timer.",
        "/services/online-stores/",
    ),
    (
        "Kitting, done right",
        "Why the unboxing matters as much as the swag inside &mdash; and how we build welcome kits that earn photos.",
        "/services/warehousing-and-custom-kitting/",
    ),
    (
        "Large format, done fast",
        "Banners, backdrops and pop-ups for events that materialized on short notice. Print turnarounds that don&rsquo;t cut corners.",
        "/services/large-format-printing/",
    ),
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
    (lambda title, excerpt, href, tgt: (
        f'          <article class="blog-card" data-reveal>\n'
        f'            <div class="blog-card__chip">Journal</div>\n'
        f'            <h3>{title}</h3>\n'
        f'            <p>{excerpt}</p>\n'
        f'            <a href="{href}" class="blog-card__link"{tgt}>Read more <span aria-hidden="true">&rarr;</span></a>\n'
        f'          </article>\n'
    ))(title, excerpt, href, ' target="_blank" rel="noopener"' if href.startswith('http') else '')
    for title, excerpt, href in BLOG_POSTS
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
            <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> <small>(toll-free)</small></p>
            <p><a href="tel:{PHONE_LOCAL_TEL}">{PHONE_LOCAL}</a> <small>(local)</small></p>
            <p><small>Fax {FAX_DISPLAY}</small></p>
          </div>
          <div class="block">
            <h3>Studio</h3>
            <p>{ADDRESS_HTML}</p>
          </div>
          <div class="block">
            <h3>Shop online</h3>
            <p><a href="{SHOP_URL}" target="_blank" rel="noopener">shop.idyourself.com &#8599;</a></p>
            <p><a href="{PRODUCTS_URL}" target="_blank" rel="noopener">products.idyourself.com &#8599;</a></p>
          </div>
          <div class="block">
            <h3>Follow</h3>
            <p>
              <a href="{SOCIAL_FACEBOOK}" target="_blank" rel="noopener">Facebook</a> &middot;
              <a href="{SOCIAL_LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &middot;
              <a href="{SOCIAL_PINTEREST}" target="_blank" rel="noopener">Pinterest</a>
            </p>
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
        "headline": "Apparel for <em>employees</em><br/>&amp; customers alike.",
        "lede": "Designing custom apparel for employees or merchandise for customers &mdash; with industry leading printing and embroidery options.",
        "what": "Whether you&rsquo;re outfitting a team in branded uniforms or building a merchandise line that customers actually want to wear, we handle the full process in-house: source the garment, prep the art, decorate, and ship.",
        "how": "We start with what the piece needs to do &mdash; uniform, giveaway, retail merch &mdash; and match the garment and decoration to the job. Proofs before production, always.",
        "bullets": [
            "Screen printing for punchy, high-impact color",
            "Embroidery for logos that wear and wash well",
            "Employee uniform programs with reorder options",
            "Customer-facing merchandise apparel",
            "Industry leading print and decoration options",
        ],
    },
    "company-merch": {
        "title": "Company Merch",
        "eyebrow": "Company Merch",
        "headline": "Merch people are<br/><em>excited</em> to receive.",
        "lede": "High quality bags, pens, tech gifts, and other promotional items that people are excited to receive and use &mdash; with thousands of selections to choose from.",
        "what": "We curate merch programs for employee onboarding, events, customer gifting and everyday brand presence. Every item is sourced with the logo, the audience and the use case in mind.",
        "how": "Tell us the brief &mdash; we come back with a tight short list, real samples on request, and one quote that includes decoration and freight. No mystery SKUs.",
        "bullets": [
            "Bags, pens, drinkware and tech gifts",
            "1000s of selections across every category",
            "Thoughtful, brand-right product curation",
            "In-house decoration &mdash; laser, pad print, screen, embroidery",
            "Kitting + branded packaging available",
        ],
    },
    "incentives-and-gifts": {
        "title": "Incentives & Gifts",
        "eyebrow": "Incentives &amp; Gifts",
        "headline": "Loyalty programs<br/>&amp; <em>corporate gifts</em>.",
        "lede": "Create incentive and gift programs for customers and sponsors to show appreciation and keep your business fresh on their minds.",
        "what": "From a single executive gift to a multi-tier sales incentive program, we design the full experience &mdash; product, packaging, note, delivery window &mdash; so the thank-you actually lands.",
        "how": "Give us the budget, audience and occasion. We come back with tiered options. Approve, we build, we ship.",
        "bullets": [
            "Customer incentive &amp; loyalty programs",
            "Sponsor gifts and partnership thank-yous",
            "Corporate gifting, tiered by recipient",
            "Reward program design &amp; fulfillment",
            "Custom packaging and personalized notes",
        ],
    },
    "warehousing-and-custom-kitting": {
        "title": "Warehousing & Custom Kitting",
        "eyebrow": "Warehousing &amp; Custom Kitting",
        "headline": "Pick, pack, ship,<br/><em>hold</em> &mdash; we&rsquo;ve got it.",
        "lede": "We have the square footage and team to pick, pack, ship and hold all of your promotional products. Take advantage of bulk pricing without taking up valuable office space.",
        "what": "Services range from basic mailers sent to target audiences to kitting multiple items to be packaged and shipped individually or in bulk. We focus on flexibility and work with you to develop a plan that meets your specific needs.",
        "how": "Pallets come into our facility and leave as branded kits on your schedule. SKU-level visibility, on-demand reorders, real humans on the account.",
        "bullets": [
            "Pick, pack and ship from our warehouse",
            "Product storage &mdash; bulk pricing without the office clutter",
            "Basic mailers to target audiences",
            "Custom multi-item kitting &mdash; individual or bulk",
            "Flexible fulfillment plans built around your needs",
        ],
    },
    "online-stores": {
        "title": "Online Stores",
        "eyebrow": "Online Stores",
        "headline": "User-friendly<br/><em>branded stores</em>.",
        "lede": "Online company stores are user-friendly and allow you to customize the shopping experience for both employees and customers.",
        "what": "Easily set up and manage your promotional inventory. Employees and customers order online, we produce and ship. Perfect for uniform programs, loyalty programs and reward programs.",
        "how": "We set up the store, photograph the SKUs, connect it to our fulfillment, and keep it running. On-demand or held-stock &mdash; whichever fits your volume.",
        "bullets": [
            "Custom branded company store setup",
            "User-friendly shopping for employees or customers",
            "Easy inventory management",
            "Uniform, loyalty and reward programs",
            "Tied into our warehousing and kitting services",
        ],
    },
    "creative-services": {
        "title": "Creative Services",
        "eyebrow": "Creative Services",
        "headline": "Design that gives<br/>your brand <em>polish</em>.",
        "lede": "Our design team can craft designs or logos that capture your business&rsquo;s personality and aesthetic &mdash; starting from the ground up or giving an established brand a fresh look.",
        "what": "Logos, graphic design and digitizing give promotional products polish. Whether you&rsquo;re rebranding or launching, we design logos and promotional items that fit the way your brand needs to show up.",
        "how": "Brief, concepts, refinement, production-ready files. Every piece of creative we produce is ready for the press it&rsquo;s going to.",
        "bullets": [
            "Logo design and brand identity",
            "Graphic design for promotional items",
            "Digitizing for embroidery",
            "Virtual samples and vector art conversions",
            "Rebranding and brand refresh",
        ],
        "pricing_note": "Our hourly rate for graphic services starts at $50.00/hour for most jobs.",
    },
    "large-format-printing": {
        "title": "Large Format Printing",
        "eyebrow": "Large Format Printing",
        "headline": "Signs, banners<br/>&amp; <em>posters</em>, big.",
        "lede": "Custom signage, banners, posters and a variety of large format printing options &mdash; fast turns from our in-house team.",
        "what": "Indoor and outdoor large-format for events, retail, wayfinding and brand installations. We print, finish and ship &mdash; or deliver locally on the Outer Banks.",
        "how": "Send the art (or we&rsquo;ll design it). We proof, print, finish and deliver on the timeline you need.",
        "bullets": [
            "Custom signage for retail, events and wayfinding",
            "Vinyl, mesh and pole banners",
            "Posters &mdash; indoor and outdoor rated",
            "Large-scale backdrops",
            "Tradeshow and event signage",
        ],
    },
    "print-collateral-and-packaging": {
        "title": "Print Collateral & Packaging",
        "eyebrow": "Print Collateral &amp; Packaging",
        "headline": "If you can <em>dream it</em>,<br/>we can print it.",
        "lede": "Printing and packaging materials that deliver marketing messages and brand directly to customers&rsquo; hands.",
        "what": "Custom packaging showcases products in the best light and communicates product benefits to clients and end users. From business cards to branded shippers, we cover every print touchpoint.",
        "how": "We&rsquo;ll help spec the stock, finish and bindery based on the job. Real press proofs on anything that matters.",
        "bullets": [
            "Postcards and direct mailers",
            "Brochures and business cards",
            "Custom packaging for your products",
            "Package signage and large format pieces",
            "Press-quality finishes &mdash; foil, emboss, die-cut",
        ],
    },
    "awards-and-recognition": {
        "title": "Awards & Recognition",
        "eyebrow": "Awards &amp; Recognition",
        "headline": "From <em>Grammy-esque</em><br/>to custom plaques.",
        "lede": "From Grammy-esque trophies to unique plaques and certificates &mdash; with a range of materials, textures, designs, engraving options and price points.",
        "what": "Recognition programs, milestone awards, sales incentives, service anniversaries, team shout-outs. We source the piece, handle the engraving, and deliver on-time for the moment it needs to land.",
        "how": "Share the occasion, budget and volume. We come back with options across materials and tiers, then produce and ship.",
        "bullets": [
            "Custom trophies and awards",
            "Plaques, certificates and recognition pieces",
            "Engraving, etching and printed personalization",
            "Material range: acrylic, wood, metal, glass, stone",
            "Tiered programs for annual recognition",
        ],
    },
    "tradeshow-displays": {
        "title": "Tradeshow Displays",
        "eyebrow": "Tradeshow Displays",
        "headline": "Eye-catching booths,<br/>one-of-a-kind <em>presence</em>.",
        "lede": "Large-scale backdrops or banners, standout signage, and tabletop displays &mdash; eye-catching, unique designs that represent your brand.",
        "what": "Retractable banners, fabric backdrops, rigid signage, tablecloths, feather flags, hanging structures. Everything needed to own a 10x10 (or bigger) on the show floor.",
        "how": "Tell us the space, the story and the lead time. We design, produce and ship &mdash; with carry cases and setup guidance.",
        "bullets": [
            "Large scale backdrops and banners",
            "Retractable and pull-up banner stands",
            "Tabletop displays and table throws",
            "Standout signage and feather flags",
            "Custom design tailored to your brand",
        ],
    },
}

def service_body(slug: str) -> str:
    d = SERVICE_CONTENT[slug]
    bullets = '\n'.join(f'            <li>{b}</li>' for b in d['bullets'])
    pricing = ''
    if d.get('pricing_note'):
        pricing = f"<p style=\"margin-top:1rem;color:var(--text-dim);font-style:italic;\">{d['pricing_note']}</p>"
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
              {pricing}
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
