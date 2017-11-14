# coding=utf-8

from dw.dw_api import get_finance_sheet
from utils import *


class FinanceIndicator(object):
    def __init__(self, stock_code, date_list):
        term_type = 'report'
        self.zycwzb_a = get_finance_sheet(stock_code, 'zycwzb', term_type)
        self.ylnl_a = get_finance_sheet(stock_code, 'zycwzb', term_type, 'ylnl')
        self.cznl_a = get_finance_sheet(stock_code, 'zycwzb', term_type, 'cznl')
        self.chnl_a = get_finance_sheet(stock_code, 'zycwzb', term_type, 'chnl')
        self.yynl_a = get_finance_sheet(stock_code, 'zycwzb', term_type, 'yynl')
        self.cwbbzy_a = get_finance_sheet(stock_code, 'cwbbzy', term_type)
        self.zcfzb_a = get_finance_sheet(stock_code, 'zcfzb', term_type)
        self.lrb_a = get_finance_sheet(stock_code, 'lrb', term_type)
        self.xjllb_a = get_finance_sheet(stock_code, 'xjllb', term_type)
        self.zycwzb = df_get_cols(self.zycwzb_a, date_list, raise_e=False)
        self.ylnl = df_get_cols(self.ylnl_a, date_list, raise_e=False)
        self.cznl = df_get_cols(self.cznl_a, date_list, raise_e=False)
        self.chnl = df_get_cols(self.chnl_a, date_list, raise_e=False)
        self.yynl = df_get_cols(self.yynl_a, date_list, raise_e=False)
        self.cwbbzy = df_get_cols(self.cwbbzy_a, date_list, raise_e=False)
        self.zcfzb = df_get_cols(self.zcfzb_a, date_list, raise_e=False)
        self.lrb = df_get_cols(self.lrb_a, date_list, raise_e=False)
        self.xjllb = df_get_cols(self.xjllb_a, date_list, raise_e=False)
        self.date_list = date_list

    def _check_algorithm(self, algorithm_name, read_value, compute_value, given_date_list=None, deviation=0.01):
        if given_date_list is None:
            given_date_list = self.date_list
        for date in given_date_list:
            e = ServerException(SERVER_ERR_INTERNAL,
                                'wrong {}: read_value[{}], compute_value[{}]'
                                .format(algorithm_name, read_value, compute_value))
            if df_numeric_is_nan(read_value[date]):
                continue
            elif df_numeric_is_nan(compute_value[date]):
                raise e
            else:
                diff = np.abs(compute_value[date] - compute_value[date])
                if diff >= deviation:
                    raise e

    def _get_term_start(self):
        return ['{}-12-31'.format(int(date.split('-')[0]) - 1) for date in self.date_list]

    def _get_term_last_year(self):
        new_date_list = []
        for date in self.date_list:
            y, m, d = date.split('-')
            new_date_list.append('{}-{}-{}'.format(int(y) - 1, m, d))
        return new_date_list

    def main_business_income(self, given_date_list=None):
        if given_date_list is None:
            given_date_list = self.date_list
            zycwzb = self.zycwzb
            lrb = self.lrb
        else:
            zycwzb = df_get_cols(self.zycwzb_a, given_date_list, raise_e=False)
            lrb = df_get_cols(self.lrb_a, given_date_list, raise_e=False)
        read_value = df_get_row_numeric(zycwzb, u'主营业务收入(万元)')
        compute_value = df_get_row_numeric(lrb, u'营业收入(万元)').copy(deep=True)
        self._check_algorithm('main_business_income', read_value, compute_value, given_date_list=given_date_list)
        compute_value.name = read_value.name
        return compute_value

    def net_profit(self, given_date_list=None):
        if given_date_list is None:
            given_date_list = self.date_list
            lrb = self.lrb
        else:
            lrb = df_get_cols(self.lrb_a, given_date_list, raise_e=False)
        read_value = df_get_row_numeric(lrb, u'净利润(万元)').copy(deep=True)
        compute_value = df_get_row_numeric(lrb, u'利润总额(万元)') - df_get_row_numeric(lrb, u'所得税费用(万元)')
        self._check_algorithm('net_profit', read_value, compute_value, given_date_list=given_date_list, deviation=1.1)
        for date in given_date_list:
            if df_numeric_is_nan(read_value[date]) and not df_numeric_is_nan(compute_value[date]):
                read_value[date] = df_numeric_is_nan(compute_value[date])
        return read_value

    def net_profit_exclude(self, given_date_list=None):
        if given_date_list is None:
            zycwzb = self.zycwzb
        else:
            zycwzb = df_get_cols(self.zycwzb_a, given_date_list, raise_e=False)
        return df_get_row_numeric(zycwzb, u'净利润(扣除非经常性损益后)(万元)').copy(deep=True)

    def parent_company_net_profit(self, given_date_list=None):
        if given_date_list is None:
            given_date_list = self.date_list
            zycwzb = self.zycwzb
            lrb = self.lrb
        else:
            zycwzb = df_get_cols(self.zycwzb_a, given_date_list, raise_e=False)
            lrb = df_get_cols(self.lrb_a, given_date_list, raise_e=False)
        read_value = df_get_row_numeric(zycwzb, u'净利润(万元)')
        compute_value = df_get_row_numeric(lrb, u'归属于母公司所有者的净利润(万元)').copy(deep=True)
        self._check_algorithm('main_business_income', read_value, compute_value, given_date_list=given_date_list)
        compute_value.name = read_value.name
        return compute_value

    def parent_company_shareholders_equity(self, given_date_list=None):
        if given_date_list is None:
            zcfzb = self.zcfzb
        else:
            zcfzb = df_get_cols(self.zcfzb_a, given_date_list, raise_e=False)
        return df_get_row_numeric(zcfzb, u'归属于母公司股东权益合计(万元)').copy(deep=True)

    def total_asset(self, given_date_list=None):
        if given_date_list is None:
            zcfzb = self.zcfzb
        else:
            zcfzb = df_get_cols(self.zcfzb_a, given_date_list, raise_e=False)
        return df_get_row_numeric(zcfzb, u'资产总计(万元)').copy(deep=True)

    def gross_profit_rate(self):
        read_value = df_get_row_numeric(self.ylnl, u'销售毛利率(%)')
        compute_value = (1 - df_get_row_numeric(self.lrb, u'营业成本(万元)') / self.main_business_income()) * 100
        self._check_algorithm('gross_profit_rate', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def net_profit_rate(self):
        read_value = df_get_row_numeric(self.ylnl, u'销售净利率(%)')
        compute_value = self.net_profit() / self.main_business_income() * 100
        self._check_algorithm('net_profit_rate', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def three_expense_rate(self):
        read_value = df_get_row_numeric(self.ylnl, u'三项费用比重(%)')
        compute_value = (df_get_row_numeric(self.lrb, u'销售费用(万元)') + df_get_row_numeric(self.lrb, u'管理费用(万元)')
                         + df_get_row_numeric(self.lrb, u'财务费用(万元)')) / self.main_business_income() * 100
        self._check_algorithm('three_expense_rate', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def sales_expenses_rate(self):
        compute_value = df_get_row_numeric(self.lrb, u'销售费用(万元)') / self.main_business_income() * 100
        compute_value.name = u'销售费用比重(%)'
        return compute_value

    def administrative_expenses_rate(self):
        compute_value = df_get_row_numeric(self.lrb, u'管理费用(万元)') / self.main_business_income() * 100
        compute_value.name = u'管理费用比重(%)'
        return compute_value

    def financial_expenses_rate(self):
        compute_value = df_get_row_numeric(self.lrb, u'财务费用(万元)') / self.main_business_income() * 100
        compute_value.name = u'财务费用比重(%)'
        return compute_value

    def assets_liabilities_ratio(self):
        read_value = df_get_row_numeric(self.chnl, u'资产负债率(%)')
        compute_value = df_get_row_numeric(self.zcfzb, u'负债合计(万元)') / df_get_row_numeric(self.zcfzb, u'资产总计(万元)') * 100
        self._check_algorithm('assets_liabilities_ratio', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def roe(self):
        read_value = df_get_row_numeric(self.ylnl, u'净资产收益率(%)')
        compute_value = self.parent_company_net_profit() / self.parent_company_shareholders_equity() * 100
        self._check_algorithm('roe', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def total_assets_turnover_ratio(self):
        read_value = df_get_row_numeric(self.yynl, u'总资产周转率(次)')
        term_start = self.total_asset(self._get_term_start())
        term_start.index = self.date_list
        term_end = self.total_asset()
        for date in self.date_list:
            if df_numeric_is_nan(term_start[date]) and not df_numeric_is_nan(term_end[date]):
                term_start[date] = term_end[date]
        term_avg = (term_start + term_end) / 2
        compute_value = self.main_business_income() / term_avg
        self._check_algorithm('total_assets_turnover_ratio', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def cffo_net_profit_rate(self):
        read_value = df_get_row_numeric(self.yynl, u'经营现金净流量与净利润的比率(%)')
        compute_value = df_get_row_numeric(self.xjllb, u'经营活动产生的现金流量净额(万元)') / self.net_profit()
        self._check_algorithm('cffo_net_profit_rate', read_value, compute_value)
        compute_value.name = u'经营现金净流量与净利润的比率'
        return compute_value

    def major_business_income_increase_rate(self):
        read_value = df_get_row_numeric(self.cznl, u'主营业务收入增长率(%)')
        term_last_year = self.main_business_income(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.main_business_income() / term_last_year - 1) * 100
        self._check_algorithm('major_business_income_increase_rate', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def net_profit_increase_rate(self):
        read_value = df_get_row_numeric(self.cznl, u'净利润增长率(%)')
        term_last_year = self.net_profit(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.net_profit() / term_last_year - 1) * 100
        self._check_algorithm('net_profit_increase_rate', read_value, compute_value)
        compute_value.name = read_value.name
        return compute_value

    def net_profit_exclude_increase_rate(self):
        term_last_year = self.net_profit_exclude(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.net_profit_exclude() / term_last_year - 1) * 100
        compute_value.name = u'净利润(扣除非经常性损益后)增长率(%)'
        return compute_value


if __name__ == '__main__':
    # fi = FinanceIndicator('300438', ['2017-09-30', '2016-12-31', '2015-12-31', '2014-12-31'])
    fi = FinanceIndicator('600276', ['2017-09-30', '2017-06-30', '2017-03-31', '2016-12-31', '2015-12-31', '2014-12-31', '2013-12-31', '2012-12-31'])
    # print fi.gross_profit_rate()
    # print fi.net_profit_rate()
    # print fi.three_expense_rate()
    # print fi.sales_expenses_rate()
    # print fi.financial_expenses_rate()
    # print fi.administrative_expenses_rate()
    # print fi.assets_liabilities_ratio()
    # print fi.roe()
    # print fi.total_assets_turnover_ratio()
    # print fi.cffo_net_profit_rate()
    # print fi.major_business_income_increase_rate()
    # print fi.net_profit_exclude_increase_rate()

    # pd.set_option("precision", 2)
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    print series_list_to_df_as_row([fi.gross_profit_rate(),
                                    fi.net_profit_rate(),
                                    fi.three_expense_rate(),
                                    fi.sales_expenses_rate(),
                                    fi.financial_expenses_rate(),
                                    fi.administrative_expenses_rate(),
                                    fi.assets_liabilities_ratio(),
                                    fi.total_asset(),
                                    fi.roe(),
                                    fi.total_assets_turnover_ratio(),
                                    fi.cffo_net_profit_rate(),
                                    fi.major_business_income_increase_rate(),
                                    fi.net_profit_exclude_increase_rate()
                                    ])
