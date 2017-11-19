# coding=utf-8

import tushare as ts
from utils import *


def _download_forecast(year, quarter):
    forecast = ts.forecast_data(year, quarter)
    forecast.set_index('code', inplace=True)
    forecast.to_csv(_get_forecast_file_path(year, quarter), encoding='utf-8')


def _download_report(year, quarter):
    df = ts.get_report_data(year, quarter)
    df.drop_duplicates(subset='code', inplace=True)
    df.sort_values(["profits_yoy"], inplace=True, ascending=False)
    df.set_index('code', inplace=True)
    return df


def _loop_retrieve_report_data(year, quarter):
    print("loop retrieve report data for " + str(year))
    filename = _get_report_file_path(year, quarter)
    dfall = None
    dfall_size = 0
    retry = 5
    while True:
        df = _download_report(year, quarter)
        retry = retry - 1
        if dfall is None:
            dfall = df
        else:
            dfall = df_concat([dfall, df])
            dfall = dfall[~dfall.index.duplicated()]
            dfall.sort_values(["profits_yoy"], inplace=True, ascending=False)

        size = len(dfall.index)
        print("=> size: " + str(size))

        if retry > 0 or size > dfall_size:
            dfall_size = size
            continue

        break

    dfall.to_csv(filename, encoding='utf-8')


def _get_forecast_file_path(year, quarter):
    return os.path.join(REPORT_DIR, "forecast_{}_{}.csv".format(year, quarter))


def _get_report_file_path(year, quarter):
    return os.path.join(REPORT_DIR, "report_{}_{}.csv".format(year, quarter))


def download_all(start_year, start_quarter, end_year, end_quarter):
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            if year == start_year and quarter < start_quarter:
                continue
            elif year == end_year and quarter > end_quarter:
                continue
            else:
                _download_forecast(year, quarter)
                _loop_retrieve_report_data(year, quarter)


if __name__ == "__main__":
    download_all(2017, 2, 2017, 3)
