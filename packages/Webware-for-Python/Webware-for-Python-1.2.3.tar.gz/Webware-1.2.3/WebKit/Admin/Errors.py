from os import sep

from WebUtils.Funcs import urlEncode

from DumpCSV import DumpCSV

class Errors(DumpCSV):

    def filename(self):
        return self.application().setting('ErrorLogFilename')

    def cellContents(self, rowIndex, colIndex, value):
        """Hook for subclasses to customize the contents of a cell.

        Based on any criteria (including location).
        """
        if self._headings[colIndex] in ('pathname', 'error report filename'):
            path = self.application().serverSidePath()
            if value.startswith(path):
                value = value[len(path):]
                if value.startswith(sep):
                    value = value[len(sep):]
                link = 'View?filename=%s' % urlEncode(value)
                value = value.replace(sep, sep + '<wbr>')
                value = '<a href="%s">%s</a>' % (link, value)
            else:
                value = value.replace(sep, sep + '<wbr>')
            return value
        elif self._headings[colIndex] == 'time':
            return '<span style="white-space:nowrap">%s</span>' % (value)
        else:
            return self.htmlEncode(value)
