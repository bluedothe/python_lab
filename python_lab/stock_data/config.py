#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    module description
    date: 2020/4/5
'''
__author__ = "Bigcard"
__copyright__ = "Copyright 2018-2020"

tushare_csv_home = "E:/database/csv/tushare/"
tushare_csv_day = tushare_csv_home + "day/"
tushare_csv_day_pro = tushare_csv_home + "day_pro/"
tushare_csv_day_index = tushare_csv_home + "/day_index/"

tdx_local_home = "D:/Software/Stock/jcb_hlzq/"
tdx_local_sh_day = tdx_local_home + "Vipdoc/sh/lday/"  #上海的日k线数据
tdx_local_sz_day = tdx_local_home + "Vipdoc/sz/lday/"  #深圳的日k线数据
tdx_local_sh_minline = tdx_local_home + "Vipdoc/sh/minline/"  #上海的分钟数据
tdx_local_sz_minline = tdx_local_home + "Vipdoc/sz/minline/"  #深圳的分钟数据

tdx_local_incon_file = tdx_local_home + "incon.dat"     #证监会行业，通达信新行业，申万行业等描述信息
tdx_local_block_file = tdx_local_home + "T0002/hq_cache/block.dat"             #一般板块
tdx_local_block_gn_file = tdx_local_home + "T0002/hq_cache/block_gn.dat"       #概念板块
tdx_local_block_fg_file = tdx_local_home + "T0002/hq_cache/block_fg.dat"        #风格板块
tdx_local_block_zs_file = tdx_local_home + "T0002/hq_cache/block_zs.dat"        #指数板块:
tdx_local_tdxhy_file = tdx_local_home + "T0002/hq_cache/tdxhy.cfg"              #每个股票对应通达信行业和申万行业
tdx_local_block_tdxzs_file = tdx_local_home + "T0002/hq_cache/tdxzs.cfg"              #板块指数，部分板块的最后一个字段映射到incon.dat的TDXNHY和SWHY
tdx_local_block_self_file = tdx_local_home + "T0002/blocknew/blocknew.cfg"         #自定义板块概要描述文件

tdx_csv_home = "E:/database/csv/tdx/"
tdx_csv_day = tdx_csv_home + "day/"

mysql_host = "localhost"
mysql_username = "root"
mysql_dbname = "stock"

if __name__ == '__main__':
    pass