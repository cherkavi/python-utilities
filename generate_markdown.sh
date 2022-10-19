#!/usr/bin/env bash
# Generate the list of markdown files from the directory structure
# Essentially to provide a documentation of the python scripts
# Usage: ./generate_markdown.sh
set -e

# Get the destination directory where the files will be generated
DEST_DIR=${1:-.}
CURRENT_DIR=$(pwd)

# Get the list of files
files=$(find . -type f -name "*.py" | sort)

readonly DEST_DIR CURRENT_DIR files

# Print the header
echo "Documentation"
echo "The scripts are grouped by directory, and the scripts are sorted alphabetically. sub directories are added as headers."
echo

# LOG the files
echo "Found files (total: $(echo "$files" | wc -l))"
echo "Generated on $(date)"
echo "DEST_DIR: $DEST_DIR"

# Function to generate the markdown
function generate_markdown {

    # Markdown file name
    local file_name="$1"
    local markdown_dir="$CURRENT_DIR/$DEST_DIR"
    local markdown_name="$markdown_dir/$(basename "$file_name" .py).md"
    echo "Generating markdown for $file_name -> $markdown_name"

    local header=$(basename "$file_name" .py)
    echo "
## ${header//-/ }
\`\`\`python
$file_name
\`\`\`
" >> "$markdown_name"
}

echo "Generating markdown files"
for file in $files; do
    generate_markdown "$file"
done
