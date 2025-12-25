############################
##  application for showing/navigating in records list from script srt2tsv-remove-duplication
############################
## TabSeparatedValues should looks like 
# [19]    00:00:21,720    00:00:24,070    чем миллион долларов и обучил более 150
# [21]    00:00:24,080    00:00:26,029    учеников В этом видео вы узнаете Как
# [25]    00:00:28,880    00:00:31,470    используя уже готовые листинги не тратя

############################
## installation 
# pip install prompt_toolkit


############################

import os
import webbrowser
import argparse
import csv
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.filters import has_focus
from prompt_toolkit.layout.scrollable_pane import ScrollOffsets
from prompt_toolkit.data_structures import Point


parser = argparse.ArgumentParser(description="Read TSV data from a file.")
parser.add_argument("--data_file", required=True, help="Path to the TSV file")
parser.add_argument("--youtube_src", required=True, help="original video to open in youtube")
args = parser.parse_args()


def read_tsv_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            return list(reader)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def convert_to_youtube_timestamp(time_str):
    # Split the time and milliseconds (e.g., "00:04:50" and "720")
    time_part, _ = time_str.split(',')
    h, m, s = map(int, time_part.split(':'))
    
    # Calculate total seconds
    total_seconds = h * 3600 + m * 60 + s
    
    return f"&t={total_seconds}s"


class SubtitleBrowser:
    def __init__(self, data):
        self.data = data or []
        self.selected_index = 0
        self.yt_url = args.youtube_src
        self.search_buffer = Buffer()
        self.printed_value = None
        self.filtered_data = self.data
        
    def get_lines(self):
        search_term = self.search_buffer.text.lower()
        self.filtered_data = [
            row for row in self.data 
            if not search_term or (len(row) > 3 and search_term in row[3].lower())
        ]

        if self.selected_index >= len(self.filtered_data):
            self.selected_index = max(0, len(self.filtered_data) - 1)

        result = []
        for i, row in enumerate(self.filtered_data):
            style = 'reverse' if i == self.selected_index else ''
            prefix = " > " if i == self.selected_index else "   "
            line_text = f"{row[0]}  {row[1]}  {row[2]}  {row[3]}" if len(row) > 3 else str(row)
            result.append((style, f"{prefix}{line_text}\n"))
            
        if not result:
            return [('', " No matches found.")]
        return result

    def get_cursor_position(self):
        return Point(x=0, y=self.selected_index)

browser = SubtitleBrowser(read_tsv_data(args.data_file))

# --- UI Components ---
search_control = BufferControl(buffer=browser.search_buffer)
search_window = Window(content=search_control, height=1)

content_control = FormattedTextControl(
    browser.get_lines,
    get_cursor_position=browser.get_cursor_position
)

content_window = Window(
    content=content_control,
    scroll_offsets=ScrollOffsets(top=2, bottom=2),
    cursorline=False
)

# --- Key Bindings ---
kb = KeyBindings()
nav_filter = ~has_focus(search_control)

@kb.add('q', filter=nav_filter)
@kb.add('й', filter=nav_filter)
def _(event):
    if browser.filtered_data:
        row = browser.filtered_data[browser.selected_index]
        browser.printed_value = f"{row[1]}\t{row[2]}\t{row[3]}" if len(row) > 3 else str(row)
    event.app.exit()

@kb.add('j', filter=nav_filter)
@kb.add('о', filter=nav_filter)
@kb.add('down', filter=nav_filter)
def _(event):
    browser.selected_index = min(len(browser.filtered_data) - 1, browser.selected_index + 1)

@kb.add('k', filter=nav_filter)
@kb.add('л', filter=nav_filter)
@kb.add('up', filter=nav_filter)
def _(event):
    browser.selected_index = max(0, browser.selected_index - 1)

@kb.add('d', filter=nav_filter)
@kb.add('в', filter=nav_filter)
@kb.add('pagedown', filter=nav_filter)
def _(event):
    page_size = content_window.render_info.window_height if content_window.render_info else 10
    browser.selected_index = min(len(browser.filtered_data) - 1, browser.selected_index + page_size)

@kb.add('u', filter=nav_filter)
@kb.add('г', filter=nav_filter)
@kb.add('pageup', filter=nav_filter)
def _(event):
    page_size = content_window.render_info.window_height if content_window.render_info else 10
    browser.selected_index = max(0, browser.selected_index - page_size)

@kb.add('p', filter=nav_filter)
@kb.add('з', filter=nav_filter)
def _(event):
    if browser.filtered_data:
        browser.printed_value = browser.filtered_data[browser.selected_index][3]

@kb.add('y', filter=nav_filter)
@kb.add('н', filter=nav_filter)
def _(event):
    if browser.filtered_data:
        raw_ts = browser.filtered_data[browser.selected_index][1]                
        full_url = f"{browser.yt_url}{convert_to_youtube_timestamp(raw_ts)}"
        webbrowser.open(full_url)

@kb.add('/')
@kb.add('.')
def _(event):
    event.app.layout.focus(search_window)

@kb.add('escape')
def _(event):
    current_id = None
    if browser.filtered_data and len(browser.filtered_data) > 0:
        current_id = browser.filtered_data[browser.selected_index][0]

    browser.search_buffer.text = ""
    
    if current_id:
        for i, row in enumerate(browser.data):
            if row[0] == current_id:
                browser.selected_index = i
                break
    
    event.app.layout.focus(content_window)

@kb.add('enter')
def _(event):
    if event.app.layout.has_focus(search_window):
        event.app.layout.focus(content_window)

# --- Layout ---
root_container = HSplit([
    content_window,
    Window(height=1, char='─', style='class:line'),
    VSplit([
        Window(FormattedTextControl(" SEARCH: "), width=9, style="bold"),
        search_window,
    ]),
    Window(content=FormattedTextControl(
        HTML(" <ansigray><b>[j/k/u/d]</b> Nav  <b>[/ .]</b> Search  <b>[y]</b> YT  <b>[p]</b> Print  <b>[Esc]</b> Reset  <b>[q]</b> Quit</ansigray>")
    ), height=1, style="bg:#222222")
])

# focused_element=content_window ensures we start in navigation mode
app = Application(
    layout=Layout(root_container, focused_element=content_window),
    key_bindings=kb,
    full_screen=True
)

if __name__ == "__main__":
    app.run()
    if browser.printed_value:
        print(f"\n {browser.printed_value}")