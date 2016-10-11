#!/usr/bin/env python
'''$0 PREFIX

Parse the dpkg.cfg lines given on stdin, execute the "path-exclude" and
"path-include" lines according to dpkg(1) as if the root of all paths were
PREFIX, and print to stdout all paths which should be excluded.
'''

import sys
import os
import os.path
from fnmatch import fnmatch
from functools import partial


def should_exclude(path, rules):
    exclude = False

    for rule in rules:
        exclude = rule(path, exclude)

    return exclude


def list_excludes(root, rules, excludes):
    entries = os.listdir(root)
    paths = [os.path.join(root, e) for e in entries]
    has_child = False

    subdirs = [p for p in paths if os.path.isdir(p) and not os.path.islink(p)]
    for d in subdirs:
        subdir_has_child = list_excludes(d, rules, excludes)
        if subdir_has_child:
            has_child = True
        elif should_exclude(d, rules):
            excludes.append(d)
        else:
            has_child = True

    files = [p for p in paths if os.path.isfile(p) or os.path.islink(p)]
    for f in files:
        if should_exclude(f, rules):
            excludes.append(f)
        else:
            has_child = True

    return has_child


def build_rules(fobj, root):
    def exclude_rule(pattern, path, pending_exclusion):
        return pending_exclusion or fnmatch(path, pattern)

    def include_rule(pattern, path, pending_exclusion):
        return pending_exclusion and not fnmatch(path, pattern)

    rules = []
    for line in fobj:
        try:
            option, value = line.rstrip().split(None, 1)
        except ValueError:
            continue
        else:
            pattern = os.path.join(root, value[1:])
            if option == 'path-exclude':
                rule = partial(exclude_rule, pattern)
                rules.append(rule)
            elif option == 'path-include':
                rule = partial(include_rule, pattern)
                rules.append(rule)

    return rules


def main():
    root = sys.argv[1]
    rules = build_rules(sys.stdin, root)
    excludes = []
    list_excludes(root, rules, excludes)
    print '\n'.join(excludes)


if __name__ == "__main__":
    main()
