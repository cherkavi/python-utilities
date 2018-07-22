#!/usr/bin/env python3
import argparse
import datetime
'''
emulator of long-running application
settings file contains three lines:
1) answer before time out
2) predefined time
3) answer after time out
'''

def main(file_lines):
    print(file_lines)
    answer_before = file_lines[0]
    answer_after = file_lines[2]
    time_frontier = datetime.datetime.strptime(file_lines[1], "%H:%M")

    # difference between time only, compare time
    time_to_compare = datetime.time(time_frontier.hour, time_frontier.minute, 0)
    time_now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute, 0)

    print(time_to_compare, time_now)
    if time_now>time_to_compare:
        print(answer_after)
    else:
        print(answer_before)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read settings file and return first or third strings depends on timeout ')
    parser.add_argument('--settings_file',
                        help='three line file: 1) current return 2) time (20:35) when return third line 3) line with answer after timeout',
                        required=True)
    args = parser.parse_args()
    
    lines = list()
    with open(args.settings_file) as settings_file:
        for line in settings_file:
            clear_line = line.strip()
            if len(clear_line)>0:
                lines.append(clear_line)
    main(lines)