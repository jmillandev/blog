#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub Pages...\033[0m"

cd public

if [ -n "$BOT_GITHUB_AUTH_SECRET" ]
then
    touch ~/.git-credentials
    chmod 0600 ~/.git-credentials
    echo $BOT_GITHUB_AUTH_SECRET > ~/.git-credentials

    git config credential.helper store
    git config user.email "jmillandev-blog-bot@users.noreply.github.com"
    git config user.name "jmillandev-blog-bot"
fi

git add .
git commit -m "Rebuild site"
git push --force origin HEAD:master
