#!/usr/bin/env python
# -*- coding: utf-8 mode: python -*-
#
# LaTeXStripper.py - A tool to get rid of LaTeX code in .tex files
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import re


# autofunction:: strip()


def extract_body(text):
    """Extract the body of a LaTeX document,
    i.e. everything between \\begin{document} and \\end{document}."""
    matcher_body = r"\\begin{document}([.\S\s]*)\\end{document}"
    return re.findall(matcher_body, text)[0]


def delete_pattern(pattern, text):
    """Delete all occurences of pattern in my_text. Gives back cleaned text."""
    return re.sub(pattern, "", text)


def delete_comment(text):
    """Delete LaTeX comment from the end of a string."""
    return delete_pattern(r"(%.*)", text)


def delete_formulas(text):
    """Delete all formulas in a text, i.e. everything of the form $...$."""
    return delete_pattern(r"(\$[^\$]+\$)", text)


def load_uncommented_text_from_file(filepath):
    with open(filepath, "r") as f:
        raw_text = []
        # Stripping out comments requires stripping out the comments from the end of the lines
        for line in f:
            raw_text.append(delete_comment(line.rstrip()))
    return " ".join(raw_text)


def delete_braced_command(command, text):
    # matches \command{whatever}
    # example: \label{my-fabulous-label}
    # also matches with option
    # example: \email[sth-sth]{my-fabulous-email}
    # second part of regex matches braces and everything in between (which is not a brace)
    return delete_pattern(rf"\\{command}" + r"(\[[^\]]*]){0,1}{[^}]+}", text)


def delete_braced_commands(commands, text):
    for command in commands:
        text = delete_braced_command(command, text)
    return text


def delete_unbraced_command(command, text):
    return delete_pattern(rf"\\{command} ", text)


def delete_unbraced_commands(commands, text):
    for command in commands:
        text = delete_unbraced_command(command, text)
    return text


def delete_environment(environment, text):
    return delete_pattern(
        r"\\begin{"
        + environment
        + r"}.+?(?=\\end{"
        + environment
        + r"})\\end{"
        + environment
        + r"}",
        text,
    )


def delete_environments(environments, text):
    for environment in environments:
        text = delete_environment(environment, text)
    return text


def strip(filename):
    """A tool to delete LaTeX formatting from a .tex file"""
    body_length = []

    body = extract_body(load_uncommented_text_from_file(filename))
    body_length.append(len(body))

    body = delete_formulas(body)
    body_length.append(len(body))

    body = delete_environments(
        [
            "abstract",
            "equation",
            "eqnarray",
            "figure",
            "tabular",
            "align",
            "subequations",
        ],
        body,
    )
    body_length.append(len(body))

    body = delete_braced_commands(
        [
            "date",
            "label",
            "eqref",
            "ref",
            "cite",
            "fig",
            "bibliography",
            "title",
            "subsubsection",
            "subsection",
            "section",
            "author",
            "affiliation",
            "textcolor",
            "email",
        ],
        body,
    )
    body_length.append(len(body))

    body = delete_unbraced_commands(
        ["centering", "clearpage", "itemize", "item", "maketitle", "emph", "enumerate"],
        body,
    )
    body_length.append(len(body))

    for word in ["Eq", "Figure", "Appendix", "Section", "et al", "Fig\.", "Sec\."]:
        body = delete_pattern(word, body)
    body_length.append(len(body))

    print(
        f"Your text originally contained {body_length[0]} words, "
        f"{body_length[0] - body_length[len(body_length) - 1]} of which were stripped off."
    )
    return body.strip()


if __name__ == "__main__":
    my_file = r"paper2.tex"
    strip(my_file)
