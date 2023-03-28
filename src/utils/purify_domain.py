from urllib3.util import parse_url, Url


def purify_domain(url: str) -> str:
    """Получаем голый домен без постфикса верхнего уровня и префикса www"""

    url_: Url = parse_url(url)

    if url_.hostname is None:
        raise ValueError
    
    domain = url_.hostname.split(".")

    _offset = 1 if domain[0] == "www" else 0
    pure_domain = ".".join(domain[_offset:-1])

    return pure_domain
