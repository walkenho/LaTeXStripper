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

def get_body(my_text):
    """Extracts the body of a LaTeX document, i.e. everything between \\begin{document} and \\end{document}."""
    matcher_body = r"\\begin{document}([.\S\s]*)\\end{document}"
    body = re.findall(matcher_body, my_text)
    return body[0]

def delete_pattern(pattern, my_text):
    """Deletes all occurences of pattern in my_text. Gives back cleaned text."""
    return re.sub(pattern, "", my_text)

def delete_comment(my_line):
    """Deletes all the comments in a text, i.e. everything following % till the end of the line. \
       Wrapper around delete_pattern."""
    matcher_comment = r"(%.*)"
    clean_line = delete_pattern(matcher_comment, my_line)
    return clean_line

def delete_formula(my_text):
    """Deletes all formulas in a text, i.e. everything of the form $...$. \
       Wrapper around delete_pattern."""
    matcher_formula = r"(\$[^\$]+\$)"
    my_text = delete_pattern(matcher_formula, my_text)
    return my_text

def get_string_from_file(myfile):
    f = open(myfile, 'r')
    raw_text = []    
    for line in f:
        clean_line = delete_comment(line.rstrip())
        raw_text.append(clean_line)
    my_text = ' '.join(raw_text)   
    return my_text
    

def strip(my_file):
    """ A small tool to get rid of LaTeX code in .tex files 
        to be able to run them through a bag-of-words algorithm 
        (like e.g. WordCloud) and get reasonable results."""
    body_length = []

    my_text = get_string_from_file(my_file)
    my_body = get_body(my_text)
    body_length.append(len(my_body))
    
    my_body = delete_formula(my_body)
    body_length.append(len(my_body))

    environments_to_delete = ["abstract",\
                                "equation", \
                                "eqnarray",\
                                "figure",\
                                "tabular",\
                                "align",\
                                "subequations"]
                                
    for env in environments_to_delete:
        matcher = r"\\begin{"+env+r"}.+?(?=\\end{"+env+r"})\\end{"+env+r"}"    
        my_body = delete_pattern(matcher, my_body)
    body_length.append(len(my_body))
        
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
        matcher = r"\\" + command + r"{[^}]+}"
        my_body = delete_pattern(matcher, my_body)
    body_length.append(len(my_body))

    braced_commands_with_options_to_delete = ["email"]
    for command in braced_commands_with_options_to_delete:
        matcher = r"\\" + command + r"\[[^\]]*]{[^}]+}"
        my_body = delete_pattern(matcher, my_body)
    body_length.append(len(my_body))
    
    unbraced_commands_to_delete = ["centering", "clearpage", "itemize", "item", "maketitle", "emph", "enumerate"] 
    for command in unbraced_commands_to_delete:
        matcher = r"\\" + command
        my_body = delete_pattern(matcher, my_body)
    body_length.append(len(my_body))
          
    words_to_delete = ["Eq", "Figure", "Appendix", "Section", "et al", "Fig\.", "Sec\."]
    for word in words_to_delete:
        matcher = word
        my_body = delete_pattern(matcher, my_body)
    body_length.append(len(my_body))
    
    print(my_body)
    print(body_length)
    return my_body

if __name__ == '__main__':
    my_file = r"paper2.tex"
    strip(my_file)
    
