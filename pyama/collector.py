import glob
import re
from pyama.regex_helper import re_search


class FileCollector:
    def __init__(self, configurations, *patterns):
        """
        Collect the file names parse recursively into subdirectories
        and selecting the files that match any of the patterns
        :param configurations: the configurations
        :param patterns: array of patterns to match the file names
        """
        self.configurations = configurations
        self.patterns = patterns

    def collect(self):
        files = set()
        for pattern in self.patterns:
            for file in glob.glob(pattern, recursive=True):
                for configuration in self.configurations:
                    if any([re_search(regex, file) for regex in configuration.filename_regexes]) and not any(
                            [re_search(regex, file) for regex in configuration.filename_excludes]):
                        files.add(file)

        return files
