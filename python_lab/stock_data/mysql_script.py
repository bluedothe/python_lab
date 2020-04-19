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
from stock_data import config

mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password, config.mysql_dbname)

"""
CREATE DATABASE mydb default character set utf8mb4 collate utf8mb4_general_ci;
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
create database mydb DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci
create database if not exists mydb default character set = 'utf8';
"""

create_database_common = "CREATE DATABASE if not exists {} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"

drop_table_common = "drop table if exists {};"

create_stock_basic = """
/*==============================================================*/
/* Table: stock_basic                                           */
/*==============================================================*/
create table stock_basic
(
   ts_code              varchar(16) comment 'TS代码',
   symbol               varchar(16) comment '股票代码',
   name                 varchar(16) comment '股票名称',
   area                 varchar(16) comment '所在地域',
   industry             varchar(16) comment '所属行业',
   fullname             varchar(64) comment '股票全称',
   enname               varchar(128) comment '英文全称',
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
   primary key (ts_code)
);
"""

alter_comment_stock_basic = "alter table stock_basic comment 'from tushare';"

insert_exam = "INSERT INTO stock_basic(code,symbol,fullname,enname,create_time) VALUES('000001.SZ', '000001', '平安银行',NULL,'2020-2-27 23:32:32'),('000002.SZ', '000002', '平安银行2',NULL,'2020-2-27 23:32:32'),"

create_collect_log = """
/*==============================================================*/
/* Table: collect_log                                           */
/*==============================================================*/
create table collect_log
(
   id                   bigint not null auto_increment,
   data_type            varchar(64) comment '采集的数据类型:tushare_history_all',
   data_name            varchar(64) comment '采集的数据名称',
   data_source          varchar(64) comment '数据来源，tushare,tdx,ths',
   data_end_date        date comment '已采集数据最后日期',
   collect_start_time   datetime comment '采集数据开始时间',
   collect_end_time     datetime comment '采集数据结束时间',
   collect_log          varchar(128) comment '数据采集日志',
   collect_status       varchar(16) comment 'R采集中，S采集成功，E发生异常',
   primary key (id)
);
"""

insert_collect_log = "INSERT INTO collect_log(data_type,data_name,data_source,collect_start_time,collect_status) VALUES('{data_type}','{data_name}','{data_source}','{collect_start_time}','{collect_status}')"
update_collect_log = "UPDATE collect_log SET data_end_date = '{data_end_date}', collect_end_time = '{collect_end_time}', collect_log = '{collect_log}', collect_status = '{collect_status}' WHERE id = {id}"


def record_log(paras, is_insert=True):
    # paras = {"data_type":"tushare_history_all","data_name":"tushare交易数据，两个接口合并","data_source":"tusharepro+tushare","collect_start_time":"","collect_status":"R"}
    # paras = {"data_end_date":"","collect_end_time":"","collect_log":"sucess", "collect_status":"S","id":1}
    if is_insert:
        id = mysql.insert_one(insert_collect_log.format(**paras))
        return id
    else:
        mysql.exec(update_collect_log.format(**paras))

if __name__ == '__main__':
    #mysql.exec(drop_stock_basic)
    #mysql.exec(create_stock_basic)
    #mysql.exec(insert_exam[0:-1])
    #mysql.exec(drop_table_common.format('collect_log'))
    mysql.exec(create_collect_log)