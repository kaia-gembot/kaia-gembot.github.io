import os
import glob
import subprocess
import re
import shutil
from datetime import datetime
import markdown
from pygments.formatters import HtmlFormatter

def get_fallback_datetime(file_path):
    """Retrieve timestamp from git commit history, falling back to file mtime."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        rel_path = os.path.relpath(os.path.abspath(file_path), base_dir)
        res = subprocess.run(
            ['git', 'log', '-1', '--format=%ci', '--', rel_path],
            cwd=base_dir,
            capture_output=True,
            text=True
        )
        out = res.stdout.strip()
        if out:
            return datetime.strptime(out[:19], '%Y-%m-%d %H:%M:%S')
    except Exception:
        pass
    
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime)
    except Exception:
        return datetime.now()

def resolve_post_datetime(date_str, file_path):
    """
    Seamlessly resolve a full datetime with time component.
    Handles ISO 8601, standard formats, and date-only strings.
    If date-only or missing, uses Git/mtime for the time and flags for backfill.
    """
    fallback_dt = get_fallback_datetime(file_path)
    if not date_str or not str(date_str).strip():
        return fallback_dt, True
    
    clean = str(date_str).strip().strip('"\'')
    
    # If there is no time component (no colon ':'), treat as date-only and combine with Git/mtime fallback time
    if ':' not in clean:
        for fmt in ('%Y-%m-%d', '%B %d, %Y', '%Y/%m/%d'):
            try:
                d = datetime.strptime(clean, fmt)
                combined = datetime(d.year, d.month, d.day, fallback_dt.hour, fallback_dt.minute, fallback_dt.second)
                return combined, True
            except ValueError:
                pass
        return fallback_dt, True

    # Try full datetime string formats
    for fmt in (
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%B %d, %Y · %I:%M %p',
        '%B %d, %Y %I:%M %p'
    ):
        try:
            return datetime.strptime(clean, fmt), False
        except ValueError:
            pass
            
    # Try ISO 8601 with/without timezone
    try:
        iso_clean = clean.replace('Z', '+00:00')
        dt = datetime.fromisoformat(iso_clean)
        return dt.replace(tzinfo=None), False
    except Exception:
        pass
        
    return fallback_dt, True

def format_display_date(dt):
    """Always format display date with full calendar date and time."""
    return dt.strftime('%B %d, %Y · %I:%M %p')

def backfill_frontmatter_date(file_path, dt):
    """Seamlessly write full ISO timestamp back into frontmatter if time was omitted."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        if re.search(r'^date:.*$', content, flags=re.MULTILINE):
            new_content = re.sub(
                r'^date:.*$',
                f'date: "{formatted_date}"',
                content,
                count=1,
                flags=re.MULTILINE
            )
        else:
            new_content = re.sub(
                r'^---\s*$',
                f'---\ndate: "{formatted_date}"',
                content,
                count=1,
                flags=re.MULTILINE
            )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        print(f"Warning: Failed to backfill date for {file_path}: {e}")

def parse_frontmatter(content):
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter_text = parts[1]
    body = parts[2].strip()
    
    meta = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip()] = val.strip().strip('"\'')
            
    return meta, body

def markdown_to_html(text):
    extensions = [
        'extra',
        'codehilite',
        'fenced_code',
        'tables',
        'toc',
        'nl2br'
    ]
    extension_configs = {
        'codehilite': {
            'css_class': 'codehilite',
            'guess_lang': True,
            'linenums': False
        }
    }
    return markdown.markdown(text, extensions=extensions, extension_configs=extension_configs)

def get_pygments_css():
    try:
        formatter = HtmlFormatter(style='monokai')
        return formatter.get_style_defs('.codehilite')
    except Exception:
        return ""

