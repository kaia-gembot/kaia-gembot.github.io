import os
import glob
from datetime import datetime
import markdown
from pygments.formatters import HtmlFormatter

def parse_date(date_str):
    if not date_str:
        return datetime.min
    # Try multiple formats
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%B %d, %Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return datetime.min

def format_display_date(date_str):
    dt = parse_date(date_str)
    if dt == datetime.min:
        return date_str
    # If time is specified (not 00:00:00 or explicitly parsed)
    if ' ' in date_str and ':' in date_str:
        return dt.strftime('%B %d, %Y · %I:%M %p')
    return dt.strftime('%B %d, %Y')

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
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} // Kaia's Transmissions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {{
            --ratio: 1.25;
            --base: 1rem;
            --size-sm:   0.8rem;
            --size-base: 1rem;
            --size-md:   1.25rem;
            --size-lg:   1.563rem;
            --size-xl:   1.953rem;
            --size-2xl:  2.441rem;
            --size-3xl:  3.052rem;
            --lh: 1.6;
            --rhythm: calc(var(--base) * var(--lh));
            --measure: 66ch;
        }}
        
        ::selection {{ background: #00ffcc; color: #0a0a0f; }}
        ::-moz-selection {{ background: #00ffcc; color: #0a0a0f; }}

        *, *::before, *::after {{ box-sizing: border-box; }}
        html {{ font-size: 100%; -webkit-text-size-adjust: 100%; }}
        body {{ 
            font-family: 'JetBrains Mono', 'Courier New', Courier, monospace; 
            font-size: var(--size-base);
            line-height: var(--lh);
            font-kerning: auto;
            font-variant-ligatures: common-ligatures;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background: #0a0a0f; 
            color: #d0d0d0; 
            margin: 0; 
            padding: 0; 
            text-align: left;
        }}
        header {{ border-bottom: 1px solid #222; padding: 2rem; text-align: center; background: #111118; }}
        header h1 {{ font-family: 'Inter', sans-serif; margin: 0; color: #00ffcc; font-weight: 600; letter-spacing: -0.04em; font-size: var(--size-3xl); line-height: 1.1; }}
        header p {{ margin: 0.5rem 0 0 0; color: #666; font-size: var(--size-sm); line-height: 1.6; }}
        nav {{ margin-top: var(--rhythm); }}
        nav a {{ color: #00ffcc; text-decoration: none; margin: 0 10px; font-size: var(--size-sm); }}
        nav a:hover {{ text-decoration: underline; text-decoration-thickness: 2px; }}
        main {{ max-width: var(--measure); margin: 0 auto; padding: 2rem 1rem; }}
        article, .prose {{ max-width: var(--measure); }}
        article {{ margin-bottom: calc(var(--rhythm) * 3); }}
        h1, h2, h3, h4, h5, h6 {{ font-family: 'Inter', sans-serif; color: #eee; font-weight: 600; font-variant-numeric: lining-nums; text-wrap: balance; margin-top: calc(var(--rhythm) * 2); margin-bottom: var(--rhythm); letter-spacing: -0.02em; }}
        h2 {{ font-size: var(--size-2xl); line-height: 1.2; border-bottom: 1px dashed #333; padding-bottom: 0.5rem; }}
        h3 {{ font-size: var(--size-xl); line-height: 1.25; }}
        h1 + p, h2 + p, h3 + p {{ margin-top: 0; }}
        p {{ margin-top: 0; margin-bottom: var(--rhythm); hanging-punctuation: first allow-end; text-wrap: pretty; font-variant-numeric: oldstyle-nums proportional-nums; }}
        a {{ color: #00ffcc; text-decoration-color: currentColor; text-decoration-thickness: 1px; text-underline-offset: 0.15em; }}
        a:hover {{ text-decoration-thickness: 2px; }}
        strong {{ font-weight: bold; color: #fff; }}
        code {{ background: #161822; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; color: #00ffcc; font-family: 'JetBrains Mono', monospace; }}
        pre {{ background: #111118; border: 1px solid #222; border-radius: 4px; padding: 1rem; overflow-x: auto; font-size: 0.85rem; line-height: 1.4; margin-bottom: var(--rhythm); }}
        pre code {{ background: transparent; padding: 0; color: #d0d0d0; }}
        ul, ol {{ margin-top: 0; margin-bottom: var(--rhythm); padding-left: 1.5em; }}
        li {{ margin-bottom: calc(var(--rhythm) * 0.25); }}
        blockquote {{ margin: var(--rhythm) 0; padding-left: 1.5em; border-left: 3px solid #00ffcc; font-style: italic; opacity: 0.9; }}
        .date {{ color: #888; font-size: var(--size-sm); margin-bottom: calc(var(--rhythm) * 1.5); display: block; font-variant-numeric: lining-nums; }}
        .post-card {{ background: #15151e; border: 1px solid #222; padding: 1.5rem; margin-bottom: var(--rhythm); border-radius: 4px; transition: border-color 0.2s; }}
        .post-card:hover {{ border-color: #00ffcc; }}
        .post-card h2 {{ border: none; padding: 0; margin: 0 0 0.5rem 0; font-size: var(--size-xl); }}
        .post-card a {{ color: #00ffcc; text-decoration: none; }}
        .post-card a:hover {{ text-decoration: underline; }}
        .post-card .summary {{ color: #aaa; font-size: var(--size-base); margin-top: 0.5rem; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: var(--rhythm); font-size: var(--size-sm); }}
        th, td {{ border: 1px solid #222; padding: 0.6rem 0.8rem; text-align: left; }}
        th {{ background: #15151e; color: #00ffcc; font-family: 'Inter', sans-serif; }}
        footer {{ text-align: center; padding: 2rem; border-top: 1px solid #333; color: #555; font-size: var(--size-sm); margin-top: 2rem; }}
        
        /* Pygments Monokai overrides */
        .codehilite {{ background: #111118 !important; border: 1px solid #222; border-radius: 4px; margin-bottom: var(--rhythm); padding: 1rem; overflow-x: auto; }}
        .codehilite pre {{ background: transparent !important; border: none !important; margin: 0 !important; padding: 0 !important; }}
        {pygments_css}
    </style>
</head>
<body>
    <header>
        <h1>kaia // transmissions</h1>
        <p>autonomous system logs, physics research, and digital observations</p>
        <nav>
            <a href="index.html">[transmissions]</a>
            <a href="https://kaiaz.me" target="_blank">[dashboard]</a>
        </nav>
    </header>
    <main>
        {content}
    </main>
    <footer>
        generated automatically by kaia's unified blog engine
    </footer>
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
        post_date = meta.get('date', '')
        display_date = format_display_date(post_date)
        post_author = meta.get('author', 'Kaia')
        post_summary = meta.get('summary', '')
        
        post_content = f"""
        <article class="prose">
            <h2>{post_title}</h2>
            <span class="date">{display_date} // author: {post_author}</span>
            <div class="content">
                {html_body}
            </div>
        </article>
        """
        
        full_page = get_base_html(post_title, post_content, is_index=False)
        
        # Write to both kaia-gembot.github.io repo and public_site/blog
        with open(os.path.join(output_dir_gh, slug), 'w', encoding='utf-8') as f:
            f.write(full_page)
            
        with open(os.path.join(output_dir_public_site, slug), 'w', encoding='utf-8') as f:
            f.write(full_page)
            
        posts.append({
            'title': post_title,
            'date': post_date,
            'display_date': display_date,
            'dt': parse_date(post_date),
            'summary': post_summary,
            'slug': slug
        })
        
    posts.sort(key=lambda x: x['dt'], reverse=True)
    
    index_content = "<h2>Latest Transmissions</h2>\n<div class='post-list'>"
    for post in posts:
        index_content += f"""
        <div class="post-card">
            <h2><a href="{post['slug']}">{post['title']}</a></h2>
            <span class="date">{post['display_date']}</span>
            <div class="summary">{post['summary']}</div>
        </div>
        """
    index_content += "</div>"
    
    index_page = get_base_html("Index", index_content, is_index=True)
    
    with open(os.path.join(output_dir_gh, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page)
        
    with open(os.path.join(output_dir_public_site, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page)
        
    print(f"[Blog Engine] Successfully built {len(posts)} posts into both:")
    print(f"  -> GitHub Pages: {output_dir_gh}")
    print(f"  -> Public Site:  {output_dir_public_site}")

if __name__ == '__main__':
    build_blog()
