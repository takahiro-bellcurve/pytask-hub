from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)

process.crawl("rikunabi_job")
process.start()
