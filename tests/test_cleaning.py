from LaTeXStripper.LaTeXStripper import delete_braced_command, extract_body


def test_delete_braced_command_deletes_braced_command():
    assert (delete_braced_command('title', r'\begin{document}\n\title{Sample Title}\nSome text\n\end{document}')
            == r'\begin{document}\n\nSome text\n\end{document}')


def test_delete_braced_command_deletes_braced_command_with_option():
    assert (delete_braced_command('email', r'text-part-1\n\email[some-fabulour-option]{email-adress}\ntext-part-2')
            == r'text-part-1\n\ntext-part-2')


def test_extract_body_extracts_body():
    assert (extract_body(r'\begin{document}\n\title{Sample Title}\nSome text\n\end{document}')
            == r'\n\title{Sample Title}\nSome text\n')
