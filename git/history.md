## it is not possible to preserve cherry-picked git-hash in destination branch
![image](https://user-images.githubusercontent.com/8113355/198723432-23cc0b63-c028-4a1f-85f3-45486408ea83.png)

```sh
git init .
git status
touch file.txt
echo "init" >> file.txt
git add file.txt
git commit --message 'init commit'
git log -1 --oneline
# 4df7fdc (HEAD -> master) init commit
echo "2.step" >> file.txt
git add file.txt
git commit --message "2.step"
```

```sh
git checkout -b release
echo "3.step " >> file.txt
git add file.txt
git commit --message "3.step"
git log --oneline
# e4fe8f7 (HEAD -> release) 3.step
# 4e4b490 (master) 2.step
# 4df7fdc init commit
```

```sh
git checkout master
echo "4.step" >> file.txt
git add file.txt
git commit --message "4.step"
git log --oneline
# 1702149 (HEAD -> master) 4.step
# 4e4b490 2.step
# 4df7fdc init commit
```

```sh
git checkout -b bug-fix
echo "5.step " >> file.txt
git add file.txt
git commit --message "5.step"
git log --oneline
# 7389312 (HEAD -> bug-fix) 5.step
# 1702149 (master) 4.step
# 4e4b490 2.step
# 4df7fdc init commit
```

```sh
git checkout release
git cherry-pick 7389312
git add file.txt
git cherry-pick --continue
git log --oneline
# febc79f (HEAD -> release) 5.step
# e4fe8f7 3.step
# 4e4b490 2.step
# 4df7fdc init commit

git reset --hard e4fe8f7
```

 
### not working solutions
```
git cherry-pick --keep-redundant-commits 7389312 
git cherry-pick --strategy=merge 7389312 
git cherry-pick -m 1 7389312 
git merge 7389312 
git rebase --onto bug-fix 7389312 7389312
```
