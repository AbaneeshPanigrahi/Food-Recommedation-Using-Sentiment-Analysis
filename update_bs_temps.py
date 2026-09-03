import os
import re

template_dir = r"d:\Food Recommedation Using Sentiment Analysis\templates"

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace CSS
        content = content.replace(
            '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">',
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">'
        )

        # Replace JS
        content = re.sub(
            r'<script src="https://code\.jquery\.com/jquery-3\.5\.1\.slim\.min\.js"></script>[\s\S]*?<script src="https://stackpath\.bootstrapcdn\.com/bootstrap/4\.5\.2/js/bootstrap\.min\.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>',
            content
        )

        # Replace data attributes
        content = content.replace('data-toggle="', 'data-bs-toggle="')
        content = content.replace('data-target="', 'data-bs-target="')
        content = content.replace('data-dismiss="', 'data-bs-dismiss="')

        # Replace spacing utilities (Bootstrap 4 -> 5: left/right -> start/end)
        content = re.sub(r'\bml-(\d+|auto)\b', r'ms-\1', content)
        content = re.sub(r'\bmr-(\d+|auto)\b', r'me-\1', content)
        content = re.sub(r'\bpl-(\d+|auto)\b', r'ps-\1', content)
        content = re.sub(r'\bpr-(\d+|auto)\b', r'pe-\1', content)
        
        # Flash message close buttons need the btn-close class instead of times
        content = re.sub(
            r'<button type="button" class="close" data-bs-dismiss="alert" aria-label="Close">\s*<span aria-hidden="true">&times;</span>\s*</button>',
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            content
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Updated {filename}")
