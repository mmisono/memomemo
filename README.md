# memomemo.py
- Generate a list of memos

# Example
- See `example/` directory. [README.md](./example/README.md) is generated from `cd example && python ../memomemo.py`

# Supported File Types
- Markdown
    - See [markdown example](./example/markdown/foo.md) to know how to add metadata (title & tags)
- Ipynb
    - See [ipynb example](./example/ipynb/sin.ipynb) metadata "memomemo" section to know how to add metadata (title & tags)
    - You can add metadata by directly editing `.ipynb` file or open file with `ipython notebook` and `Edit -> Edit Notebook Metadata`.

# NOTE
- `memomemo.py` checks mtime of each file and only process the file which was created later than the mtime of `README.md`. If you want do all over again please remove `README.md` and retry.
