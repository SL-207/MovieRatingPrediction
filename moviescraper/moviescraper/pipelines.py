# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name in ['budget', 'gross_na', 'gross_worldwide']:
                value = value.replace('(estimated)','')
                value = value.replace(',','')
                value.replace('¬','')
                adapter[field_name] = value.replace('$','')
                # adapter[field_name] = int(value)
        if adapter.get('gross_na') == adapter.get('gross_worldwide'):
            adapter['gross_na'] = ''