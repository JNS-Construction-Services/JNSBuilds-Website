import os, re

root = r"C:\Users\nknig\Downloads\JNSConstruction\jnsconstructionservicesllcwebiste"

def disable_scripts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content

    # 1. GA4 External Loader
    content = re.sub(
        r'<script\s+async\s+src="https://www\.googletagmanager\.com/gtag/[^"]*"></script>',
        '<!-- GA4 external loader disabled: <script async src="https://www.googletagmanager.com/gtag/js?id=G-L28E0GQHBV"></script> -->',
        content
    )

    # 2. GA4 Inline / Deferred
    # Matches <script ...> ... G-L28E0GQHBV ... </script>
    # Only replace if not already disabled
    def ga4_replacer(match):
        header = match.group(1)
        body = match.group(2)
        footer = match.group(3)
        if 'type="text/plain"' in header or 'data-disabled' in header:
            return match.group(0)
        return f'<script type="text/plain" data-disabled="ga4">{body}</script>'

    content = re.sub(
        r'(<script[^>]*>)(\s*.*?(?:G-L28E0GQHBV).*?)(\s*</script>)',
        ga4_replacer,
        content,
        flags=re.DOTALL
    )

    # 3. Clarity Inline / Deferred
    # Matches <script ...> ... (function(c,l,a,r,i,t,y) ... wnhtr2nn8g ... </script>
    def clarity_replacer(match):
        header = match.group(1)
        body = match.group(2)
        footer = match.group(3)
        if 'type="text/plain"' in header or 'data-disabled' in header:
            return match.group(0)
        return f'<script type="text/plain" data-disabled="clarity">{body}</script>'

    content = re.sub(
        r'(<script[^>]*>)(\s*.*?\(function\(c,l,a,r,i,t,y\).*?wnhtr2nn8g.*?)(\s*</script>)',
        clarity_replacer,
        content,
        flags=re.DOTALL
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            if disable_scripts(filepath):
                print(f"Updated: {os.path.relpath(filepath, root)}")
            else:
                print(f"Skipped/No change: {os.path.relpath(filepath, root)}")
