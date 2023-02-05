# pip install GitPython

path_to_git:str="/home/projects/python-utilities"
git_repo=git.Repo(path_to_git)

git_repo.heads

git_repo.active_branch

git_repo.remotes()
