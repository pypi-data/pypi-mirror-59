import os
from glob import glob
from WebKit.Examples.ExamplePage import ExamplePage


class PSPExamplePage(ExamplePage):

    def cornerTitle(self):
        return "PSP Examples"

    def scripts(self):
        """Get list of PSP scripts.

        Creates a list of dictionaries, where each dictionary stores
        information about a particular script.
        """
        examples = []
        filesyspath = self.request().serverSidePath()
        files = glob(os.path.join(os.path.dirname(filesyspath), "*.psp"))
        for i in files:
            file = os.path.split(i)[1]
            script = {}
            script['pathname'] = script['name'] = file
            examples.append(script)
        return examples

    def writeOtherMenu(self):
        self.menuHeading('Other')
        viewPath = self.request().uriWebKitRoot() + "PSP/Examples/View"
        self.menuItem(
            'View source of<br/>%s' % self.title(),
            self.request().uriWebKitRoot() + 'PSP/Examples/View?filename=%s'
                % os.path.basename(self.request().serverSidePath()))
        if self.application().hasContext('Documentation'):
            filename = 'Documentation/WebKit.html'
            if os.path.exists(filename):
                self.menuItem('Local WebKit docs',
                    self.request().servletPath() + '/' + filename)
