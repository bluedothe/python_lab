#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    数据库表初始化
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe

"""
CREATE DATABASE mydb default character set utf8mb4 collate utf8mb4_general_ci;
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
create database mydb DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci
create database if not exists mydb default character set = 'utf8';
"""

create_database = "CREATE DATABASE if not exists stock DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"

drop_stock_basic = "drop table if exists stock_basic;"

create_stock_basic = """
/*==============================================================*/
/* Table: stock_basic                                           */
/*==============================================================*/
create table stock_basic
(
   id                   bigint not null auto_increment,
   code                 varchar(16) comment 'TS代码',
   symbol               varchar(16) comment '股票代码',
   name                 varchar(16) comment '股票名称',
   area                 varchar(16) comment '所在地域',
   industry             varchar(16) comment '所属行业',
   fullname             varchar(16) comment '股票全称',
   enname               varchar(16) comment '英文全称',
   market               varchar(16) comment '市场类型 （主板/中小板/创业板/科创板）',
   exchange             varchar(16) comment '交易所代码(SSE上交所 SZSE深交所 HKEX港交所(未上线))',
   curr_type            varchar(16) comment '交易货币',
   list_status          varchar(16) comment '上市状态： L上市 D退市 P暂停上市',
   list_date            varchar(16) comment '上市日期',
   delist_date          varchar(16) comment '退市日期',
   is_hs                varchar(16) comment '是否沪深港通标的，N否 H沪股通 S深股通',
   province             varchar(16) comment '所在省份',
   city                 varchar(16) comment '所在城市',
   introduction         varchar(16) comment '公司介绍',
   main_business        varchar(16) comment '主要业务及产品',
   business_scope       varchar(16) comment '经营范围',
   create_time          datetime,
   update_time          datetime,
   primary key (id)
);
"""

alter_comment_stock_basic = "alter table stock_basic comment 'from tushare';"

if __name__ == '__main__':
    mysql = mysqlHelper(bluedothe.mysql_host, bluedothe.mysql_username, bluedothe.mysql_password, bluedothe.mysql_dbname)
    mysql.exec(drop_stock_basic)
    mysql.exec(create_stock_basic)