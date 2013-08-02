pivotal_tools
=============

Set of helper tools to rock your pivotal process.  On the Command Line of course

As of now, if only generates readme and changlogs.  But more to follow


install
-------

```bash
pip install git+ssh://git@github.com/jtushman/pivotal_tools.git
```


setup
-----
Add PIVOTAL_TOKEN to your environment

I put mine in ~/.zshenv, like so ...

`export PIVOTAL_TOKEN='your token'`

usage
-----

```bash
pivotal_tools generate_readme
pivotal_tools generate_changelog

pivotal_tools generate_changelog > changes.md
pivotal_tools generate_readme >> readme.md
```
