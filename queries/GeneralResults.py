import json
import requests
import pandas as pd
import os
import datetime as dt
import psutil
import time


class GeneralResults:
    """
    This class allows you to generate the statistics
    of the best products based on how much they generate,
    also the products that have increased and decreased their
    incomings
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

        self.parameters_best_products = [self.shop, self.start_date,
                                         self.end_date] * 2
        # General Query
        self.best_products_query = "SELECT\
                                    name,\
                                    brand,\
                                    \"UnidadesVendidas\",\
                                    total,\
                                    \"IngresosConBusqueda\" * 100.0 / total\
                                    FROM (SELECT\
                                    variant_id,\
                                    name,\
                                    brand,\
                                    sum(\"stats.nconv\") as \
                                        \"UnidadesVendidas\",\
                                    sum(\"stats.pconv\") as total\
                                    FROM \"%s PRODUCTS\"\
                                    where TIME_IN_INTERVAL(__time, '%s/%s')\
                                    GROUP BY 1, 2, 3) as tb2 \
                                    LEFT JOIN \
                                    (SELECT\
                                    variant_id,\
                                    sum(\"stats.pconv\") as \
                                        \"IngresosConBusqueda\"\
                                    FROM \"%s PRODUCTS\"\
                                    where TIME_IN_INTERVAL(__time, '%s/%s') \
                                        and \"stats.vclickconv\" >= 1\
                                    GROUP BY variant_id) as tb1 \
                                    ON tb1.variant_id = tb2.variant_id\
                                    GROUP BY 1, 2, 3, 4, 5\
                                    ORDER BY total DESC\
                                    " % tuple(self.parameters_best_products)

        # Comparative dates
        self.month_1 = self.month - 1
        self.month_2 = self.month
        self.limit_query = limit

        # Comparative queries
        self.comparative_query = "SELECT tb1.name,\
                                  tb1.brand,\
                                  tb1.\"UnidadesVendidas\",\
                                  tb1.\"TotalIngresosporVenta\",\
                                  tb2.\"UnidadesVendidas\",\
                                  tb2.\"TotalIngresosporVenta\",\
                                  tb2.\"TotalIngresosporVenta\"- \
                                      tb1.\"TotalIngresosporVenta\"\
                                  from (SELECT \
                                  name, brand,\
                                  sum(\"stats.pconv\") as \
                                    \"TotalIngresosporVenta\",\
                                  sum(\"stats.nconv\") as \"UnidadesVendidas\"\
                                  FROM \"%s PRODUCTS\"\
                                  where  TIME_EXTRACT(__time, 'MONTH')\
                                       = %s\
                                  GROUP BY name, brand\
                                  ORDER BY 3) as tb1\
                                  INNER JOIN\
                                  (SELECT \
                                  name,\
                                  sum(\"stats.pconv\") as\
                                    \"TotalIngresosporVenta\",\
                                  sum(\"stats.nconv\") as \"UnidadesVendidas\"\
                                  FROM \"%s PRODUCTS\"\
                                  where TIME_EXTRACT(__time, 'MONTH')\
                                       = %s\
                                  GROUP BY name\
                                  ORDER BY 2) as tb2\
                                  ON tb1.name = tb2.name\
                                  GROUP BY 1,2,3,4,5,6,7\
                                  ORDER BY 7 %s\
                                  LIMIT %s"
        self.rise_query = self.comparative_query % (self.shop,
                                                    self.month_1,
                                                    self.shop,
                                                    self.month_2,
                                                    "DESC",
                                                    self.limit_query)
        self.fall_query = self.comparative_query % (self.shop,
                                                    self.month_1,
                                                    self.shop,
                                                    self.month_2,
                                                    "ASC",
                                                    self.limit_query)
        self.writer = pd.ExcelWriter("generalResults" + str(self.year) +
                                     "-" + str(self.month) + '.' +
                                     self.shop + '.xlsx')

    def generate_generals(self):
        """
        Compute the general query, where the brand, income, sold units and
        percentage by searcher is calculated, the save it in a dataFrame
        """
        payload_generals = json.dumps({"query": self.best_products_query,
                                       "resultFormat": "array",
                                       "context": {
                                        "maxNumTasks": 4
                                       }})
        response_generals = requests.request("POST", self.url,
                                             headers=self.headers,
                                             data=payload_generals
                                             ).json()

        # We save each result in an list
        self.df_general = pd.DataFrame(response_generals,
                                       columns=["Producto", "Marca",
                                                "Unidades Vendidas",
                                                "Total ingresos por venta",
                                                "Ingresos con Búsqueda"])

    def generate_general_xlsx(self, route: str = ''):
        """
        Export the current dateframe to an excel file
        with extension xlsx
        """
        self.df_general.to_excel(self.writer, sheet_name="General" +
                                 str(self.interval) + "months", index=False)

    def memory_usage_psutil(self) -> float:
        """
        return the memory usage in MB
        """
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / float(2 ** 20)
        return mem

    def generate_rise_products(self):
        payload_rise = json.dumps({"query": self.rise_query,
                                   "resultFormat": "array",
                                   "context": {
                                     "maxNumTasks": 4
                                              }})
        response_rise = requests.request("POST", self.url,
                                         headers=self.headers,
                                         data=payload_rise
                                         ).json()
        self.df_rise = pd.DataFrame(response_rise,
                                    columns=["Productos con mayor alza en \
                                             ventas", "Marca", "Unidades",
                                             "Ventas", "Unidades", "Ventas",
                                             "Diferencia($)"])

    def generate_rise_xlsx(self, route: str = ''):
        """
        Export the current dateframe to an excel file
        with extension xlsx
        """
        self.df_rise.to_excel(self.writer, sheet_name="Rise",
                              index=False)

    def generate_fall_products(self):
        payload_fall = json.dumps({"query": self.fall_query,
                                   "resultFormat": "array",
                                   "context": {
                                     "maxNumTasks": 4
                                              }})
        response_fall = requests.request("POST", self.url,
                                         headers=self.headers,
                                         data=payload_fall
                                         ).json()
        self.df_fall = pd.DataFrame(response_fall,
                                    columns=["Productos con mayor baja en \
                                             ventas", "Marca", "Unidades",
                                             "Ventas", "Unidades", "Ventas",
                                             "Diferencia($)"])

    def generate_fall_xlsx(self, route: str = ''):
        """
        Export the current dateframe to an excel file
        with extension xlsx
        """
        self.df_fall.to_excel(self.writer, sheet_name="Fall",
                              index=False)

    def close_excel(self):
        """
        Close and save the actual excel for this query
        """
        self.writer.close()


start = time.time()
general_results = GeneralResults(2022, 12, 6, "Pepeganga")
general_results.generate_generals()
general_results.generate_rise_products()
general_results.generate_fall_products()

print("Peak Ram in MB:", round(general_results.memory_usage_psutil(), 2))
end = time.time()
print("Total time in seconds:", round(end - start, 2))

# general_results.generate_general_xlsx()
# general_results.generate_fall_xlsx()
# general_results.generate_rise_xlsx()
# general_results.close_excel()
