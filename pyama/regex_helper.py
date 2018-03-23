import logging
import re

logger = logging.getLogger(__name__)

reported = []


def re_search(regex, string):
    try:
        return re.search(regex, string)
    except Exception as e:
        msg = str(e)
        if msg not in reported:
            logger.error("Error using the regular expression >>%s<<" % regex)
            logger.error("exception: >>%s<<" % e)
            reported.append(msg)
        return None


def re_sub(regex, replace, string):
    try:
        return re.sub(regex, replace, string)
    except Exception as e:
        msg = str(e)
        if msg not in reported:
            logger.error("Error using the regular expression >>%s<<" % regex)
            logger.error("                replacement string >>%s<<" % replace)
            logger.error("exception: >>%s<<" % e)
            reported.append(msg)
        return None
