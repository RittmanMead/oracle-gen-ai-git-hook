# Oracle Generative AI Git Hook

This repository is an example of how to use Oracle Generative AI with Git to provide peer review of files being commited.

## pre-commit

The file called `pre-commit` should be placed in the directory `.git/hooks/`. The file needs to be executable which can be acheived by running:

```
chmod u+x .git/hooks/pre-commit
```

## oracle_ai_peer_review.py

The file called `oracle_ai_peer_review.py` should be stored in the root of your git repo. For this file to work you need to configure `~/.oci/config` and supply your compartment id in the variable called `ORACLE_COMPARTMENT_ID`.

