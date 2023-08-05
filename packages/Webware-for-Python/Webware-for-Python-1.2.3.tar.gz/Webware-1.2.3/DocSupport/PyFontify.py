"""Module to analyze Python source code; for syntax coloring tools.

Interface:
    tags = fontify(pytext, searchfrom, searchto)

The 'pytext' argument is a string containing Python source code.
The (optional) arguments 'searchfrom' and 'searchto' may contain a slice in pytext.
The returned value is a list of tuples, formatted like this:
    [('keyword', 0, 6, None),
     ('keyword', 11, 17, None),
     ('comment', 23, 53, None), ...]
The tuple contents are always like this:
    (tag, startindex, endindex, sublist)
tag is one of ('comment', 'string', 'keyword', 'function', 'class')
sublist is not used, hence always None.
"""

# Based on FontText.py by Mitchell S. Chapman,
# which was modified by Zachary Roadhouse,
# then un-Tk'd by Just van Rossum.
# Many thanks for regular expression debugging & authoring are due to:
#    Tim (the-incredib-ly y'rs) Peters and Christian Tismer
# So, who owns the copyright? ;-) How about this:
# Copyright 1996-1997:
#    Mitchell S. Chapman,
#    Zachary Roadhouse,
#    Tim Peters,
#    Just van Rossum
#
# Version 0.4 - changes copyright (c) 2001 Mark Pilgrim (f8dy@diveintopython.org)
#   2001/02/05 - MAP - distinguish between class and function identifiers
#   2001/03/21 - MAP - get keywords from keyword module (instead of hard-coded list)
#   2001/03/22 - MAP - use re module instead of deprecated regex module
#
# 2005/09/09 - deprecated string functions removed by Christoph Zwerschke

__version__ = "0.4"

import re
import keyword

# Build up a regular expression which will match anything interesting,
# including multi-line triple-quoted strings.
commentPat = "#.*"

pat = "q[^\q\n]*(\\\\[\000-\377][^\q\n]*)*q"
quotePat = pat.replace("q", "'") + "|" + pat.replace('q', '"')

# Way to go, Tim!
pat = """
qqq
[^\\q]*
(
    (   \\\\[\000-\377]
    |   q
        (   \\\\[\000-\377]
        |   [^\\q]
        |   q
            (   \\\\[\000-\377]
            |   [^\\q]
            )
        )
    )
    [^\\q]*
)*
qqq
"""
pat = ''.join(pat.split())  # get rid of whitespace
tripleQuotePat = pat.replace("q", "'") + "|" + pat.replace('q', '"')

# Build up a regular expression which matches all and only Python keywords.
# This will let us skip the uninteresting identifier references.
# nonKeyPat identifies characters which may legally precede a keyword pattern.
nonKeyPat = "(^|[^a-zA-Z0-9_.\"'])"
keywordsPat = '|'.join(keyword.kwlist)
keyPat = nonKeyPat + "(" + keywordsPat + ")" + nonKeyPat

matchPat = keyPat + "|" + commentPat + "|" + tripleQuotePat + "|" + quotePat
matchRE = re.compile(matchPat)

idKeyPat = "[ \t]*[A-Za-z_][A-Za-z_0-9.]*"  # ident with leading whitespace
idRE = re.compile(idKeyPat)


def fontify(pytext, searchfrom=0, searchto=None):
    if searchto is None:
        searchto = len(pytext)
    tags = []
    commentTag = 'comment'
    stringTag = 'string'
    keywordTag = 'keyword'
    functionTag = 'function'
    classTag = 'class'

    start, end = 0, searchfrom
    while 1:
        matchObject = matchRE.search(pytext, end)
        if not matchObject:
            break
        start, end = matchObject.span()
        match = matchObject.group(0)
        c = match[0]
        if c not in "#'\"":
            # Must have matched a keyword.
            if start == searchfrom:
                # this is the first keyword in the text
                match = match[:-1]  # only a space at the end
            else:
                # there's still a redundant char before and after it
                match = match[1:-1]
                start += 1
            end -= 1
            tags.append((keywordTag, start, end, None))
            # If this was a defining keyword,
            # look ahead to the following identifier.
            if match in ('def', 'class'):
                idMatchObject = idRE.search(pytext, end)
                if idMatchObject:
                    start, end = idMatchObject.span()
                    match = idMatchObject.group(0)
                    tags.append((functionTag if match == 'def' else classTag,
                        start, end, None))
        elif c == "#":
            tags.append((commentTag, start, end, None))
        else:
            tags.append((stringTag, start, end, None))
    return tags


def test(path):
    with open(path) as f:
        text = f.read()
    tags = fontify(text)
    for tag, start, end, sublist in tags:
        print tag, repr(text[start:end]), start, end
