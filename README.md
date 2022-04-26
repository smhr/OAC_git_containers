## Git for scientists

![Final doc!](https://phdcomics.com/comics/archive/phd101212s.gif "My git notes")

[A Quick Introduction to Version Control with Git and GitHub](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004668)

[git_4_sci](https://milesmcbain.github.io/git_4_sci/index.html)

## git and jupyter

https://jupytext.readthedocs.io/en/latest/index.html
https://medium.com/capital-fund-management/automated-reports-with-jupyter-notebooks-using-jupytext-and-papermill-619e60c37330
https://www.reviewnb.com
https://blog.reviewnb.com/github-jupyter-notebook/

## Good git tutorial

https://www.git-scm.com/book
https://www.atlassian.com/git/tutorials/learn-git-with-bitbucket-cloud
https://swcarpentry.github.io/git-novice/

## Setting up git

```sh
git config --global user.name "Moha Rad"
git config --global user.email "Moha@email.com"
```

For this lesson, we will be interacting with GitHub and so the email address used should be the same as the one used when setting up your GitHub account. If you are concerned about privacy, please review GitHub’s instructions for keeping your email address private.

---

Initializing a git repository in your current directory.

```sh
git init
```

```sh
ls -a
```

You will see a `.git` directory is created and will be controlled by git.

---

## Stashing

Often, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The problem is, you don’t want to do a commit of half-done work just so you can get back to this point later. The answer to this issue is the `git stash` command.

Stashing takes the dirty state of your working directory - that is, your modified tracked files and staged changes - and saves it on a stack of unfinished changes that you can reapply at any time (even on a different branch).

```sh
git stash
```

Re-applying your stashed changes

The `git stash pop` removes the changes from your stash and re-applies them to your working copy. The alternate way is running `git stash apply` if you want to re-apply the changes and keep them in your stash.

A good article about stashing example: https://medium.com/javarevisited/git-stash-when-and-how-to-use-6f5dc1bb2ee0

The `git stash` will stash the changes that have been added to your index (staged changes) and changes made to files currently tracked by Git (unstaged changes). It will not stash the new files in the working copy that have not yet been staged and ignored files. In these cases, the `git stash -u` option (or `--include-untracked`) helps to stash the untracked files.

You can add changes to ignored files as well by using the `-a` option (or `--all`) when running git stash.

---

## Tagging

To create a lightweight new tag run

```sh
git tag <tagname>
```

Annotated tags are stored as full objects in the Git database. To reiterate, They store extra meta data such as: the tagger name, email, and date. Similar to commits and commit messages Annotated tags have a tagging message.

```sh
git tag -a v2.7
```

To list all tags

```sh
git tag
```

To push tags to the remote

```sh
git push origin v2.7
```

---

## Some points

### What is Git ref, head and HEAD?

Git **refs** and Git **heads** are simply pointers to commits, in the form of text files where the file name represents the name of the ref/head and the content is the commit ID that the ref points to.

**head** is a general term that means any commit that represents a branch tip. **HEAD** is a specific Git ref that always points to the commit currently checked out in the working directory.

A **detached HEAD** state, which means that HEAD is not currently pointing to a branch head (branch tip).

### switch vs checkout

https://stackoverflow.com/questions/57265785/whats-the-difference-between-git-switch-and-git-checkout-branch

| previous command                                      | new command                                                                  |
| ----------------                                      | -----------                                                                  |
| `git checkout <branch>`                               | `git switch <branch>`                                                        |
| `git checkout`                                        | N/A (use `git status`)                                                       |
| `git checkout -b <new_branch> [<start_point>]`        | `git switch -c <new-branch> [<start-point>]`                                 |
| `git checkout -B <new_branch> [<start_point>]`        | `git switch -C <new-branch> [<start-point>]`                                 |
| `git checkout --orphan <new_branch>`                  | `git switch --orphan <new-branch>`                                           |
| `git checkout --orphan <new_branch> <start_point>`    | N/A (use `git switch <start-point>` then `git switch --orphan <new-branch>`) |
| `git checkout [--detach] <commit>`                    | `git switch --detach <commit>`                                               |
| `git checkout --detach [<branch>]`                    | `git switch --detach [<branch>]`                                             |
| `git checkout [--] <pathspec>…`                       | `git restore [--] <pathspec>…`                                               |
| `git checkout --pathspec-from-file=<file>`            | `git restore --pathspec-from-file=<file>`                                    |
| `git checkout <tree-ish> [--] <pathspec>…`            | `git restore -s <tree> [--] <pathspec>…`                                     |
| `git checkout <tree-ish> --pathspec-from-file=<file>` | `git restore -s <tree> --pathspec-from-file=<file>`                          |
| `git checkout -p [<tree-ish>] [--] [<pathspec>…]`     | `git restore -p [-s <tree>] [--] [<pathspec>…]`                              |





