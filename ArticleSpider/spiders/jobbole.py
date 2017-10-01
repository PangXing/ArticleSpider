# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urlparse import urljoin
import re
from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        # 详情页面的爬取
        detail_selectors = response.css('#archive .post-thumb a')
        for i in detail_selectors:
            detail_img = i.css('img::attr(src)').extract_first('')
            detail_img = urljoin(response.url, detail_img)
            detail_url = i.css('::attr(href)').extract_first('')
            if detail_url:
                yield Request(url=urljoin(response.url, detail_url), meta={'front_img_url': detail_img},
                              callback=self.parse_detail)

        # 下一页的爬取
        next_url = response.css('.next.page-numbers').css('::attr("href")').extract_first('')
        if next_url:
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = ArticlespiderItem()

        # 使用Xpath提取
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first().strip()
        # created_at = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().encode(
        #     'utf-8').replace('·', "").strip()
        # raise_num = int(response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first())
        # mark_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()
        # tmp_re = re.match('.*?(\d+).*', mark_num)
        # if tmp_re:
        #     mark_num = int(tmp_re.group(1))
        # else:
        #     mark_num = 0
        # comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        # tmp_re = re.match('.*?(\d+).*', comment_num)
        # if tmp_re:
        #     comment_num = int(tmp_re.group(1))
        # else:
        #     comment_num = 0
        # centent = response.xpath('//div[@class="entry"]').extract_first()

        # css 方式提取
        title = response.css('.entry-header h1::text').extract_first().strip()
        created_at = response.css('.entry-meta-hide-on-mobile::text').extract_first().strip().encode(
            'utf-8').replace('·', "").strip()
        raise_num = int(response.css('span.vote-post-up h10::text').extract_first())
        mark_num = response.css('span.bookmark-btn::text').extract_first()
        tmp_re = re.match('.*?(\d+).*', mark_num)
        if tmp_re:
            mark_num = int(tmp_re.group(1))
        else:
            mark_num = 0
        comment_num = response.css('a[href="#article-comment"] span::text').extract_first()
        tmp_re = re.match('.*?(\d+).*', comment_num)
        if tmp_re:
            comment_num = int(tmp_re.group(1))
        else:
            comment_num = 0
        centent = response.css('div.entry').extract_first()

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u"评论")]
        tags = ",".join(tag_list)

        article_item['url_object_id'] = get_md5(response.url)
        article_item['url'] = response.url
        article_item['title'] = title
        try:
            created_at = datetime.datetime.strptime(created_at, '%Y/%m/%d').date()
        except Exception as e:
            created_at = datetime.datetime.now().date()
        article_item['created_at'] = str(created_at)
        article_item['front_image_url'] = [response.meta.get("front_img_url", "")]  # 文章封面图
        article_item['praise_nums'] = raise_num
        article_item['comment_nums'] = comment_num
        article_item['fav_nums'] = mark_num
        article_item['tags'] = tags
        # article_item['content'] = centent

        yield article_item
