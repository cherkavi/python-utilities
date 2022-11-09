# git-check-branches

## git check merged branches

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/git-check-branches/git-check-merged-branches.py) -->
<!-- The below code snippet is automatically added from ../../python/git-check-branches/git-check-merged-branches.py -->
```py
import subprocess
import shutil
import os


DEFAULT_ENCODING = "utf-8"

def __clear_binary_line__(b_line):
    next_line = b_line.decode(DEFAULT_ENCODING)
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line.strip()


def cmd_result(arguments):
    result = list()
    with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for b_line in process.stdout:
            result.append(__clear_binary_line__(b_line))
    return result


if __name__=='__main__':
    ''' check git repository for all branches what was merged into specific branch '''
    git_folder = "c:\\project\\ccp-brand-server\\.git";
    control_branch_name = "/release"

    response = cmd_result(("git --git-dir %s branch --all" % (git_folder)).split(" "))
    response = [line for line in response if line.startswith('remotes/origin') and not(line.startswith('remotes/origin/HEAD')) and not(line.startswith('remotes/origin'+control_branch_name))]
    list_in_release = list()
    list_not_in_release = list()
    for each_branch in response:
        commit = cmd_result(  ("git --git-dir %s log -1 --oneline %s" % (git_folder, each_branch[8:]) ).split(" ") )[0].split(" ")[0]
        branches = cmd_result( ("git --git-dir %s branch --all --contains %s" % (git_folder, commit)).split(" ") )
        if(len([line for line in branches if control_branch_name in line])>0):
            list_in_release.append(each_branch)
        else:
            list_not_in_release.append(each_branch)

    print("in release:")
    for line in list_in_release:
        print(line)

    print("\n not in release:")
    for line in list_not_in_release:
        print(line)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


