# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum


class SaveImage(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            filename = request._url.rsplit("/", 1)[1]
            path = '%s' % (filename)
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height})
        return checksum
