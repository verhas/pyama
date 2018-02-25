class SegmentHandler:
    def passes(self):
        '''
        :return: the numbers of passes when the handler needs to be invoked. Passes are numbered from 1 upward.
        '''
        return [ 1 ]

    def start(self):
        '''
        :return: the regular expression to be used to recognize the start of a segment handled by this segment handler
        '''
        return None

    def end(self):
        '''
        :return: the regular expression to be used to recognize the end of a segment handled by this segment handler,
        or None if there is no such regular expression
        '''
        return None

    def handle(self,pass_nr, segment):
        pass