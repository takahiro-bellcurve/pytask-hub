import logging

from scrapy import logformatter


class LoggingFormatter(logformatter.LogFormatter):
    # crowl時のLogLevelをDEBUGに落とす
    def crawled(self, request, response, spider):
        return {
            'level': logging.DEBUG,
            'msg': 'Crawled %(request)s',
            'args': {
                'response': response,
                'request': request,
            }
        }

    # scraped時のLogFormatを変更する
    def scraped(self, item, response, spider):
        return {
            'level': logging.INFO,
            'msg': 'Scraped from %(response)s success',
            'args': {
                'item': item,
                'response': response,
            }
        }
