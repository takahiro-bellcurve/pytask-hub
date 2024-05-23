import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from src.services.scrapy.custom_spider import CustomCrawlSpider


class RikunabiJobSpider(CustomCrawlSpider):
    name = "rikunabi_job"
    start_url = "https://job.rikunabi.com/2024/s/?fw=&isc=r21rcna01561&toplink=search"

    def start_requests(self):
        yield scrapy.Request(self.start_url)

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//a[@class='ts-h-search-cassetteTitleMain js-h-search-cassetteTitleMain']"), callback='parse_item'),
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='ts-h-search-upperPager']//a[text()='次の100社']"), follow=True),
    )

    def parse_item(self, response):
        rikunabi_company_url = response.url

        company_name = response.xpath(
            "//h1/a/text()"
        ).get()

        target_industry = response.xpath(
            "//table[@class='ts-h-company-dataTable']//th[text()='業種']/following-sibling::td/div[@class='ts-h-company-dataTable-main']/text()"
        ).get()

        # 本社
        head_office = response.xpath(
            "//table[@class='ts-h-company-dataTable']//th[text()='本社']/following-sibling::td/div[@class='ts-h-company-dataTable-main']/text()"
        ).get()

        # 残り採用予定人数
        remaining_recruitment = response.xpath(
            "//table[@class='ts-h-company-dataTable']//th[text()='残り採用予定数']/following-sibling::td/div[@class='ts-h-company-dataTable-main']/text()"
        ).get()
        remaining_recruitment = re.sub(
            r"\s", "", remaining_recruitment) if remaining_recruitment is not None else None

        # 従業員数
        number_of_employees = response.xpath(
            "//th[text()='従業員数']/following-sibling::td/text()"
        ).get()
        number_of_employees = re.sub(
            r"\s", "", number_of_employees) if number_of_employees is not None else None

        phone_number_regex = [
            r"\d{4}-\d{3}-\d{3}",
            r"\d{3}-\d{3}-\d{4}",
            r"\d{3}-\d{2}-\d{4}",
            r"\d{2}-\d{4}-\d{4}",
        ]
        email_regex = r"[\w\.-]+@[\w\.-]+"

        company_info = response.xpath(
            "//h2[@class='ts-h-company-heading ts-s-mb28']/following-sibling::div/text()"
        ).getall()

        phone_number = ""
        email = ""
        for info in company_info:
            for phone_number_pattern in phone_number_regex:
                if re.search(phone_number_pattern, info):
                    phone_number = re.search(
                        phone_number_pattern, info).group()

            if re.search(email_regex, info):
                email = re.search(email_regex, info).group()

        recruit_info_link = response.xpath(
            "//div[@class='ts-h-company-upperArea-optionTabArea']//a[text()='採用情報']/@href"
        ).get()

        if recruit_info_link is not None:
            yield response.follow(recruit_info_link, self.parse_recruit_info, cb_kwargs=dict(
                rikunabi_company_url=rikunabi_company_url,
                company_name=company_name,
                target_industry=target_industry,
                head_office=head_office,
                remaining_recruitment=remaining_recruitment,
                number_of_employees=number_of_employees,
                phone_number=phone_number,
                email=email,
            ))
        else:
            yield {
                "リクナビ会社ページリンク": rikunabi_company_url,
                "会社名": company_name,
                "業種": target_industry,
                "本社": head_office,
                "残り採用予定人数": remaining_recruitment,
                "従業員数": number_of_employees,
                "電話番号": phone_number,
                "email": email,
                "採用予定人数": "",
                "プレエントリー登録人数": "",
            }

    def parse_recruit_info(self, response, **kwargs):
        # 採用予定人数
        number_of_hires = response.xpath(
            "//h3[text()='採用人数（今年度予定）']/following-sibling::table//td/text()"
        ).get()

        # プレエントリー登録人数
        pre_entry = response.xpath(
            "//th[text()='プレエントリー候補リスト登録人数']/following-sibling::td/text()"
        ).get()
        pre_entry = re.sub(
            r"\s", "", pre_entry) if pre_entry is not None else None
        pre_entry = re.sub(
            r"名", "", pre_entry) if pre_entry is not None else None

        yield {
            "リクナビ会社ページリンク": kwargs["rikunabi_company_url"],
            "会社名": kwargs["company_name"],
            "業種": kwargs["target_industry"],
            "本社": kwargs["head_office"],
            "残り採用予定人数": kwargs["remaining_recruitment"],
            "従業員数": kwargs["number_of_employees"],
            "電話番号": kwargs["phone_number"],
            "email": kwargs["email"],
            "採用予定人数": number_of_hires,
            "プレエントリー登録人数": pre_entry,
        }
