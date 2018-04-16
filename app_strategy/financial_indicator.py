# coding=utf-8

from crawler import get_finance_sheet_df
from common.df_utils import *
from common.constant import *
from common.messy import *


class FinanceIndicator(object):
    def __init__(self, stock_code, date_list=None):
        term_type = 'report'
        self.zycwzb_a = get_finance_sheet_df(stock_code, 'zycwzb', term_type)
        self.ylnl_a = get_finance_sheet_df(stock_code, 'zycwzb', term_type, 'ylnl')
        self.cznl_a = get_finance_sheet_df(stock_code, 'zycwzb', term_type, 'cznl')
        self.chnl_a = get_finance_sheet_df(stock_code, 'zycwzb', term_type, 'chnl')
        self.yynl_a = get_finance_sheet_df(stock_code, 'zycwzb', term_type, 'yynl')
        self.cwbbzy_a = get_finance_sheet_df(stock_code, 'cwbbzy', term_type)
        self.zcfzb_a = get_finance_sheet_df(stock_code, 'zcfzb', term_type)
        self.lrb_a = get_finance_sheet_df(stock_code, 'lrb', term_type)
        self.xjllb_a = get_finance_sheet_df(stock_code, 'xjllb', term_type)
        if date_list is None:
            date_list = list(self.lrb_a.columns)[:-1]
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
        # self._to_json()

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

    ####################################################################################################################
    # LiJie indicators
    ####################################################################################################################
    def gross_profit_rate(self):
        read_value = df_get_row_numeric(self.ylnl, u'销售毛利率(%)')
        compute_value = (1 - df_get_row_numeric(self.lrb, u'营业成本(万元)') / self.main_business_income()) * 100
        self._check_algorithm('gross_profit_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['gross_profit_rate']
        return compute_value

    def net_profit_rate(self):
        read_value = df_get_row_numeric(self.ylnl, u'销售净利率(%)')
        compute_value = self.net_profit() / self.main_business_income() * 100
        self._check_algorithm('net_profit_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['net_profit_rate']
        return compute_value

    def three_expenses_ratio(self):
        read_value = df_get_row_numeric(self.ylnl, u'三项费用比重(%)')
        compute_value = (df_get_row_numeric(self.lrb, u'销售费用(万元)') + df_get_row_numeric(self.lrb, u'管理费用(万元)')
                         + df_get_row_numeric(self.lrb, u'财务费用(万元)')) / self.main_business_income() * 100
        self._check_algorithm('three_expense_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['three_expenses_ratio']
        return compute_value

    def sales_expenses_ratio(self):
        compute_value = df_get_row_numeric(self.lrb, u'销售费用(万元)') / self.main_business_income() * 100
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['sales_expenses_ratio']
        return compute_value

    def administrative_expenses_ratio(self):
        compute_value = df_get_row_numeric(self.lrb, u'管理费用(万元)') / self.main_business_income() * 100
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['administrative_expenses_ratio']
        return compute_value

    def financial_expenses_ratio(self):
        compute_value = df_get_row_numeric(self.lrb, u'财务费用(万元)') / self.main_business_income() * 100
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['financial_expenses_ratio']
        return compute_value

    def assets_liabilities_ratio(self):
        read_value = df_get_row_numeric(self.chnl, u'资产负债率(%)')
        compute_value = df_get_row_numeric(self.zcfzb, u'负债合计(万元)') / df_get_row_numeric(self.zcfzb, u'资产总计(万元)') * 100
        self._check_algorithm('assets_liabilities_ratio', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['assets_liabilities_ratio']
        return compute_value

    def roe(self):
        read_value = df_get_row_numeric(self.ylnl, u'净资产收益率(%)')
        compute_value = self.parent_company_net_profit() / self.parent_company_shareholders_equity() * 100
        self._check_algorithm('roe', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['roe']
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
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['total_assets_turnover_ratio']
        return compute_value

    def cffo_net_profit_ratio(self):
        read_value = df_get_row_numeric(self.yynl, u'经营现金净流量与净利润的比率(%)')
        compute_value = df_get_row_numeric(self.xjllb, u'经营活动产生的现金流量净额(万元)') / self.net_profit()
        self._check_algorithm('cffo_net_profit_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['cffo_net_profit_ratio']
        return compute_value

    def major_business_income_increase_rate(self):
        read_value = df_get_row_numeric(self.cznl, u'主营业务收入增长率(%)')
        term_last_year = self.main_business_income(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.main_business_income() / term_last_year - 1) * 100
        self._check_algorithm('major_business_income_increase_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['major_business_income_increase_rate']
        return compute_value

    def net_profit_increase_rate(self):
        read_value = df_get_row_numeric(self.cznl, u'净利润增长率(%)')
        term_last_year = self.net_profit(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.net_profit() / term_last_year - 1) * 100
        self._check_algorithm('net_profit_increase_rate', read_value, compute_value)
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['net_profit_increase_rate']
        return compute_value

    def net_profit_exclude_increase_rate(self):
        term_last_year = self.net_profit_exclude(self._get_term_last_year())
        term_last_year.index = self.date_list
        compute_value = (self.net_profit_exclude() / term_last_year - 1) * 100
        compute_value.name = FinanceIndicator._customized_indicators_name_dict['net_profit_exclude_increase_rate']
        return compute_value

    ####################################################################################################################
    # season indicators
    ####################################################################################################################
    def season_main_business_income(self):
        report_value = self.main_business_income()
        last_report_value = self.main_business_income(self._get_term_last_report())
        season_value = self._compute_season_value(report_value, last_report_value)
        season_value.name = FinanceIndicator._customized_indicators_name_dict['season_main_business_income']
        return season_value

    def season_net_profit(self):
        report_value = self.net_profit()
        last_report_value = self.net_profit(self._get_term_last_report())
        season_value = self._compute_season_value(report_value, last_report_value)
        season_value.name = FinanceIndicator._customized_indicators_name_dict['season_net_profit']
        return season_value

    def season_net_profit_exclude(self):
        report_value = self.net_profit_exclude()
        last_report_value = self.net_profit_exclude(self._get_term_last_report())
        season_value = self._compute_season_value(report_value, last_report_value)
        season_value.name = FinanceIndicator._customized_indicators_name_dict['season_net_profit_exclude']
        return season_value

    def get_indicator(self, indicator_type, indicator_name):
        if indicator_type == u'主要财务指标':
            return df_get_row_numeric(self.zycwzb, indicator_name)
        elif indicator_type == u'盈利能力':
            return df_get_row_numeric(self.ylnl, indicator_name)
        elif indicator_type == u'成长能力':
            return df_get_row_numeric(self.cznl, indicator_name)
        elif indicator_type == u'偿还能力':
            return df_get_row_numeric(self.chnl, indicator_name)
        elif indicator_type == u'营运能力':
            return df_get_row_numeric(self.yynl, indicator_name)
        elif indicator_type == u'财务报表摘要':
            return df_get_row_numeric(self.cwbbzy, indicator_name)
        elif indicator_type == u'资产负债表':
            return df_get_row_numeric(self.zcfzb, indicator_name)
        elif indicator_type == u'利润表':
            return df_get_row_numeric(self.lrb, indicator_name)
        elif indicator_type == u'现金流量表':
            return df_get_row_numeric(self.xjllb, indicator_name)
        elif indicator_type == u'其它':
            if indicator_name not in FinanceIndicator._customized_indicators:
                raise error.ServerException(error.SERVER_ERR_WRONG_PARAM,
                                      'unknown customized indicator: {}'.format(indicator_name))
            func = FinanceIndicator._customized_indicators[indicator_name]
            return func(self)
        else:
            raise error.ServerException(error.SERVER_ERR_WRONG_PARAM,
                                  'unknown indicator: {} - {}'.format(indicator_type, indicator_name))

    @staticmethod
    def all_indicators_dict():
        return FinanceIndicator._all_indicators

    @staticmethod
    def all_indicators_json():
        return FinanceIndicator._all_indicators_json

    def _to_json(self):
        indicator_dict = {
            u'主要财务指标': [indicator for indicator in self.zycwzb.index],
            u'盈利能力': [indicator for indicator in self.ylnl.index],
            u'成长能力': [indicator for indicator in self.cznl.index],
            u'偿还能力': [indicator for indicator in self.chnl.index],
            u'营运能力': [indicator for indicator in self.yynl.index],
            u'财务报表摘要': [indicator for indicator in self.cwbbzy.index],
            u'资产负债表': [indicator for indicator in self.zcfzb.index],
            u'利润表': [indicator for indicator in self.lrb.index],
            u'现金流量表': [indicator for indicator in self.xjllb.index],
        }
        with codecs.open(FinanceIndicator._fi_json_file, 'w', encoding='utf-8') as f:
            json.dump(indicator_dict, f, ensure_ascii=False)

    def _check_algorithm(self, algorithm_name, read_value, compute_value, given_date_list=None, deviation=0.01):
        if given_date_list is None:
            given_date_list = self.date_list
        for date in given_date_list:
            e = error.ServerException(error.SERVER_ERR_INTERNAL,
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

    def _get_term_last_report(self):
        new_date_list = []
        for date in self.date_list:
            y, m, d = date.split('-')
            if m == '12':
                new_date_list.append('{}-{}-{}'.format(y, '09', '30'))
            elif m == '09':
                new_date_list.append('{}-{}-{}'.format(y, '06', '30'))
            elif m == '06':
                new_date_list.append('{}-{}-{}'.format(y, '03', '31'))
            elif m == '03':
                new_date_list.append('{}-{}-{}'.format(y, '01', '01'))
            else:
                raise error.ServerException(error.SERVER_ERR_WRONG_PARAM, 'date_list: {}'.format(self.date_list))
        return new_date_list

    def _compute_season_value(self, report_value, last_report_value):
        last_report_value.index = self.date_list
        for date in self.date_list:
            if df_numeric_is_nan(last_report_value[date]) and not df_numeric_is_nan(report_value[date]):
                last_report_value[date] = 0
        return report_value - last_report_value

    _fi_json_file = os.path.join(CONFIG_DIR, 'fi.json')
    _basic_indicators = json_file_to_dict(os.path.join(CONFIG_DIR, 'fi.json'))
    _customized_indicators = {
        u'销售毛利率(%)': gross_profit_rate,
        u'销售净利率(%)': net_profit_rate,
        u'三项费用比重(%)': three_expenses_ratio,
        u'销售费用比重(%)': sales_expenses_ratio,
        u'财务费用比重(%)': financial_expenses_ratio,
        u'管理费用比重(%)': administrative_expenses_ratio,
        u'资产负债率(%)': assets_liabilities_ratio,
        u'净资产收益率(%)': roe,
        u'总资产周转率(次)': total_assets_turnover_ratio,
        u'经营现金净流量与净利润的比率': cffo_net_profit_ratio,
        u'主营业务收入增长率(%)': major_business_income_increase_rate,
        u'净利润增长率(%)': net_profit_increase_rate,
        u'净利润(扣除非经常性损益后)增长率(%)': net_profit_exclude_increase_rate,

        # season indicators
        u'单季主营业务收入(万元)': season_main_business_income,
        u'单季净利润(万元)': season_net_profit,
        u'单季净利润(扣非后)(万元)': season_net_profit_exclude,
    }
    _all_indicators = dict(_basic_indicators, **{u'其它': _customized_indicators.keys()})
    _all_indicators_json = json.dumps(_all_indicators, ensure_ascii=False)

    _customized_indicators_name_dict = {func.__name__: name for name, func in _customized_indicators.items()}


if __name__ == '__main__':
    fi = FinanceIndicator('300438', ['2017-09-30', '2016-12-31', '2015-12-31', '2014-12-31'])
    # print fi.get_indicator(u'盈利能力', u'净资产收益率(%)')
    # print fi.get_indicator(u'其它', u'销售费用比重(%)')
    print(FinanceIndicator.all_indicators_dict())
    print('其它' in FinanceIndicator.all_indicators_dict())
