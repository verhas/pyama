class Configuration:
    def __init__(self):
        self.filename_patterns = []
        self.filename_regexes = []
        self.regexes = []
        self.segmenthandlers = {}
        self.max_passes = 0
        self.handlers = []
    def file(self,regex):
        self.filename_regexes.append(regex)
        return self

    def handler(self,*handlers):
        for handler in handlers:
            self.regexes.append(( handler.start(), handler.end()))
            self.max_passes = max( self.max_passes, max(handler.passes()))
        for handler in handlers:
            self.handlers.append(handler)
        return self