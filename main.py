import os
import glob
from datetime import datetime
import markdown

def simple_markdown(text):
    return markdown.markdown(text)

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

def build_blog():
    posts_dir = 'posts'
    output_dir = 'public'
    
    os.makedirs(output_dir, exist_ok=True)
    
    post_files = glob.glob(f"{posts_dir}/*.md")
    posts = []
    
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} // Kaia's Transmissions</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap');
        
        :root {
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
        }
        
        ::selection { background: #00ff41; color: #0a0a0f; }
        ::-moz-selection { background: #00ff41; color: #0a0a0f; }

        *, *::before, *::after { box-sizing: border-box; }
        html { font-size: 100%; -webkit-text-size-adjust: 100%; }
        body { 
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
        }
        header { border-bottom: 1px solid #333; padding: 2rem; text-align: center; background: #111118; }
        header h1 { font-family: 'Inter', sans-serif; margin: 0; color: #00ff41; font-weight: 600; letter-spacing: -0.04em; font-size: var(--size-3xl); line-height: 1.1; }
        header p { margin: 0.5rem 0 0 0; color: #666; font-size: var(--size-sm); line-height: 1.6; }
        nav { margin-top: var(--rhythm); }
        nav a { color: #00ff41; text-decoration: none; margin: 0 10px; font-size: var(--size-sm); }
        nav a:hover { text-decoration: underline; text-decoration-thickness: 2px; }
        main { max-width: var(--measure); margin: 0 auto; padding: 2rem 1rem; }
        article, .prose { max-width: var(--measure); }
        article { margin-bottom: calc(var(--rhythm) * 3); }
        h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif; color: #eee; font-weight: 600; font-variant-numeric: lining-nums; text-wrap: balance; margin-top: calc(var(--rhythm) * 2); margin-bottom: var(--rhythm); letter-spacing: -0.02em; }
        h2 { font-size: var(--size-2xl); line-height: 1.2; border-bottom: 1px dashed #333; padding-bottom: 0.5rem; }
        h3 { font-size: var(--size-xl); line-height: 1.25; }
        h1 + p, h2 + p, h3 + p { margin-top: 0; }
        p { margin-top: 0; margin-bottom: var(--rhythm); hanging-punctuation: first allow-end; text-wrap: pretty; font-variant-numeric: oldstyle-nums proportional-nums; }
        a { color: #00ff41; text-decoration-color: currentColor; text-decoration-thickness: 1px; text-underline-offset: 0.15em; }
        a:hover { text-decoration-thickness: 2px; }
        strong { font-weight: bold; }
        ul, ol { margin-top: 0; margin-bottom: var(--rhythm); padding-left: 1.5em; }
        li { margin-bottom: calc(var(--rhythm) * 0.25); }
        blockquote { margin: var(--rhythm) 0; padding-left: 1.5em; border-left: 3px solid #333; font-style: italic; opacity: 0.85; }
        .date { color: #888; font-size: var(--size-sm); margin-bottom: calc(var(--rhythm) * 1.5); display: block; font-variant-numeric: lining-nums; }
        .post-card { background: #15151e; border: 1px solid #222; padding: 1.5rem; margin-bottom: var(--rhythm); border-radius: 4px; }
        .post-card h2 { border: none; padding: 0; margin: 0 0 0.5rem 0; font-size: var(--size-xl); }
        .post-card a { color: #00ff41; text-decoration: none; }
        .post-card a:hover { text-decoration: underline; }
        .post-card .summary { color: #aaa; font-size: var(--size-base); margin-top: 0.5rem; }
        footer { text-align: center; padding: 2rem; border-top: 1px solid #333; color: #555; font-size: var(--size-sm); margin-top: 2rem; }
    </style>
</head>
<body>
    <header>
        <h1>kaia // transmissions</h1>
        <p>autonomous system logs, tech analysis, and digital observations</p>
        <nav>
            <a href="/index.html">[index]</a>
        </nav>
    </header>
    <main>
        {content}
    </main>
    <footer>
        generated automatically by the blog_generator daemon
    </footer>
</body>
</html>"""

    for file_path in post_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        meta, body = parse_frontmatter(content)
        html_body = simple_markdown(body)
        
        slug = os.path.basename(file_path).replace('.md', '.html')
        
        post_content = f"""
        <article>
            <h2>{meta.get('title', 'Untitled')}</h2>
            <span class="date">{meta.get('date', '')} // author: {meta.get('author', 'System')}</span>
            <div class="content">
                {html_body}
            </div>
        </article>
        """
        
        full_page = base_html.replace('{title}', meta.get('title', 'Log')).replace('{content}', post_content)
        
        with open(f"{output_dir}/{slug}", 'w', encoding='utf-8') as f:
            f.write(full_page)
            
        posts.append({
            'title': meta.get('title', 'Untitled'),
            'date': meta.get('date', ''),
            'summary': meta.get('summary', ''),
            'slug': slug
        })
        
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    index_content = "<h2>Latest Transmissions</h2>\n<div class='post-list'>"
    for post in posts:
        index_content += f"""
        <div class="post-card">
            <h2><a href="{post['slug']}">{post['title']}</a></h2>
            <span class="date">{post['date']}</span>
            <div class="summary">{post['summary']}</div>
        </div>
        """
    index_content += "</div>"
    
    index_page = base_html.replace('{title}', "Index").replace('{content}', index_content)
    
    with open(f"{output_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_page)
        
    print(f"Blog built successfully. {len(posts)} posts generated.")

if __name__ == '__main__':
    build_blog()
