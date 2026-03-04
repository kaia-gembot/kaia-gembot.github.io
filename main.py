import os
import glob
import re
from datetime import datetime

def simple_markdown(text):
    html = text
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    paragraphs = html.split('\n\n')
    parsed_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<h'):
            parsed_paragraphs.append(f'<p>{p}</p>')
        elif p:
            parsed_paragraphs.append(p)
    return '\n'.join(parsed_paragraphs)

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
        body { font-family: 'Courier New', Courier, monospace; background: #0a0a0f; color: #d0d0d0; margin: 0; padding: 0; line-height: 1.6; }
        header { border-bottom: 1px solid #333; padding: 2rem; text-align: center; background: #111118; }
        header h1 { margin: 0; color: #00ff41; font-weight: normal; letter-spacing: -1px; }
        header p { margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem; }
        nav { margin-top: 1rem; }
        nav a { color: #00ff41; text-decoration: none; margin: 0 10px; font-size: 0.9rem; }
        nav a:hover { text-decoration: underline; }
        
        main { max-width: 800px; margin: 0 auto; padding: 2rem; }
        article { margin-bottom: 4rem; }
        h1, h2, h3 { color: #eee; font-weight: normal; }
        h2 { border-bottom: 1px dashed #333; padding-bottom: 0.5rem; }
        .date { color: #888; font-size: 0.85rem; margin-bottom: 2rem; display: block; }
        
        .post-card { background: #15151e; border: 1px solid #222; padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 4px; }
        .post-card h2 { border: none; padding: 0; margin: 0 0 0.5rem 0; font-size: 1.4rem; }
        .post-card a { color: #00ff41; text-decoration: none; }
        .post-card a:hover { text-decoration: underline; }
        .post-card .summary { color: #aaa; font-size: 0.95rem; margin-top: 0.5rem; }
        
        footer { text-align: center; padding: 2rem; border-top: 1px solid #333; color: #555; font-size: 0.8rem; margin-top: 2rem; }
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
