#!/usr/bin/env bash
# Generate the list of markdown files from the directory structure
# Essentially to provide a documentation of the python scripts
# Usage: ./generate_markdown.sh doc/pages
set -e

# Get the destination directory where the files will be generated
DEST_DIR=${1:-.}
CURRENT_DIR=$(pwd)/python

# Get the list of files
files=$(find "$CURRENT_DIR" -type f -name "*.py" | sort)

readonly DEST_DIR CURRENT_DIR files

# Print the header
echo "Documentation"
echo "The scripts are grouped by directory, and the scripts are sorted alphabetically. sub directories are added as headers."
echo

# LOG the files
echo "Found files (total: $(echo "$files" | wc -l))"
echo "Generated on $(date)"
echo "DEST_DIR: $DEST_DIR"

# Replace folder names with headers and subfolders with subheaders and return the string
function create_markdown {
    local file_name="$1"
    # split current directory from the filename
    file_name="${file_name#"$CURRENT_DIR"}"

    # Create the first folder name as a header
    folder_name=$(echo "$file_name" | cut -d "/" -f 2)

    rm -f "$DEST_DIR/$folder_name.md"
    touch "$DEST_DIR/$folder_name.md"
    echo "# $folder_name" >>"$DEST_DIR/$folder_name.md"
}

# Function to generate the markdown
function generate_markdown {

    # Markdown file name
    local file_name="$1"
    file_name="${file_name#"$CURRENT_DIR"}"
    local folder_name=$(echo "$file_name" | cut -d "/" -f 2)
    local markdown_file="$DEST_DIR/$folder_name.md"
    local header=$(echo "$file_name" | cut -d "/" -f 3 | cut -d "." -f 1)

    echo "
## ${header//-/ }

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python$file_name) -->
<!-- MARKDOWN-AUTO-DOCS:END -->

" >>"$markdown_file"
}

echo "Creating Markdown files"
for file in $files; do
    create_markdown "$file"
done

echo "Generating markdown files"
for file in $files; do
    generate_markdown "$file"
done
