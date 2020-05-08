#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/3/28
    数据库表初始化
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

import pandas as pd
from db.mysqlHelper import mysqlHelper
from stock_data import bluedothe
from stock_data import config
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer, DateTime, BigInteger

mysql = mysqlHelper(config.mysql_host, config.mysql_username, bluedothe.mysql_password, config.mysql_dbname)
# pandas的mysql对象
engine = create_engine(f'mysql+pymysql://{config.mysql_username}:{bluedothe.mysql_password}@{config.mysql_host}/{config.mysql_dbname}?charset=utf8')

"""
CREATE DATABASE mydb default character set utf8mb4 collate utf8mb4_general_ci;
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
create database mydb DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci
create database if not exists mydb default character set = 'utf8';
"""

create_database_common = "CREATE DATABASE if not exists {} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"

drop_table_common = "drop table if exists {};"   #删除表
truncate_table_common = "truncate table {};"    #清空表数据
delete_table_common = "delete from {};"    #清空表数据

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

insert_collect_log_before = "INSERT INTO collect_log(data_type,data_name,data_source,collect_start_time,collect_status) VALUES('{data_type}','{data_name}','{data_source}','{collect_start_time}','{collect_status}')"
update_collect_log_after = "UPDATE collect_log SET data_end_date = '{data_end_date}', collect_end_time = '{collect_end_time}', collect_log = '{collect_log}', collect_status = '{collect_status}' WHERE id = {id}"
insert_collect_log = "INSERT INTO collect_log(data_type,data_name,data_source,data_end_date,collect_start_time,collect_end_time,collect_log,collect_status) VALUES('{data_type}','{data_name}','{data_source}','{data_end_date}','{collect_start_time}','{collect_end_time}','{collect_log}','{collect_status}')"

create_index_basic = """
/*==============================================================*/
/* Table: index_basic                                           */
/*==============================================================*/
create table index_basic
(
   code                 varchar(16) comment '指数代码',
   ts_code              varchar(16) not null comment '加市场标志的指数代码',
   name                 varchar(16) comment '指数名称',
   market               varchar(16) comment '市场类型 SH沪市，SZ深市',
   primary key (ts_code)
);

"""

insert_index_basic = "INSERT INTO index_basic(code, ts_code, name, market) VALUES('{code}', '{ts_code}', '{name}', '{market}')"

create_block_member = """
/*==============================================================*/
/* Table: block_member                                          */
/*==============================================================*/
create table block_member
(
   data_source          varchar(16) not null,
   block_category       varchar(16) not null,
   block_type           varchar(16) not null comment '板块类型：1普通板块；2风格板块；3概念板块；4指数板块',
   block_name           varchar(16) not null comment '板块名称',
   block_code           varchar(16) not null,
   ts_code              varchar(16) not null,
   create_time          datetime,
   primary key (data_source, block_name, block_type, block_category, block_code, ts_code)
);

"""

create_block_basic = """
/*==============================================================*/
/* Table: block_basic                                            */
/*==============================================================*/
create table block_basic
(
   data_source          varchar(16) not null comment '板块分类来源',
   block_category       varchar(16) not null comment '板块种类',
   block_type           varchar(16) not null comment '板块分类',
   block_name           varchar(64) not null comment '板块名称',
   block_code           varchar(16) not null comment '板块代码',
   member_count         int comment '成分股数量',
   gn_date              date comment '概念提出时间',
   gn_event             varchar(256) comment '概念事件驱动',
   create_time          datetime,
   primary key (data_source, block_category, block_type, block_name, block_code)
);

"""

def record_log(paras, flag = 'all'):
    # paras = {"data_type":"tushare_history_all","data_name":"tushare交易数据，两个接口合并","data_source":"tusharepro+tushare","collect_start_time":"","collect_status":"R"}
    # paras = {"data_end_date":"","collect_end_time":"","collect_log":"sucess", "collect_status":"S","id":1}
    if flag == 'before':
        id = mysql.insert_one(insert_collect_log_before.format(**paras))
        return id
    elif flag == 'after':
        mysql.exec(update_collect_log_after.format(**paras))
    else:
        id = mysql.insert_one(insert_collect_log.format(**paras))
        return id

#更新block_basic和block_member两张表的数据
def df2db_update(data_source, block_basic_df, block_member_df):
    dtypedict = {
        'data_source': NVARCHAR(length=16), 'block_category': NVARCHAR(length=16), 'block_type': NVARCHAR(length=16),
        'block_name': NVARCHAR(length=16), 'block_code': NVARCHAR(length=16), 'ts_code': NVARCHAR(length=16),
        'member_count': Integer, 'create_time': DateTime
    }
    mysql.exec(delete_table_common.format(f"block_member where data_source = '{data_source}'"))  # 删除表中记录
    # 该函数调用前，需要先将block_member表中的tdx相关的数据删掉
    pd.io.sql.to_sql(block_member_df, 'block_member', con=engine, if_exists='append', index=False,
                     index_label="data_source, block_category, block_type, block_name, block_code, ts_code",
                     dtype=dtypedict, chunksize=10000)  # chunksize参数针对大批量插入，pandas会自动将数据拆分成chunksize大小的数据块进行批量插入;

    mysql.exec(delete_table_common.format(f"block_basic where data_source = '{data_source}'"))  # 删除表中记录
    pd.io.sql.to_sql(block_basic_df, 'block_basic', con=engine, if_exists='append', index=False,
                     index_label="data_source, block_category, block_type, block_name, block_code",
                     dtype=dtypedict, chunksize=10000)

if __name__ == '__main__':
    #mysql.exec(drop_stock_basic) #删除表
    mysql.exec(create_block_basic) #建表
    #mysql.exec(insert_exam[0:-1])
    #mysql.exec(drop_table_common.format('collect_log'))  #删除表
    #mysql.exec(delete_table_common.format("block_member where data_source = 'tdx'"))  #删除表中记录
    pass