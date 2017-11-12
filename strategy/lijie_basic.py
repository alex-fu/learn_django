# coding=utf-8

import pandas as pd
from dw.dw_api import parse_finance_file


def _get_row_numeric(df, row_name):
    return pd.to_numeric(df.ix[row_name], errors="coerce").fillna(0.0)


def gross_profit_rate(stock_code, date_list):
    """
    1. 毛利率
       读取数据
           来自： 盈利能力
           取值： 销售毛利率(%)
       计算数据
           来自： 利润表
           取值： 营业收入(万元)[??主要财务指标:主营业务收入(万元)], 营业成本(万元)
           算法：
                 毛利率 = (营业收入(万元) - 营业成本(万元)) / 营业收入(万元)
    """
    lrb_df = parse_finance_file(stock_code, "lrb", "report")

    income = _get_row_numeric(lrb_df[date_list], u"营业收入(万元)")
    cost = _get_row_numeric(lrb_df[date_list], u"营业成本(万元)")

    ret_df = lrb_df[date_list].copy(deep=True)
    ret_df.ix[u"毛利率"] = (income - cost) / income * 100.0

    return ret_df.ix[[u"毛利率"]]


def expense_rate(stock_code, date_list):
    """
    2. 三项费用率(销售费用率 管理费用率 财务费用率)
       读取数据
           来自： 盈利能力
           取值： 三项费用比重(%) [仅有一项，数据不全]
       计算数据
           来自： 利润表
           取值： 营业收入(万元)，销售费用(万元)，管理费用(万元)，财务费用(万元)
           算法：
                 销售费用率 = 销售费用(万元) / 营业收入(万元)
                 管理费用率 = 管理费用(万元) / 营业收入(万元)
                 财务费用率 = 财务费用(万元) / 营业收入(万元)
                 三项费用率 = (销售费用(万元) + 管理费用(万元) + 财务费用(万元)) / 营业收入(万元)
    """
    lrb_df = parse_finance_file(stock_code, "lrb", "report")

    income = _get_row_numeric(lrb_df[date_list], u"营业收入(万元)")
    sale_expense = _get_row_numeric(lrb_df[date_list], u"销售费用(万元)")
    manage_expense = _get_row_numeric(lrb_df[date_list], u"管理费用(万元)")
    finance_expense = _get_row_numeric(lrb_df[date_list], u"财务费用(万元)")

    ret_df = lrb_df[date_list].copy(deep=True)
    ret_df.ix[u"销售费用率"] = sale_expense / income * 100.0
    ret_df.ix[u"管理费用率"] = manage_expense / income * 100.0
    ret_df.ix[u"财务费用率"] = finance_expense / income * 100.0
    ret_df.ix[u"三项费用率"] = (sale_expense + manage_expense + finance_expense) / income * 100.0

    return ret_df.ix[[u"销售费用率", u"管理费用率", u"财务费用率", u"三项费用率"]]


def net_profit_rate(stock_code, date_list):
    """
    3. 净利润率
       读取数据
           来自： 盈利能力
           取值： 销售净利率(%)
       计算数据
           来自： 主要财务指标, 利润表
           取值： 净利润(万元), 所得税费用(万元)
           算法：
                 净利润率 = 净利润(万元) / 营业收入(万元)
                 净利润(万元) = 利润总额(万元) - 所得税费用(万元) ??
    """
    lrb_df = parse_finance_file(stock_code, "lrb", "report")

    net_profit = _get_row_numeric(lrb_df[date_list], u"净利润(万元)")
    income = _get_row_numeric(lrb_df[date_list], u"营业收入(万元)")

    ret_df = lrb_df[date_list].copy(deep=True)
    ret_df.ix[u"净利润率"] = net_profit / income * 100.0

    return ret_df.ix[[u"净利润率"]]


"""
4. 资产负债率
   读取数据
       来自： 偿还能力
       取值： 资产负债率(%)
   计算数据
       来自： 资产负债表
       取值： 资产总计(万元), 负债合计(万元)
       算法：
             资产负债率 = 负债合计(万元) / 资产总计(万元)
"""

"""
5. 固定资产比重
   读取数据
       来自： 偿还能力
       取值： 固定资产比重(%)
   计算数据
       来自： 资产负债表
       取值： 资产总计(万元), 固定资产净值(万元)
       算法：
             资产负债率 = 固定资产净值(万元) / 资产总计(万元)
"""

"""
6. 净资产收益率
   读取数据
       来自： 盈利能力
       取值： 净资产收益率(%)
   计算数据
       来自： 资产负债表, 利润表
       取值： 归属于母公司股东权益合计(万元)[??主要财务指标:净利润(万元)], 归属于母公司所有者的净利润(万元)
       算法：
             净资产收益率 = 归属于母公司所有者的净利润(万元) / 归属于母公司股东权益合计(万元)
"""

"""
7. 总资产周转率
   读取数据
       来自： 营运能力
       取值： 总资产周转率(次)
   计算数据
       来自： 资产负债表, 利润表
       取值： 资产总计(万元), 营业收入(万元)
       算法：
             净资产收益率 = 营业收入(万元) / ((资产总计(万元) + 资产总计(万元)(last year)) / 2)
"""

"""
8. 经营性现金流净额/净利润
   读取数据
       来自： 营运能力
       取值： 经营现金净流量与净利润的比率(%)
   计算数据
       来自： 现金流量表, 利润表
       取值： 经营活动产生的现金流量净额(万元), 净利润(万元)
       算法：
             经营性现金流净额/净利润 = 经营活动产生的现金流量净额(万元) / 净利润(万元)
"""

"""
9. 过去三年营业收入增长率 （3行）
   读取数据
       来自： 成长能力
       取值： 主营业务收入增长率(%)
   计算数据
       来自： 利润表
       取值： 营业收入(万元)
       算法：
             营业收入(万元)(this year) - 营业收入(万元)(last year) / 营业收入(万元)(last year)
"""

"""
10. 过去三年净利润增长率（扣除非经常性损益后）
   读取数据
       来自： 成长能力
       取值： 净利润增长率(%)
   计算数据
       来自： 主要财务指标
       取值： 净利润(扣除非经常性损益后)(万元)
       算法：
             净利润(扣除非经常性损益后)(万元)(this year) - 净利润(扣除非经常性损益后)(万元)(last year) / 净利润(扣除非经常性损益后)(万元)(last year)
"""


if __name__ == "__main__":
    # 设置显示精度为两位小数
    # pd.set_option('precision', 3)

    ret = gross_profit_rate("300438", ["2017-09-30", "2017-06-30"])
    print(ret)
    print("-" * 30)

    ret = expense_rate("300438", ["2017-09-30", "2017-06-30"])
    print(ret)
    print("-" * 30)

    ret = net_profit_rate("300438", ["2017-09-30", "2017-06-30"])
    print(ret)
    print("-" * 30)
