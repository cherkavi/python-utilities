# parse git log output
# for replacing ` git cherry-pick -x <hash> ` commit 
#

import json
import sys
from typing import List, Generator


class GitLogRecord:
    def __init__(self, lines: List[str]):
        self.commit: str = None
        self.commit_replaced: str = None
        self.author: str = None
        self.message: List[str] = []

        for each_line in lines:
            if each_line.startswith("commit"):
                self.commit = each_line.split(" ")[1].strip()
                continue
            if each_line.startswith("Author"):
                self.author = each_line.split(" ")[1].strip()
                continue
            if each_line.startswith(" "):
                self.message.append(each_line)
            if each_line.startswith("    (cherry picked from commit"):
                self.commit_replaced = each_line.split(" ")[8].strip("\n)")

    def __str__(self) -> str:
        return json.dumps(
            {"commit": self.commit_value(), "message": self.message})
        # return f"{{commit:{self.commit}, commit_cherrypicked:{self.commit_replaced}, message:{self.message} }}"

    def commit_value(self) -> str:
        return self.commit_replaced if self.commit_replaced else self.commit

    def is_valid(self) -> bool:
        return self.commit is not None and self.author is not None and len(self.message) > 0


def log2record(logfile: str) -> Generator[GitLogRecord, None, None]:
    with open(logfile, mode="r") as file:
        chunk: List[str] = []
        for each_line in file:
            if each_line.startswith("commit") and len(chunk) > 0:
                next_record: GitLogRecord = GitLogRecord(chunk)
                if next_record.is_valid():
                    yield next_record
                chunk = []
            chunk.append(each_line)
        if len(chunk) > 0:
            next_record: GitLogRecord = GitLogRecord(chunk)
            if next_record.is_valid():
                yield next_record


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("first argument must contains filepath", file=sys.stderr)
        sys.exit(1)
    for each_record in log2record(sys.argv[1]):
        if len(sys.argv) > 2:
            print(each_record.commit_value())
        else:
            print(each_record)
