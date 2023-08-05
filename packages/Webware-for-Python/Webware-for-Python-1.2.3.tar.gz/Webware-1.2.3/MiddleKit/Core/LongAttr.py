from BasicTypeAttr import BasicTypeAttr


class LongAttr(BasicTypeAttr):

    def __init__(self, attr):
        BasicTypeAttr.__init__(self, attr)
        if self.get('Max') is not None:
            self['Max'] = long(self['Max'])
        if self.get('Min') is not None:
            self['Min'] = long(self['Min'])
