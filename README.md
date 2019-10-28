# personal website

## The `index.py` file

It is kinda like a quine in a sense that when it runs, it writes
itself to `index.html`. The condition is the requirements need to be
installed.

## Running

After cloning this repo, run:

```shell
git submodule update --init --recursive
```

This will pull the `gruvbox-theme` submodule.

Then, run:

```shell
pipenv install
```

This will install the required python dependencies.

Now, just run:

```
pipenv run ./index.py
```
