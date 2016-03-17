import datetime
import urllib
import urlparse

from django.utils.encoding import smart_str

import jinja2
from django_jinja import library
from markdown import markdown as _markdown

from ..urlresolvers import reverse


@library.global_function
def thisyear():
    """The current year."""
    return jinja2.Markup(datetime.date.today().year)


@library.global_function
def url(viewname, *args, **kwargs):
    """Helper for our locale-aware ``reverse`` in templates."""
    return reverse(viewname, args=args, kwargs=kwargs)


@library.filter
def markdown(text, *args, **kwargs):
    """
    Parse text with markdown library.
    :param text:   - text for parsing;
    :param args:   - markdown arguments (http://pythonhosted.org/Markdown/reference.html#markdown)
    :param kwargs: - markdown keyword arguments (http://pythonhosted.org/Markdown/reference.html#markdown)
    :return:       - parsed result.
    """
    return jinja2.Markup(_markdown(text, *args, **kwargs))


@library.filter
def urlparams(url_, hash=None, **query):
    """Add a fragment and/or query paramaters to a URL.

    New query params will be appended to exising parameters, except duplicate
    names, which will be replaced.
    """
    url = urlparse.urlparse(url_)
    fragment = hash if hash is not None else url.fragment

    # Use dict(parse_qsl) so we don't get lists of values.
    q = url.query
    query_dict = dict(urlparse.parse_qsl(smart_str(q))) if q else {}
    query_dict.update((k, v) for k, v in query.items())

    query_string = _urlencode([(k, v) for k, v in query_dict.items()
                               if v is not None])
    new = urlparse.ParseResult(url.scheme, url.netloc, url.path, url.params,
                               query_string, fragment)
    return new.geturl()


def _urlencode(items):
    """A Unicode-safe URLencoder."""
    try:
        return urllib.urlencode(items)
    except UnicodeEncodeError:
        return urllib.urlencode([(k, smart_str(v)) for k, v in items])


@library.filter
def urlencode(txt):
    """Url encode a path."""
    if isinstance(txt, unicode):
        txt = txt.encode('utf-8')
    return urllib.quote_plus(txt)
