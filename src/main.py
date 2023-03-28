from devtools import debug

from .parsers import ParsersFactory
from .utils import purify_domain


def main():
    url = "https://russian.rt.com/russia/article/1124103-sevmash-podvodnye-lodki-yasen-borei"
    pure_domain = purify_domain(url)

    d = ParsersFactory().get(pure_domain).parse(url)
    debug(d)
