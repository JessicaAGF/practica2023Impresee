import json
import requests
import pandas as pd
import os
import datetime as dt
import psutil
import matplotlib.pyplot as plt
import time


class ResumeResults:

    """
    """

    def __init__(self, year: int, month: int, interval_months: int,
                 shop: str, limit: int = 10):
        # General Statistics date
        self.month = month
        self.year = year
        self.shop = shop
        self.interval = interval_months
        self.start_date = (dt.date(year, month, 1) -
                           pd.DateOffset(months=interval_months)).isoformat()
        self.end_date = (dt.date(year, month, 1) +
                         pd.DateOffset(months=1)).isoformat()

        self.headers = {
                        'Content-Type': 'application/json'
                       }
        # Url where SQL Queries are loaded
        self.url = "http://localhost:8888/druid/v2/sql/"

        self.monthly_income_query = "SELECT\
                                        TIME_FLOOR(__time, 'P1M') AS \"Time\",\
                                        ROUND(SUM(\"prod.q\" * \"prod.p\"), 0)\
                                        FROM \"%s EVENT PRODS CONVERSION\"\
                                        GROUP BY 1\
                                        ORDER BY 1 ASC" % (self.shop)

        self.monthly_searches_query = "SELECT \
                                       TIME_FLOOR(__time, 'P1M'),\
                                       COUNT(*)\
                                       FROM \"%s SEARCH\"\
                                       WHERE qfinal = 1\
                                       GROUP BY 1\
                                       ORDER BY 1 ASC" % (self.shop)

        self.daily_searches_query = "SELECT\
                                     TIME_FLOOR(__time, 'P1D'),\
                                     COUNT(*)\
                                     FROM \"%s SEARCH\"\
                                     WHERE TIME_IN_INTERVAL(__time, '%s/%s') \
                                        and qfinal = 1\
                                     GROUP BY 1\
                                     ORDER BY 1 ASC" % (self.shop,
                                                        self.start_date,
                                                        self.end_date)

        self.daily_conversion_query = "SELECT\
                                       TIME_FLOOR(__time, 'P1D'),\
                                       COUNT(*)\
                                       FROM \"%s EVENT CONVERSION\"\
                                       where TIME_IN_INTERVAL(__time, '%s/%s')\
                                       GROUP BY 1\
                                       ORDER BY 1 ASC" % (self.shop,
                                                          self.start_date,
                                                          self.end_date)

    def memory_usage_psutil(self) -> float:
        """
        return the memory usage in MB
        """
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / float(2 ** 20)
        return mem

    def generate_monthly_searches(self):
        """
        Compute the monthly count of searches for this shop
        """
        payload_searches = json.dumps({"query": self.monthly_searches_query,
                                       "resultFormat": "array",
                                       "context": {
                                         "maxNumTasks": 4
                                        }})
        response_searches = requests.request("POST", self.url,
                                             headers=self.headers,
                                             data=payload_searches
                                             ).json()

        # We save each result in an list
        self.df_monthly_searches = pd.DataFrame(response_searches,
                                                columns=["Mes", "Cantidad"])

    def generate_monthly_income(self):
        """
        Compute the monthly amount of income for this shop
        """
        payload_income = json.dumps({
                                        "query": self.monthly_income_query,
                                        "resultFormat": "array",
                                        "context": {
                                         "maxNumTasks": 4
                                                   }})
        response_income = requests.request("POST", self.url,
                                           headers=self.headers,
                                           data=payload_income
                                           ).json()

        # We save each result in an list
        self.df_monthly_income = pd.DataFrame(response_income,
                                              columns=["Mes", "Cantidad"])

    def generate_daily_conversion(self):
        """
        Compute the daily amount of conversion for this shop
        """
        payload_conversion = json.dumps({
                                        "query": self.daily_conversion_query,
                                        "resultFormat": "array",
                                        "context": {
                                         "maxNumTasks": 4
                                                   }})
        response_conversion = requests.request("POST", self.url,
                                               headers=self.headers,
                                               data=payload_conversion
                                               ).json()

        # We save each result in an list
        self.df_daily_conversion = pd.DataFrame(response_conversion,
                                                columns=["Dia", "Cantidad"])

    def generate_daily_searches(self):
        """
        Compute the daily count of searches for this shop
        """
        payload_searches = json.dumps({"query": self.daily_searches_query,
                                       "resultFormat": "array",
                                       "context": {
                                         "maxNumTasks": 4
                                        }})
        response_searches = requests.request("POST", self.url,
                                             headers=self.headers,
                                             data=payload_searches
                                             ).json()

        # We save each result in an list
        self.df_daily_searches = pd.DataFrame(response_searches,
                                              columns=["Dia", "Cantidad"])

    def generate_monthly_searches_graph(self):
        """
        """
        plt.plot(self.df_monthly_searches.loc[:, 'Mes'],
                 self.df_monthly_searches.loc[:, 'Cantidad'], '-')
        plt.xticks(rotation=60, fontsize=5)
        plt.ylabel("Searches Count")
        plt.xlabel("Months")
        plt.title("Monthly Searches")
        plt.tight_layout()
        plt.show()

    def generate_monthly_income_graph(self):
        """
        """
        plt.plot(self.df_monthly_income.loc[:, 'Mes'],
                 self.df_monthly_income.loc[:, 'Cantidad'], '-')
        plt.xticks(rotation=60, fontsize=5)
        plt.ylabel("Income Amount (MM)")
        plt.xlabel("Months")
        plt.title("Monthly Incomes")
        plt.tight_layout()
        plt.show()

    def generate_daily_conversion_graph(self):
        """
        """
        plt.plot(self.df_daily_conversion.loc[:, 'Mes'],
                 self.df_daily_conversion.loc[:, 'Cantidad'], '-')
        plt.xticks(rotation=60, fontsize=5)
        plt.ylabel("Conversion Count")
        plt.xlabel("Days")
        plt.title("Daily Conversions")
        plt.tight_layout()
        plt.show()

    def generate_daily_searches_graph(self):
        """
        """
        plt.plot(self.df_daily_searches.loc[:, 'Mes'],
                 self.df_daily_searches.loc[:, 'Cantidad'], '-')
        plt.xticks(rotation=60, fontsize=5)
        plt.ylabel("Searches Count")
        plt.xlabel("Days")
        plt.title("Dailys Searches")
        plt.tight_layout()
        plt.show()

    def to_csv(self):
        """
        """
        self.df_monthly_income.to_csv("MonthlyIncome.csv", sep=',',
                                      index=False)
        self.df_monthly_searches.to_csv("MonthlySearches.csv", sep=',',
                                        index=False)
        self.df_daily_searches.to_csv("DailySearches.csv", sep=',',
                                      index=False)
        self.df_daily_conversion.to_csv("DailyConversion.csv", sep=',',
                                        index=False)


start = time.time()
general_results = ResumeResults(2022, 12, 0, "Pepeganga")

# Monthly Searches
print("Monthly Searches")
general_results.generate_monthly_searches()
print("Peak Ram in MB:", round(general_results.memory_usage_psutil(), 2))
end = time.time()
print("Total time in seconds:", round(end - start, 2))

# Monthly Income
print("Monthly Income")
start = time.time()
general_results.generate_monthly_income()
print("Peak Ram in MB:", round(general_results.memory_usage_psutil(), 2))
end = time.time()
print("Total time in seconds:", round(end - start, 2))


# Daily Conversion
print("Daily Conversion")
start = time.time()
general_results.generate_daily_conversion()
print("Peak Ram in MB:", round(general_results.memory_usage_psutil(), 2))
end = time.time()
print("Total time in seconds:", round(end - start, 2))


# Daily Searches
print("Daily Searches")
start = time.time()
general_results.generate_daily_searches()
print("Peak Ram in MB:", round(general_results.memory_usage_psutil(), 2))
end = time.time()
print("Total time in seconds:", round(end - start, 2))
