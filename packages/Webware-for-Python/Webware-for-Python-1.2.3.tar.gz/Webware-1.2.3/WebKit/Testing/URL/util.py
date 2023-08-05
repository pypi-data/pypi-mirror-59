from WebKit.Page import Page
from WebUtils.Funcs import htmlEncode


class Inspector(Page):

    def writeContent(self):
        req = self.request()
        self.write('Path:<br>\n')
        self.write('<code>%s</code><p>\n'
            % htmlEncode(req.extraURLPath()))
        self.write('Variables:<br>\n')
        self.write('<table>')
        for name in sorted(req.fields()):
            self.write(
                '<tr><td style="text-align:right">%s:</td><td>%s</td></tr>\n'
                % (htmlEncode(name), htmlEncode(req.field(name))))
        self.write('</table><p>\n')
        self.write('Server-side path:<br>\n')
        self.write('<code>%s</code><p>\n' % req.serverSidePath())
