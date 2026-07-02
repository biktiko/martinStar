import os
import glob

for f in glob.glob('apps/**/*.py', recursive=True):
    content = open(f).read()
    if '\\\"' in content:
        content = content.replace('\\\"', '\"')
        open(f, 'w').write(content)
