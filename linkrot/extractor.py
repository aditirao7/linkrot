#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Regexes for reference matching

Web url matching:
* http://daringfireball.net/2010/07/improved_regex_for_matching_urls
* https://gist.github.com/gruber/8891611
"""
from __future__ import absolute_import, division, print_function,\
 unicode_literals

import re

# arXiv.org
ARXIV_REGEX = r"""arxiv:\s?([^\s,]+)"""
ARXIV_REGEX2 = r"""arxiv.org/abs/([^\s,]+)"""

# DOI
DOI_REGEX = r"""DOI:\s?([^\s,]+)"""

# URL
URL_REGEX = r"""(?xi)
\b
(							# Capture 1: entire matched URL
  (?:
    [a-z][\w-]+:				# URL protocol and colon
    (?:
      /{1,3}						# 1-3 slashes
      |								#   or
      [a-z0-9%]						# Single letter or digit or '%'
      								# (Trying not to match e.g. "URI::Escape")
    )
    |							#   or
    www\d{0,3}[.]				# "www.", "www1.", "www2." … "www999."
    |							#   or
    [a-z0-9.\-]+[.][a-z]{2,4}/	# looks like domain name followed by a slash
  )
  (?:							# One or more:
    [^\s()<>]+						# Run of non-space, non-()<>
    |								#   or
    \(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
  )+
  (?:							# End with:
    \(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
    |									#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct char
  )
)
"""

def extract_urls(text):
    """
    This function will return all the unique URLs found in the `text` argument.

    - First we use the regex to find all matches for URLs
    - Finally we turn the list into a set, so we only end up with unique URLs\
     (no duplicates)
    """

    return set(re.findall(URL_REGEX, text, re.IGNORECASE))


def extract_arxiv(text):
    """
    This function will return all the unique occurences of `arvix.org/abs/` or\
     `arvix:`.

    - First we find all matches of the form `arvix:`
    - Then we find all matches of the form `arvic.org/abs/`
    - Then we concat them into a single list
    - Then we strip out any `.` from the start and end of any item in the list
    - Finally we turn the list into a set, so we only end up with unique URLs\
     (no duplicates)
    """

    res = re.findall(ARXIV_REGEX, text, re.IGNORECASE) + re.findall(
        ARXIV_REGEX2, text, re.IGNORECASE
    )
    return set([r.strip(".") for r in res])


def extract_doi(text):
    """
    This function will return all the unique DOIs found in `text` argument.

    - First we find all matches of the form `DOI:`
    - Then we strip out any `.` from the start and end of any item in the list
    - Finally we turn the list into a set, so we only end up with unique DOIs\
     (no duplicates)
    """

    res = set(re.findall(DOI_REGEX, text, re.IGNORECASE))
    return set([r.strip(".") for r in res])


if __name__ == "__main__":
    print(extract_arxiv("arxiv:123 . arxiv: 345 455 http://arxiv.org/abs/876"))
