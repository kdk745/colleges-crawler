# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import logging


class CollegescraperPipeline:

    def open_spider(self, spider):
        # connect to or create the db as needed
        self.connection = sqlite3.connect('colleges.db')
        self.cursor = self.connection.cursor()

        # drop colleges table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS colleges')
        self.connection.commit()

        # build out the table for colleges
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS colleges (
                school_name TEXT,
                school_city TEXT,
                school_state TEXT,
                college_board_code TEXT
            )
        ''')
        self.connection.commit()
        logging.info("SQLitePipeline: Database connection opened and table created.")

    def close_spider(self, spider):
        self.connection.close()
        logging.info("SQLitePipeline: Database connection closed.")

    def process_item(self, item, spider):
        # retrieve the items from the spider script output and save to the colleges table
        self.cursor.execute('''
            INSERT INTO colleges (school_name, school_city, school_state, college_board_code) VALUES (?, ?, ?, ?)
        ''', (
            item.get('school_name'),
            item.get('school_city'),
            item.get('school_state'),
            item.get('college_board_code')
        ))
        self.connection.commit()
        logging.info(f"SQLitePipeline: Item inserted into database: {item}")
        return item
