#!/usr/bin/env python
# -*- coding: utf-8 mode: python -*-
#
# LaTeXStripper.py - A small tool to get rid of LaTeX code in .tex files 
# to be able to run them through a bag-of-words algorithm 
# (like e.g. WordCloud) and get reasonable results.
#
# Copyright (c) 2016 J. Walkenhorst
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free So2tware
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import re

#autofunction:: strip()


def delete_comment(line: str) -> str:
    """Delete latex comment from a string (delete everything following a %, but not following a \%)."""
    return re.sub(r"(?<!\\)(%.*)", "", line)


def delete_formula(my_text):
    """Deletes all formulas in a text, i.e. everything of the form $...$. \
       Wrapper around delete_pattern."""
    my_text = re.sub(r"(\$[^\$]+\$)", "", my_text)
    return my_text


def load_file_without_comments(filename: str) -> str:
    with open(filename, 'r') as f:
        lines = f.readlines()
    return ' '.join([delete_comment(l.strip('\n')).strip() for l in lines])


def extract_document(latexdocument):
    try:
        return re.findall(r"\\begin{document}([.\S\s]*)\\end{document}", latexdocument)[0].strip()
    except IndexError:
        print("Document contains no body")


def strip(filename):
    """ A small tool to get rid of LaTeX code in .tex files 
        to be able to run them through a bag-of-words algorithm 
        (like e.g. WordCloud) and get reasonable results."""
    cleaning_process = {}

    document = load_file_without_comments(filename)
    body_raw = extract_document(document)
    cleaning_process['body_length_raw'] = len(body_raw.split())
    
    my_body = delete_formula(body_raw)

    # include {} in variable, since not allowed in f-string
    environments_to_delete = ["{abstract}",\
                                "{equation}", \
                                "{eqnarray}",\
                                "{figure}",\
                                "{tabular}",\
                                "{align}",\
                                "{subequations}"]
                                
    for env in environments_to_delete:
        my_body = re.sub(rf"\\begin{env}.+?(?=\\end{env})\\end{env}",
                         "",
                         my_body)

    braced_commands_to_delete = ["date",\
                                    "label",\
                                    "eqref",\
                                    "ref",\
                                    "cite",\
                                    "fig",\
                                    "bibliography",\
                                    "title",\
                                    "subsubsection",\
                                    "subsection",\
                                    "section",\
                                    "author",\
                                    "affiliation",\
                                    "textcolor"]
    for command in braced_commands_to_delete:
        my_body = re.sub(r"\\" + command + r"{[^}]+}",
                         "",
                         my_body)

    braced_commands_with_options_to_delete = ["email"]
    for command in braced_commands_with_options_to_delete:
        my_body = re.sub(r"\\" + command + r"\[[^\]]*]{[^}]+}",
                         "",
                         my_body)

    stopwords = [r"\\centering", r"\\clearpage", r"\\itemize", r"\\item", r"\\maketitle", r"\\emph", r"\\enumerate",
                 "Eq", "Figure", "Appendix", "Section", "et al", "Fig\.", "Sec\."]
    for w in stopwords:
        my_body = re.sub(w, "", my_body)

    cleaning_process['body_length_final'] = len(my_body.split())
    
    print(f"Your raw document contains {cleaning_process['body_length_raw']} words,"
          f" {cleaning_process['body_length_raw'] - cleaning_process['body_length_final']} were deleted,"
          f" {cleaning_process['body_length_final']} remain.")

    return my_body


if __name__ == '__main__':
    my_file = r"paper2.tex"
    strip(my_file)
    
