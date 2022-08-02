The script `arxiv_checker.py` will query arXiv for papers by authors listed in
sections of `config.ini` that have been updated/submitted since the `last
digest` time stored in `database.ini`, and write a local digest to
`~/downloads/arxiv-digest-#.html`.

A poor man's installation
-------------------------
- Clone the repo
- `chmod +x arxiv_checker.py` and symlink it into `/usr/local/bin`
- Have a `/usr/bin/python3` installed and `pip install arxiv`
- Run it as a `crontab` or execute it from `.bashrc`.  Currently it will only
  write a digest on Monday or if 1 week has elapsed since the last digest.
