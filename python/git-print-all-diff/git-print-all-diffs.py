import subprocess
import shutil
import os
import sys

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

def cmd_result_print(arguments, skip_lines=[]):
    with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        index = 0
        for b_line in process.stdout:
            if not(index in skip_lines):
                print(__clear_binary_line__(b_line))
            index = index +1
    


def split_and_collect(values, index, splitter):
    return_value = list()
    for value in values:
        chains = value.split(splitter)
        if(len(chains)>index):
            return_value.append(chains[index])
    return return_value



if __name__=='__main__':
    ''' print all diffs for specific file '''
    if(len(sys.argv)<=2):
        print("two parameters should be specified : <path to .git folder> <full path to file>")
        exit()
    target_git_folder = sys.argv[1].strip() #"C:\\project\\brand-apis\\.git"
    target_filepath = sys.argv[2].strip() # "C:\\project\\brand-apis\\brand-schema\\pom.xml"

    target_git_filepath = target_filepath[len(target_git_folder)-4:]
    target_git_filepath_slash = target_git_filepath.replace("\\", "/")
    
    commits = split_and_collect(cmd_result(("git --git-dir %s log --oneline --follow %s" % (target_git_folder, target_git_filepath)).split(" ")), 0, " ")
    
    for index in range(0, len(commits)-1):
        cmd_result_print(
            ("git --git-dir %s diff %s:%s %s:%s" % (target_git_folder, commits[index], target_git_filepath_slash, commits[index+1], target_git_filepath_slash))
            .split(" "),
            [0, 2, 3, 4]
            )
