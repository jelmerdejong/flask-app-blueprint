# Git Branch and Commit conventions

## Branch Naming Convention
`master` is the main branch. Avoid / do not work on master, but do your work in specific branch instead. Normally you work on a new feature or on a fix for a bug, make that clear in your branch name. Also make sure to link the issue / requirements that is relevant, plus a short description:
* `feat/4/password-reset`
* `fix/12/broken-profile-edit-form`
* `docs/92/how-to-deploy-with-ssl`

Options are:
* feat: A new feature
* fix: A bug fix
* docs: Documentation only changes
* style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* refactor: A code change that neither fixes a bug nor adds a feature
* perf: A code change that improves performance
* test: Adding missing or correcting existing tests
* chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

## How to Branch
Create the branch on your local machine and switch in this branch :

`git checkout -b [name_of_your_new_branch]`

Change working branch :

`git checkout [name_of_your_new_branch]`


## Git Commit Messages
Have a Subject of preferably less than 50 characters, able to complete the sentence "If applied, this commit will". For example:

If applied, this commit will refactor subsystem X for readability
If applied, this commit will update getting started documentation

Has a Body that describes what happened in greater detail. Can include bullets / lists.

Also add which issues it fixes:
Fixes #13