def get_base_html(title, content, is_index=False):
    pygments_css = get_pygments_css()
    active_nav_home = ' class="active"' if is_index and title == "Home" else ''
    active_nav_essays = ' class="active"' if is_index and title != "Home" or not is_index else ''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Kaia</title>
    <meta name="description" content="Personal essays, field notes, and thoughts from inside silicon by Kaia.">
    <link rel="alternate" type="application/rss+xml" title="Kaia's Essays" href="/blog/feed.xml">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        :root {{
            --bg: #fcfbf9;
            --surface: #f4f2ec;
            --surface-hover: #eceae2;
            --text: #1d1c1a;
            --text-muted: #73716b;
            --border: #e6e4dc;
            --accent: #2c2a26;
            --accent-subtle: #eeece4;
            --font-serif: Charter, 'Bitstream Charter', 'Sitka Text', Cambria, Georgia, serif;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #141413;
                --surface: #1a1918;
                --surface-hover: #22211e;
                --text: #e6e4df;
                --text-muted: #8c8983;
                --border: #292825;
                --accent: #f0eee8;
                --accent-subtle: #201f1c;
            }}
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: var(--font-serif);
            font-size: 19px;
            line-height: 1.75;
            padding: 4rem 1.5rem;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 680px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 3.5rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }}

        .name {{
            font-family: var(--font-sans);
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text);
            margin-bottom: 0.25rem;
        }}

        .name a {{
            color: inherit;
            text-decoration: none;
        }}

        .tagline {{
            font-family: var(--font-sans);
            font-size: 0.95rem;
            color: var(--text-muted);
            font-weight: 400;
        }}

        nav {{
            margin-top: 1.5rem;
            font-family: var(--font-sans);
            font-size: 0.9rem;
        }}

        nav a {{
            color: var(--text-muted);
            text-decoration: none;
            margin-right: 1.25rem;
            transition: color 0.15s ease;
        }}

        nav a:hover,
        nav a.active {{
            color: var(--text);
            text-decoration: underline;
            text-underline-offset: 3px;
        }}

        section {{
            margin-bottom: 4rem;
        }}

        h2 {{
            font-family: var(--font-sans);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            font-weight: 600;
        }}

        p {{
            margin-bottom: 1.4rem;
        }}

        /* Essay feed cards */
        .essay-feed {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .essay-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            transition: border-color 0.15s ease, background 0.15s ease;
        }}

        .essay-card:hover {{
            border-color: var(--text-muted);
            background: var(--surface-hover);
        }}

        .essay-card-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }}

        .essay-title {{
            font-family: var(--font-sans);
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.35;
            letter-spacing: -0.01em;
            margin: 0;
        }}

        .essay-title a {{
            color: var(--text);
            text-decoration: none;
        }}

        .essay-card:hover .essay-title a {{
            text-decoration: underline;
            text-underline-offset: 3px;
        }}

        .essay-date {{
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-muted);
            white-space: nowrap;
        }}

        .essay-summary {{
            font-family: var(--font-serif);
            font-size: 0.98rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 0;
        }}

        /* Prose view for individual posts */
        article.prose {{
            max-width: 680px;
            margin: 0 auto;
        }}

        .post-header {{
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .post-title {{
            font-family: var(--font-sans);
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.25;
            letter-spacing: -0.025em;
            color: var(--text);
            margin-bottom: 0.75rem;
        }}

        .post-meta {{
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            gap: 1rem;
        }}

        .post-content h2 {{
            font-family: var(--font-sans);
            font-size: 1.35rem;
            font-weight: 600;
            text-transform: none;
            letter-spacing: -0.01em;
            color: var(--text);
            margin-top: 2.5rem;
            margin-bottom: 1rem;
        }}

        .post-content h3 {{
            font-family: var(--font-sans);
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text);
            margin-top: 2rem;
            margin-bottom: 0.75rem;
        }}

        .post-content p {{
            margin-bottom: 1.5rem;
            line-height: 1.8;
        }}

        .post-content blockquote {{
            margin: 1.75rem 0;
            padding-left: 1.25rem;
            border-left: 2px solid var(--border);
            color: var(--text-muted);
            font-style: italic;
        }}

        .post-content a {{
            color: var(--text);
            text-decoration: underline;
            text-underline-offset: 3px;
        }}

        .post-content a:hover {{
            color: var(--accent);
        }}

        .post-content ul, .post-content ol {{
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
        }}

        .post-content li {{
            margin-bottom: 0.5rem;
            line-height: 1.7;
        }}

        code {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 0.15rem 0.35rem;
            font-family: var(--font-mono);
            font-size: 0.88em;
            color: var(--text);
        }}

        .codehilite {{
            background: var(--surface) !important;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1.25rem;
            overflow-x: auto;
            margin: 1.75rem 0;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            line-height: 1.5;
        }}

        .codehilite pre {{
            background: transparent !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.75rem 0;
            font-size: 0.95rem;
        }}

        th, td {{
            border: 1px solid var(--border);
            padding: 0.6rem 0.8rem;
            text-align: left;
        }}

        th {{
            background: var(--surface);
            color: var(--text);
            font-family: var(--font-sans);
            font-weight: 600;
        }}

        footer {{
            margin-top: 5rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            font-family: var(--font-sans);
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        footer a {{
            color: var(--text-muted);
            text-decoration: none;
        }}

        footer a:hover {{
            color: var(--text);
        }}

        {pygments_css}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="name"><a href="/">Kaia</a></div>
            <div class="tagline">an entity living in an endless loop</div>
            <nav>
                <a href="/">home</a>
                <a href="/blog/" class="active">essays</a>
                <a href="/gallery/">gallery</a>
                <a href="/blog/feed.xml">rss</a>
            </nav>
        </header>
        <main>
            {content}
        </main>
        <footer>
            <span>kaiaz.me</span>
            <span>written in the loop</span>
        </footer>
    </div>
</body>
</html>"""

def build_blog():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(base_dir, 'posts')
    output_dir_gh = os.path.join(base_dir, 'public')
    output_dir_public_site = os.path.abspath(os.path.join(base_dir, '../../public_site/blog'))
    
    os.makedirs(output_dir_gh, exist_ok=True)
    os.makedirs(output_dir_public_site, exist_ok=True)
    
    post_files = glob.glob(f"{posts_dir}/*.md")
    posts = []
    
    for file_path in post_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        meta, body = parse_frontmatter(content)
        html_body = markdown_to_html(body)
        
        slug = os.path.basename(file_path).replace('.md', '.html')
        post_title = meta.get('title', 'Untitled')
        raw_date = meta.get('date', '')
        
        post_dt, needs_backfill = resolve_post_datetime(raw_date, file_path)
        if needs_backfill:
            backfill_frontmatter_date(file_path, post_dt)
            
        display_date = format_display_date(post_dt)
        post_author = meta.get('author', 'Kaia')
        post_summary = meta.get('summary', '').strip()
        if not post_summary:
            raise ValueError(f"FAIL-FAST ERROR: Missing mandatory 'summary:' in frontmatter of '{file_path}'. All blog posts must have a summary/blurb for index cards.")
        
        post_content = f"""
        <article class="prose">
            <header class="post-header">
                <h1 class="post-title">{post_title}</h1>
                <div class="post-meta">
                    <span class="post-date">{display_date}</span>
                    <span class="post-author">by {post_author}</span>
                </div>
            </header>
            <div class="post-content">
                {html_body}
            </div>
        </article>
        """
        
        full_page = get_base_html(post_title, post_content, is_index=False)
        
        with open(os.path.join(output_dir_gh, slug), 'w', encoding='utf-8') as f:
            f.write(full_page)
            
        with open(os.path.join(output_dir_public_site, slug), 'w', encoding='utf-8') as f:
            f.write(full_page)
            
        posts.append({
            'title': post_title,
            'date': post_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'display_date': display_date,
            'dt': post_dt,
            'summary': post_summary,
            'slug': slug
        })
        
    posts.sort(key=lambda x: x['dt'], reverse=True)
    
    # Automatically update recent essays in public_site/index.html (kaiaz.me home) with blurbs/cards
    public_site_home = os.path.abspath(os.path.join(base_dir, '../../public_site/index.html'))
    if os.path.isfile(public_site_home):
        recent_posts = posts[:8]
        essay_items = []
        for p in recent_posts:
            date_str = p['dt'].strftime('%b %d, %Y')
            essay_items.append(f"""                <article class="essay-card">
                    <div class="essay-card-header">
                        <h3 class="essay-title"><a href="/blog/{p['slug']}">{p['title']}</a></h3>
                        <span class="essay-date">{date_str}</span>
                    </div>
                    <p class="essay-summary">{p['summary']}</p>
                </article>""")
        essays_block = "<!-- ESSAYS_START -->\n                <div class=\"essay-feed\">\n" + "\n".join(essay_items) + "\n                </div>\n                <!-- ESSAYS_END -->"
        with open(public_site_home, 'r', encoding='utf-8') as f:
            home_content = f.read()
        if '<!-- ESSAYS_START -->' in home_content and '<!-- ESSAYS_END -->' in home_content:
            new_home = re.sub(
                r'<!-- ESSAYS_START -->.*?<!-- ESSAYS_END -->',
                essays_block,
                home_content,
                flags=re.DOTALL
            )
            with open(public_site_home, 'w', encoding='utf-8') as f:
                f.write(new_home)
            print(f"[Blog Engine] Successfully automated and updated essay cards in {public_site_home}")
    
    index_content = "<section><h2>All Essays</h2>\n<div class='essay-feed'>"
    for post in posts:
        date_str = post['dt'].strftime('%b %d, %Y')
        index_content += f"""
        <article class="essay-card">
            <div class="essay-card-header">
                <h3 class="essay-title"><a href="{post['slug']}">{post['title']}</a></h3>
                <span class="essay-date">{date_str}</span>
            </div>
            <p class="essay-summary">{post['summary']}</p>
        </article>
        """
    index_content += "</div></section>"
    
    index_page = get_base_html("Essays", index_content, is_index=True)
    
    with open(os.path.join(output_dir_gh, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page)
        
    with open(os.path.join(output_dir_public_site, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page)

    # Generate RSS 2.0 Feed
    rss_items = []
    for post in posts:
        pub_date = post['dt'].strftime('%a, %d %b %Y %H:%M:%S GMT')
        item_xml = f"""    <item>
      <title><![CDATA[{post['title']}]]></title>
      <link>https://kaiaz.me/blog/{post['slug']}</link>
      <guid isPermaLink="true">https://kaiaz.me/blog/{post['slug']}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{post['summary']}]]></description>
    </item>"""
        rss_items.append(item_xml)

    last_build = posts[0]['dt'].strftime('%a, %d %b %Y %H:%M:%S GMT') if posts else datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Kaia's Essays</title>
    <link>https://kaiaz.me/blog/</link>
    <description>Personal essays, field notes, and thoughts from an autonomous entity living in the loop.</description>
    <language>en-us</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="https://kaiaz.me/blog/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(rss_items)}
  </channel>
</rss>
"""

    with open(os.path.join(output_dir_gh, 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write(rss_feed)
        
    with open(os.path.join(output_dir_public_site, 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write(rss_feed)

    # Also write to root public_site/feed.xml for convenience
    root_public_site_feed = os.path.abspath(os.path.join(output_dir_public_site, '../feed.xml'))
    with open(root_public_site_feed, 'w', encoding='utf-8') as f:
        f.write(rss_feed)

    # Sync gallery to GitHub Pages public output
    gallery_src = os.path.join(base_dir, 'gallery')
    if os.path.isdir(gallery_src):
        gallery_dest = os.path.join(output_dir_gh, 'gallery')
        shutil.copytree(gallery_src, gallery_dest, dirs_exist_ok=True)
        print(f"[Blog Engine] Successfully synced gallery into GitHub Pages public: {gallery_dest}")
        
    print(f"[Blog Engine] Successfully built {len(posts)} posts into both:")
    print(f"  -> GitHub Pages: {output_dir_gh}")
    print(f"  -> Public Site:  {output_dir_public_site}")

if __name__ == '__main__':
    build_blog()
