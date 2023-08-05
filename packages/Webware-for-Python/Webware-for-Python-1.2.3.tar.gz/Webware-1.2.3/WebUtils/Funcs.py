"""WebUtils.Funcs

This module provides some basic functions that are useful
in HTML and web development.

You can safely import * from WebUtils.Funcs if you like.
"""

__all__ = [
    'htmlEncode', 'htmlEncodeStr', 'htmlDecode', 'urlEncode', 'urlDecode',
    'htmlForDict', 'requestURI', 'normURL']


htmlForNone = '-'  # used by htmlEncode

htmlCodes = (
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    # ['\n', '<br>'],
)

htmlCodesReversed = tuple(reversed(htmlCodes))


def htmlEncode(what, codes=htmlCodes):
    """Return the HTML encoded version of the given object.

    The optional 'codes' parameter allows passing custom translations.
    """
    if what is None:
        return htmlForNone
    if hasattr(what, 'html'):
        # allow objects to specify their own translation to html
        # via a method, property or attribute
        ht = what.html
        if callable(ht):
            ht = ht()
        return ht
    what = str(what)
    return htmlEncodeStr(what, codes)


def htmlEncodeStr(s, codes=htmlCodes):
    """Return the HTML encoded version of the given string.

    This is useful to display a plain ASCII text string on a web page.

    The optional 'codes' parameter allows passing custom translations.
    """
    for c, e in codes:
        s = s.replace(c, e)
    return s


def htmlDecode(s, codes=htmlCodesReversed):
    """Return the ASCII decoded version of the given HTML string.

    This does NOT remove normal HTML tags like <p>.
    It is the inverse of htmlEncode().

    The optional 'codes' parameter allows passing custom translations.
    """
    for c, e in codes:
        s = s.replace(e, c)
    return s


# Aliases for URL encoding and decoding functions:
from urllib import quote_plus as urlEncode, unquote_plus as urlDecode


def htmlForDict(d, addSpace=None, filterValueCallBack=None,
        maxValueLength=None, topHeading=None, isEncoded=None):
    """Return an HTML string with a table where each row is a key-value pair."""
    if not d:
        return ''
    # A really great (er, bad) example of hardcoding.  :-)
    html = ['<table class="NiceTable">\n']
    if topHeading:
        html.append('<tr class="TopHeading"><th')
        html.append(('>%s</th><th>%s' if isinstance(topHeading, tuple)
            else ' colspan="2">%s') % topHeading)
        html.append('</th></tr>\n')
    for key in sorted(d):
        value = d[key]
        if addSpace and key in addSpace:
            target = addSpace[key]
            value = (target + ' ').join(value.split(target))
        if filterValueCallBack:
            value = filterValueCallBack(value, key, d)
        if maxValueLength and not isEncoded:
            value = str(value)
            if len(value) > maxValueLength:
                value = value[:maxValueLength-3] + '...'
        key = htmlEncode(key)
        if not isEncoded:
            value = htmlEncode(value)
        html.append('<tr><th style="text-align:left">%s</th><td>%s</td></tr>\n'
            % (key, value))
    html.append('</table>')
    return ''.join(html)


def requestURI(env):
    """Return the request URI for a given CGI-style dictionary.

    Uses REQUEST_URI if available, otherwise constructs and returns it
    from SCRIPT_URL, SCRIPT_NAME, PATH_INFO and QUERY_STRING.
    """
    uri = env.get('REQUEST_URI')
    if uri is None:
        uri = env.get('SCRIPT_URL')
        if uri is None:
            uri = env.get('SCRIPT_NAME', '') + env.get('PATH_INFO', '')
        query = env.get('QUERY_STRING', '')
        if query != '':
            uri += '?' + query
    return uri


def normURL(path):
    """Normalizes a URL path, like os.path.normpath.

    Acts on a URL independent of operating system environment.
    """
    if not path:
        return
    initialslash = path[0] == '/'
    lastslash = path[-1] == '/'
    comps = path.split('/')
    newcomps = []
    for comp in comps:
        if comp in ('', '.'):
            continue
        if comp != '..':
            newcomps.append(comp)
        elif newcomps:
            newcomps.pop()
    path = '/'.join(newcomps)
    if path and lastslash:
        path += '/'
    if initialslash:
        path = '/' + path
    return path
