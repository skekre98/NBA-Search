# Contribution Guidelines

The current issue labels being handled are features, enhancements, and bugs.

### Feature Issue

This issue is meant for functional changes. Please provide the following information:
- The feature description
- Description of the implementation
- Why this would be a good `feature` to add

### Enhancement Issue

This issue is meant for non-functional changes. Please provide the following information:
- The enhancement description
- How you will add this enhancement
- Why this would be a good `enhancement` to add

### Bug Issue

This issue is meant for potential bugs. Please provide the following information:
- Bug description
- How to reproduce bug
- Technical specifications


### Pull requests

Please document any public function and class. At least required: 

* Function: Summary, Parameters, and Returns.
* Class: Summary and Attributes

### Update your fork

Is your fork not up-to-date with the NBA-Search code? Most of the time that isn't a problem. But if you like to "sync back" the changes to your repository, execute the following command:

The first time:
```
git remote add upstream https://github.com/skekre98/NBA-Search.git 
```

After that your repository will have two remotes. You could update your remote (the fork) in the following way:

```
git fetch upstream
git checkout <your feature branch>
git rebase upstream/master
..fix if needed and
git push -f 
```

if `rebase` won't work well, use `git merge master` as alternative.

It's also possible to send a PR in the opposite direction, but that's not preferred as it will pollute the commit log.
