import re
import sys
import os

class Subtitle:
    def __init__(self, index, start_time, end_time, text_lines):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text_lines

    def __repr__(self):
        return f"Subtitle(#{self.index}, Lines: {len(self.text)})"

def parse_srt_content(content):
    # Updated Regex:
    # (.*?) matches text greedily but stops at the lookahead.
    # (?=\n\s*\n\d+|\n\d+\s*\n|\Z) looks for the next block or end of file.
    pattern = re.compile(r'(\d+)\s+([\d:,]+) --> ([\d:,]+)\s*(.*?)(?=\n\d+\s*\n|\Z)', re.DOTALL)
    
    subtitles = []
    for match in pattern.finditer(content):
        index = int(match.group(1))
        start_time = match.group(2)
        end_time = match.group(3)
        
        # Capture raw text and clean it
        raw_text = match.group(4).strip()
        
        # Handle non-breaking spaces (\xa0) and other whitespace
        # We split, strip, and filter out strings that are empty or just whitespace
        text_lines = [line.strip() for line in raw_text.split('\n')]
        text_lines = [line for line in text_lines if line and not line.isspace()]
        
        # If the block was just whitespace/blank, text_lines will be an empty list []
        subtitles.append(Subtitle(index, start_time, end_time, text_lines))
    
    return subtitles

def parse_srt_sequentially(file_path):
    subtitles = []
    
    if not os.path.exists(file_path):
        return subtitles

    with open(file_path, 'r', encoding='utf-8') as f:
        # Read lines and strip trailing whitespace/newlines
        lines = [line.rstrip('\n\r') for line in f]

    current_index = None
    current_times = None
    current_text = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 1. Look for the Index (must be a digit)
        if line.isdigit():
            # If we were already building a subtitle, save it before starting new
            if current_index is not None:
                subtitles.append(Subtitle(current_index, current_times[0], current_times[1], current_text))
            
            current_index = int(line)
            current_text = []
            i += 1
            
            # 2. The very next line MUST be the timestamp
            if i < len(lines) and "-->" in lines[i]:
                times = lines[i].split("-->")
                current_times = (times[0].strip(), times[1].strip())
                i += 1
            continue

        # 3. Collect text lines
        # We ignore lines that are just whitespace or the non-breaking space \xa0
        clean_line = line.replace('\xa0', '').strip()
        if clean_line:
            current_text.append(clean_line)
        
        i += 1

    # Don't forget to add the last subtitle after the loop ends
    if current_index is not None:
        subtitles.append(Subtitle(current_index, current_times[0], current_times[1], current_text))

    return subtitles


def load_srt_file(file_path):
    """Reads the file and returns a list of Subtitle objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return parse_srt_content(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def clean_repeated_lines(subtitles):
    """
    Checks if the last line of a subtitle object is the same as the 
    first line of the subsequent subtitle object. If so, removes 
    it from the current object.
    """
    # We iterate up to len - 1 because the last item has no 'next' to compare to
    for i in range(len(subtitles) - 1):
        current_sub = subtitles[i]
        next_sub = subtitles[i + 1]

        # Ensure both objects have text lines to compare
        if current_sub.text and next_sub.text:
            last_line_current = current_sub.text[-1]
            first_line_next = next_sub.text[0]

            if last_line_current == first_line_next:
                # Remove the last element from the current list
                current_sub.text.pop()
    
    return subtitles

def remove_empty_subtitles(subtitles):
    """
    Returns a new list containing only subtitle objects 
    that have at least one line of text.
    """
    # This creates a new list including only objects where sub.text is not empty
    return [sub for sub in subtitles if len(sub.text) > 0]

# --- Execution ---
# Replace 'your_file.srt' with the actual path to your subtitle file
file_name = sys.argv[1]
# subtitle_objects = load_srt_file(file_name)
subtitle_objects = parse_srt_sequentially(file_name)

# Verify the result
for sub in remove_empty_subtitles(clean_repeated_lines(subtitle_objects)):
    print(f"[{sub.index}]\t{sub.start_time}\t{sub.end_time}\t{"".join(sub.text)}")