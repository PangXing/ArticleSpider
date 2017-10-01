# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    created_at = scrapy.Field()
    front_image_url = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''INSERT INTO article SET url_object_id=%s, url=%s, title=%s, comment_cnt=%s, fav_cnt=%s,
                              praise_cnt=%s, tags=%s, front_img_url=%s,  created_date=%s, created_at=NOW(), updated_at=NOW() 
                              ON DUPLICATE KEY UPDATE `url`=VALUES(`url`), `title`=VALUES(`title`), 
                              `comment_cnt`=VALUES(`comment_cnt`),`fav_cnt`=VALUES(`fav_cnt`), `praise_cnt`=VALUES(`praise_cnt`),
                              `tags`=VALUES(`tags`), `front_img_url`=VALUES(`front_img_url`),`updated_at`=NOW() '''
        valuses = [self['url_object_id'], self['url'], self['title'], self['comment_nums'], self['fav_nums'],
                   self['praise_nums'], self['tags'], self['front_image_url'], self['created_at']]
        return insert_sql, valuses