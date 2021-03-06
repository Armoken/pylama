import sys

from pylama.config import parse_options
from pylama.core import run
from pylama.lint.extensions import LINTERS


def test_mccabe():
    mccabe = LINTERS.get('mccabe')
    errors = mccabe.run('dummy.py', '', params={})
    assert errors == []


def test_eradicate():
    eradicate = LINTERS.get('eradicate')
    errors = eradicate.run('', code="\n".join([
        "#import os",
        "# from foo import junk",
        "#a = 3",
        "a = 4",
        "#foo(1, 2, 3)",
    ]))
    assert len(errors) == 4


def test_pyflakes():
    options = parse_options(linters=['pyflakes'], config=False)
    assert options.linters
    errors = run('dummy.py', code="\n".join([
        "import sys",
        "def test():",
        "    unused = 1"
    ]), options=options)
    assert len(errors) == 2


def test_pycodestyle():
    options = parse_options(linters=['pycodestyle'], config=False)
    assert len(options.linters) == 1
    errors = run('dummy.py', options=options)
    numbers = [error.number for error in errors]
    assert len(errors) == 4
    assert 'E265' in numbers
    assert 'E301' in numbers
    assert 'E501' in numbers

    options.linters_params['pycodestyle'] = dict(max_line_length=60)
    errors = run('dummy.py', options=options)
    assert len(errors) == 13


def test_pydocstyle():
    options = parse_options(linters=['pydocstyle'])
    assert len(options.linters) == 1
    errors = run('dummy.py', options=options)
    assert errors


def test_mypy():
    if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
        options = parse_options(linters=['mypy'])
        assert len(options.linters) == 1
        errors = run('dummy.py', options=options)
        assert len(errors) == 1


def test_vulture():
    options = parse_options(linters=['vulture'])
    assert len(options.linters) == 1
    errors = run('dummy.py', options=options)

    assert len(errors) == 15
    assert errors[0]["number"] == "V106"
    assert errors[1]["number"] == "V101"
    assert errors[2]["number"] == "V102"
    assert errors[3]["number"] == "V102"
    assert errors[4]["number"] == "V102"
    assert errors[5]["number"] == "V102"
    assert errors[6]["number"] == "V102"
    assert errors[7]["number"] == "V102"
    assert errors[8]["number"] == "V102"
    assert errors[9]["number"] == "V102"
    assert errors[10]["number"] == "V102"
    assert errors[11]["number"] == "V102"
    assert errors[12]["number"] == "V102"
    assert errors[13]["number"] == "V102"
    assert errors[14]["number"] == "V103"
