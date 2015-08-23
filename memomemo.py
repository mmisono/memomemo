#!/usr/bin/env python

# -*- coding: utf-8 -*-

import json
import os
import os.path
import time

README_FILE_NAME = "README.md"

def find_files(mtime):
    """ find files which was created later than the mtime
    """
    r = []
    for dirpath, dirnames, filenames in os.walk("."):

        exclude_dirs = [".git","tags",".ipynb_checkpoints"]
        for e in exclude_dirs:
            if e in dirnames:
                dirnames.remove(e)

        exclude_files = [README_FILE_NAME]
        for e in exclude_files:
            if e in filenames:
                filenames.remove(e)

        for filename in filenames:
            f = os.path.join(dirpath,filename)
            mt = os.path.getmtime(f)
            if mt > mtime:
                r.append((f,mt))

    return sorted(r, key = lambda x: -x[1])

def get_metadata_md(filename):
    """ get metadata from md
        1. extract pandoc style titles, i.e.
        ```
           % TITLE
           % AUTHOR
           % DATE
        ```
        2. extract tags information from top of file if any
        ```
        <!--
          tags: foo,bar,baz
        -->
        ```
    """

    r = {"title": os.path.basename(filename), "tags":[]}
    with open(filename,"r") as f:
        line = f.readline()
        if line[0] == "%":
            r["title"] = line[1:].strip()
        for i in range(10): # check only top 10 lines
            line = f.readline()
            if line.strip()[:5] == "tags:":
                r["tags"] = [w.strip() for w in line.strip()[5:].split(",")]

    return r

def get_metadata_ipynb(filename):
    """ get metadata from ipynb
        check ipynb "metadata" section
    """
    r = {"title": os.path.basename(filename), "tags":[]}

    with open(filename,"r") as f:
        data = json.loads(f.read())
        if "memomemo" in data["metadata"]:
            if "title" in data["metadata"]["memomemo"]:
                r["title"] = data["metadata"]["memomemo"]["title"]
            if "tags" in data["metadata"]["memomemo"]:
                r["tags"] = data["metadata"]["memomemo"]["tags"]

    return r

def get_metadata(filename):
    if os.path.splitext(filename)[1] == ".md":
        return get_metadata_md(filename)
    if os.path.splitext(filename)[1] == ".ipynb":
        return get_metadata_ipynb(filename)

    return {"title": os.path.basename(filename), "tags":[]}

def update(files):
    """ update README and tags
    """
    lines = ""
    for f in files:
        d = get_metadata(f[0])
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f[1]))
        lines += "- {0}: [{1}]({2})\n".format(t,d["title"],f[0])
        if len(d["tags"]) > 0:
            lines += "    - "+', '.join(d["tags"]) + "\n"

    with open(README_FILE_NAME,"r+") as f:
        content = f.read()
        f.seek(0,0)
        f.write(lines+content)

def create_readme():
    """ create empty README.md
    """
    with open(README_FILE_NAME,"w") as f:
        pass

def get_readme_modified_time():
    """ get mtime of README.md
    """
    if not os.path.exists(README_FILE_NAME):
        create_readme()
        return 0
    mtime = os.path.getmtime(README_FILE_NAME)
    return mtime

def main():
    """ entry point
    """
    mtime = get_readme_modified_time()
    files = find_files(mtime)
    update(files)

if __name__ == "__main__":
    main()
