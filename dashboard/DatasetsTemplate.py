import requests
# import json
# from IPython.display import JSON
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import datetime as dt
# import psutil
# import os
# import sys
# import time


class DatasetsTemplate(object):
    """
    This class allows to create virtual datasets and instance
    some physical ones, that ar necesary to create all the charts
    for a dashboard.
    """

    def __init__(self, store_name: str, token: str) -> None:
        self.base_url = 'http://localhost:8088'
        self.dataset_url = '/api/v1/dataset/'
        self.name = store_name
        self.datasets = {}
        self.headers_auth = {
            'Authorization': 'Bearer ' + token
        }

    def get_datasets_id(self) -> dict:
        """
        Returns a dictionary containing the id of each dataset associated
        with its name
        """
        return self.datasets

    def create_general_results_dataset(self) -> None:
        """
        Create a virtual set with the general metrics for a store
        """
        sql_query = f"SELECT \
                    substring(CAST(tb1.\"Time\" as VARCHAR), 1, 7)\
                       as \"Fecha\",\
                    tb5.\"VB\" as\
                       \"Visitantes que usan el buscador\",\
                    tb4.\"Búsquedas del periodo\" as\
                       \"Búsquedas del periodo\",\
                    tb1.\"Órdenes de compra\" as \"Órdenes de compra\",\
                    tb2.\"Unidades Vendidas\" as \"Unidades Vendidas\",\
                    tb2.\"Dinero en ventas\" as \"Dinero en ventas\",\
                    tb3.\"Dvb\" as \"Dinero en ventas desde el buscador\",\
                    tb3.\"Dvb\" * 1.0 / tb2.\"Dinero en ventas\" as\
                        \"Participación del buscador\"\
                    FROM\
                    (SELECT\
                    TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                    COUNT(*) as \"Órdenes de compra\"\
                    FROM \"{self.name} EVENT CONVERSION\"\
                    GROUP BY 1) as tb1 \
                    INNER  JOIN \
                    (SELECT \
                      TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                      ROUND(SUM(\"prod.q\" * \"prod.p\"), 0) as\
                         \"Dinero en ventas\",\
                      SUM(\"prod.q\") as \"Unidades Vendidas\"\
                      FROM \"{self.name} EVENT PRODS CONVERSION\" \
                      GROUP BY 1) as tb2 ON tb1.\"Time\" = tb2.\"Time\"\
                    INNER JOIN (SELECT \
                      TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                      ROUND(SUM(\"prod.q\" * \"prod.p\"), 0) as \"Dvb\" \
                      FROM \"{self.name} EVENT PRODS CONVERSION\" \
                      WHERE \"prod.wc\" = 1 or \"prod.wh\" = 1 or\
                         \"prod.wci\" = 1 or \"prod.wcs\"= 1\
                      GROUP BY 1) as tb3 ON tb2.\"Time\" = tb3.\"Time\"\
                      INNER JOIN (SELECT \
                      TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                      COUNT(*) as \"Búsquedas del periodo\" \
                      FROM \"{self.name} SEARCH\" \
                      GROUP BY 1) as tb4 ON tb3.\"Time\" = tb4.\"Time\"\
                      INNER JOIN (SELECT \"VB\" / \"Total\" as \"VB\",\
                      tba1.\"Time\" as \"Time\" FROM (SELECT \
                      TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                      COUNT(DISTINCT vid) * 1.0  as \"VB\"\
                      FROM \"{self.name} SEARCH\" \
                      WHERE qfinal = 1 \
                      GROUP BY 1) as tba1 INNER JOIN\
                      (SELECT COUNT(*) as \"Total\" ,\
                      TIME_FLOOR(__time, 'P1M') as \"Time\" \
                      FROM \"{self.name} VISITORS\" GROUP by 2)\
                      as tba2 on tba1.\"Time\" = tba2.\"Time\") as tb5\
                      ON tb4.\"Time\" = tb5.\"Time\""

        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"General Results {self.name}"}

        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["General Results"] = r.json()['id']

        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["General Results"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_searches_group_by_day_dataset(self) -> None:
        """
        Create a virtual dataset which agroup the searches per day
        """
        sql_query = f"SELECT \
                     TIME_PARSE(TIME_FORMAT(tb1.\"Day\",\
                      'mm-dd'), 'mm-dd') as __time,\
                     substring(CAST(tb1.\"Time\" as VARCHAR), 1, 7) as\
                       \"Fecha\",\
                     tb1.Cantidad as \"Cantidad de búsquedas\"\
                     FROM (SELECT \
                     TIME_FLOOR(__time, 'P1D') as \"Day\",\
                     TIME_FLOOR(__time, 'P1M') AS \"Time\",\
                     COUNT(*) as Cantidad\
                     from \"{self.name} SEARCH\"\
                     GROUP BY 1,2) as tb1"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Searches group by day {self.name}"}
        r = requests.put(self.base_url + self.dataset_url, json=payload,
                         headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Searches group by day"] = r.json()['id']

        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }, {
                            "column_name": "__time",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Searches group by day"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_incomes_group_by_day_dataset(self) -> None:
        """
        Create a virtual dataset which agroup the searches per day
        """
        sql_query = f"SELECT \
                     TIME_PARSE(TIME_FORMAT(tb1.\"Day\", 'mm-dd'),\
                      'mm-dd') as __time,\
                     substring(CAST(tb1.\"Time\" as VARCHAR), 1, 7) as\
                       \"Fecha\",\
                     tb1.Ingreso as \"Ingreso mes actual\"\
                     FROM (SELECT \
                     TIME_FLOOR(__time, 'P1D') as \"Day\",\
                     TIME_FLOOR(__time, 'P1M') AS \"Time\",\
                     sum(\"stats.pconv\") as Ingreso\
                     from \"{self.name} PRODUCTS\"\
                     GROUP BY 1,2) as tb1"

        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Incomes group by day {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Incomes group by day"] = r.json()['id']

        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }, {
                            "column_name": "__time",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Incomes group by day"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_incomes_per_searches_dataset(self) -> None:
        """
        Create a virtual dataset which compare the incomes
        differentiated by searches
        """
        sql_query = f"SELECT\
                      substring(CAST(tb2.\"Time\" as VARCHAR), 1, 7) as\
                        \"Fecha\",\
                      tb2.\"Dinero en ventas\" as \"Dinero en ventas\",\
                      tb3.\"Dvb\" as \"Dinero en ventas desde el buscador\"\
                      FROM\
                      (SELECT \
                        TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                        ROUND(SUM(\"prod.q\" * \"prod.p\"), 0) as\
                          \"Dinero en ventas\"\
                        FROM \"{self.name} EVENT PRODS CONVERSION\" \
                        GROUP BY 1) as tb2\
                      INNER JOIN (SELECT \
                        TIME_FLOOR(__time, 'P1M') AS \"Time\", \
                        ROUND(SUM(\"prod.q\" * \"prod.p\"), 0) as \"Dvb\" \
                        FROM \"{self.name} EVENT PRODS CONVERSION\" \
                        WHERE \"prod.wc\" = 1 or \"prod.wh\" = 1 or\
                          \"prod.wci\" = 1 or \"prod.wcs\"= 1\
                        GROUP BY 1) as tb3 ON tb2.\"Time\" = tb3.\"Time\""

        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Incomes per searches {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Incomes per searches"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Incomes per searches"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Incomes per searches"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_zero_hit_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the zero hits
        """
        sql_query = f"SELECT __time as \"Fecha\", B.txt AS Query, SUM(B.total)\
                      AS Total \
                      FROM ( \
                      SELECT __time, LOWER(\"in.intxt\") AS txt,\
                      COUNT(DISTINCT \"vid\") as total \
                        FROM \"{self.name} SEARCH\"\
                      WHERE zero = 0 AND qfinal = 1 \
                      GROUP BY  1, 2 ) AS A  \
                      RIGHT JOIN ( \
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") AS total  \
                      FROM \"{self.name} SEARCH\"  \
                      WHERE zero = 1 AND qfinal = 1  \
                      GROUP BY  1 ) AS B  \
                      ON A.txt = B.txt \
                      where B.total > 20 AND A.txt is NULL \
                      GROUP BY 1, 2 \
                      ORDER BY 2 DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Zero hits {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Zero hits"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Zero hits"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_zero_hit_restock_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the zero hits, that
        correspond to products that must be stocked
        """
        sql_query = f"SELECT B.txt AS Query, SUM(B.total) AS Total\
                      FROM (\
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") as total\
                           FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 0 AND  qfinal = 1\
                      GROUP BY  1 ) AS A \
                      INNER JOIN (\
                      SELECT LOWER(\"in.intxt\") AS txt,\
                        COUNT(DISTINCT \"vid\") AS total \
                      FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 1 AND qfinal = 1 \
                      GROUP BY  1 ) AS B \
                      ON A.txt = B.txt\
                      where B.total > 20\
                      GROUP BY 1\
                      ORDER BY 2 DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Zero hits restock {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Zero hits restock"] = r.json()['id']

    def create_zero_hit_new_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the new zero hits
        """
        sql_query = f"SELECT A1.Query, A1.Total FROM \
                      (SELECT B.txt AS Query, SUM(B.total) AS Total\
                      FROM (\
                      SELECT LOWER(\"in.intxt\") AS txt,\
                         COUNT(DISTINCT \"vid\") as total\
                           FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 0 AND qfinal = 1 AND\
                         TIME_FLOOR(__time, 'P1M') = \
                          TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M', 0),\
                            'P1M')\
                      GROUP BY  1 ) AS A \
                      RIGHT JOIN (\
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") AS total \
                      FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 1 AND qfinal = 1 AND \
                        TIME_FLOOR(__time, 'P1M') = \
                          TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M', -1),\
                            'P1M')\
                      GROUP BY  1 ) AS B \
                      ON A.txt = B.txt\
                      where B.total > 20 AND A.txt is NULL\
                      GROUP BY 1) AS A1\
                      LEFT JOIN(\
                      SELECT B.txt AS Query, SUM(B.total) AS Total\
                      FROM (\
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") as total \
                          FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 0 AND qfinal = 1 AND TIME_FLOOR(__time,\
                        'P1M') < TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                          'P1M', -1), 'P1M')\
                      GROUP BY  1 ) AS A \
                      RIGHT JOIN (\
                      SELECT LOWER(\"in.intxt\") AS txt,\
                         COUNT(DISTINCT \"vid\") AS total \
                      FROM \"{self.name} SEARCH TEXT\" \
                      WHERE zero = 1 AND qfinal = 1 AND\
                         TIME_FLOOR(__time, 'P1M') < \
                          TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, \
                            'P1M', -1), 'P1M')\
                      GROUP BY  1 ) AS B \
                      ON A.txt = B.txt\
                      where B.total > 20 AND A.txt is NULL \
                      GROUP BY 1) AS B1\
                      ON A1.Query = B1.Query\
                      WHERE B1.Query is NULL\
                      GROUP BY 1, 2"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Zero hits new {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Zero hits new"] = r.json()['id']

    def create_zero_hits_old_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the zero hits
        present in the last 3 months but no longer appearing
        """
        sql_query = f"SELECT A1.Query, A1.Total FROM\
                      (\
                      SELECT B.txt AS Query, SUM(B.total) AS Total\
                      FROM (\
                      SELECT LOWER(\"in.intxt\") AS txt,\
                         COUNT(DISTINCT \"vid\") as total FROM\
                           \"Infanti SEARCH\" \
                      WHERE zero = 0 AND qfinal = 1 AND TIME_FLOOR(__time,\
                         'P1M') < TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                           'P1M', 0), 'P1M')\
                      AND TIME_FLOOR(__time, 'P1M') >=\
                         TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M', -3),\
                           'P1M')\
                      GROUP BY  1 ) AS A \
                      RIGHT JOIN (\
                      SELECT LOWER(\"in.intxt\") AS txt,\
                         COUNT(DISTINCT \"vid\") AS total \
                      FROM \"{self.name} SEARCH\" \
                      WHERE zero = 1 AND qfinal = 1 AND TIME_FLOOR(__time,\
                         'P1M') < TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                           'P1M', 0), 'P1M')\
                      AND TIME_FLOOR(__time, 'P1M') >=\
                         TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M', -3),\
                           'P1M')\
                      GROUP BY  1 ) AS B \
                      ON A.txt = B.txt\
                      where B.total > 20 AND A.txt is NULL \
                      GROUP BY 1) AS A1\
                      LEFT JOIN \
                      (SELECT B.txt AS Query, SUM(B.total) AS Total\
                      FROM (\
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") as total \
                          FROM \"{self.name} SEARCH\" \
                      WHERE zero = 0 AND qfinal = 1 AND TIME_FLOOR(__time, \
                        'P1M') >= TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, \
                          'P1M', 0), 'P1M')\
                      GROUP BY  1 ) AS A \
                      RIGHT JOIN (\
                      SELECT LOWER(\"in.intxt\") AS txt, \
                        COUNT(DISTINCT \"vid\") AS total \
                      FROM \"{self.name} SEARCH\" \
                      WHERE zero = 1 AND qfinal = 1 AND TIME_FLOOR(__time, \
                        'P1M') >= TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                           'P1M', 0), 'P1M')\
                      GROUP BY  1 ) AS B \
                      ON A.txt = B.txt\
                      where B.total > 20 AND A.txt is NULL\
                      GROUP BY 1)AS B1\
                      ON A1.Query = B1.Query\
                      WHERE B1.Query is NULL\
                      GROUP BY 1,2"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Zero hits old {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Zero hits old"] = r.json()['id']

    def create_top_ten_products_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the top 10
        products with greates incomes
        """
        sql_query = f"SELECT\
                      __time as \"Fecha\"\
                      name as \"Producto\",\
                      brand as \"Marca\",\
                      \"UnidadesVendidas\" as \"Unidades vendidas\",\
                      total as \"Total ingresos por venta\",\
                      \"IngresosConBusqueda\" * 1.0 / total as\
                         \"Ingresos con búsqueda\"\
                      FROM \
                      (SELECT\
                          __time,\
                          variant_id,\
                          name,\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =   \
                          TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                          0), 'P1M')\
                          GROUP BY 1, 2, 3, 4) as tb2 \
                          LEFT JOIN \
                          (SELECT\
                          variant_id,\
                          sum(\"stats.pconv\") as \"IngresosConBusqueda\"\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =   \
                          TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                          0), 'P1M') and \"stats.vclickconv\" >= 1\
                          GROUP BY variant_id) as tb1 \
                          ON tb1.variant_id = tb2.variant_id\
                          GROUP BY 1, 2, 3, 4, 5, 6\
                          ORDER BY total DESC"
        payload = {
                    "database": 2,
                    "external_url": "",
                    "is_managed_externally": "false",
                    "owners": [],
                    "schema": "druid",
                    "sql": sql_query,
                    "table_name": f"Top ten products {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Top ten products"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Top ten products"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_change_incomes_per_products_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the variation of incomes
        in a month
        """
        sql_query = f"SELECT\
                      tb1.name as \"Producto\",\
                      tb1.brand as \"Marca\",\
                      tb1.\"UnidadesVendidas\" as\
                         \"Unidades vendidas mes anterior\",\
                      tb1.total as \"Total ingresos por venta mes anterior\",\
                      tb2.\"UnidadesVendidas\" as \"Unidades vendidas\",\
                      tb2.total as \"Total ingresos por venta\",\
                      tb2.total - tb1.total as \"Diferencia ($)\"\
                      FROM \
                      (SELECT\
                          variant_id,\
                          name,\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -1), 'P1M')\
                          GROUP BY 1, 2, 3) as tb2 \
                          LEFT JOIN \
                          (SELECT\
                          variant_id,\
                          name,\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -2), 'P1M')\
                          GROUP BY 1, 2, 3) as tb1 \
                          ON tb1.variant_id = tb2.variant_id\
                          GROUP BY 1, 2, 3, 4, 5, 6, 7"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Change incomes per product {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Change incomes per product"] = r.json()['id']

    def create_general_resultas_per_brand_dataset(self) -> None:
        """
        Create a virtual dataset that calculate the general metric
        for each brand
        """
        sql_query = f"SELECT\
                      tb1.brand as \"Marca\",\
                      \"UnidadesVendidas\" as \"Unidades vendidas\",\
                      total as \"Total ingresos por venta\",\
                      \"IngresosConBusqueda\" * 1.0 / total as\
                       \"Ingresos con búsqueda\",\
                      total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -1), 'P1M'))\
                                    as \"%participación\",\
                      total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -2), 'P1M'))\
                                    as \"%participación mes anterior\"\
                                    \
                      FROM \
                        (SELECT\
                          brand,\
                          sum(\"stats.pconv\") as \"IngresosConBusqueda\"\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -1), 'P1M')\
                              and \"stats.vclickconv\" >= 1\
                          GROUP BY 1) as tb1 \
                          LEFT JOIN\
                      (SELECT\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -1), 'P1M')\
                          GROUP BY 1) as tb2 \
                          ON tb1.brand = tb2.brand\
                          LEFT JOIN \
                          (SELECT\
                          brand,\
                          sum(\"stats.pconv\") as total2\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -2), 'P1M')\
                          GROUP BY 1) as tb3\
                          ON tb3.brand = tb1.brand\
                          GROUP BY 1, 2, 3, 4, 5, 6\
                          ORDER BY total DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"General results per brand {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["General results per brand"] = r.json()['id']

    def create_change_participation_brand_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the variation of participation
        in incomes of each brand in a month
        """
        sql_query = f"SELECT\
                      tb2.brand as \"Marca\",\
                      tb3.\"UnidadesVendidas\" as\
                         \"Unidades vendidas mes anterior\",\
                      total2 as \"Total ingresos por venta mes anterior\",\
                      total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                        'P1M', -1), 'P1M'))\
                                    as \"%participación mes anterior\",\
                      tb2.\"UnidadesVendidas\" as \"Unidades vendidas\",\
                      total as \"Total ingresos por venta\",\
                      total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', 0), 'P1M'))\
                                    as \"%participación\",\
                      (total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', 0), 'P1M'))) - \
                                          (total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') = \
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -1), 'P1M')))\
                                    as \"Diferencia de participación\"\
                      FROM \
                      (SELECT\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                               0), 'P1M')\
                          GROUP BY 1) as tb2\
                          LEFT JOIN \
                          (SELECT\
                          brand,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total2\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                               -1), 'P1M')\
                          GROUP BY 1) as tb3\
                          ON tb3.brand = tb2.brand\
                          GROUP BY 1, 2, 3, 4, 5, 6, 7, 8"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Change participation brand {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Change participation brand"] = r.json()['id']

    def create_participation_per_brand_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the participation
        in incomes of each brand in the curren month
        """
        sql_query = f"SELECT __time as \"Fecha\",\
                      \"brand\", \
                      SUM(\"prod.p\"*\"prod.q\") as total \
                        FROM \"{self.name} EVENT PRODS CONVERSION\" AS \
                          PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,\
                          brand FROM \"{self.name} PRODUCTS\") AS PROD\
                             on PRODCONV.\"prod.variant\" = PROD.variant_id \
                      WHERE \"brand\" is not null\
                      GROUP BY 1, 2\
                      ORDER BY 3 DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Participation per brand {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Participation per brand"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Participation per brand"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_brands_bought_together_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the brands thar are bought
        togehter in the same conversion
        """
        sql_query = f"SELECT __time as \"Fecha\", a, b, COUNT(*) FROM \
                      (SELECT A.__time as __time, A.cid ,\
                      A.brand as a, B.brand as b FROM \
                      (SELECT __time, cid, brand, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  brand FROM\
                         \"{self.name} PRODUCTS\") AS PROD \
                         on PRODCONV.\"prod.variant\" = PROD.variant_id) AS A\
                      INNER JOIN\
                      (SELECT __time, cid, brand, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  brand FROM\
                         \"{self.name} PRODUCTS\") AS PROD on\
                          PRODCONV.\"prod.variant\" = PROD.variant_id ) AS B\
                      ON A.__time = B.__time AND  A.cid = B.cid \
                      WHERE A.prod < B.prod\
                      GROUP BY 1, 2, 3, 4)\
                      GROUP BY 1, 2, 3"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Brands bought together {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Brands bought together"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Brands bought together"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_participation_per_category_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the participation
        in incomes of each category in the current month
        """
        sql_query = f"SELECT __time as \"Fecha\"\
                      \"category\", \
                      SUM(\"prod.p\"*\"prod.q\") as total \
                        FROM \"{self.name} EVENT PRODS CONVERSION\" AS \
                          PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,\
                          category FROM \"{self.name} PRODUCTS\") AS PROD\
                             on PRODCONV.\"prod.variant\" = PROD.variant_id \
                      WHERE \"category\" is not null\
                      GROUP BY 1, 2\
                      ORDER BY 3 DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Participation per category {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Participation per category"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Participation per category "]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_categories_bought_together_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the categories thar are
        bought togehter in the same conversion
        """
        sql_query = f"SELECT __time as \"Fecha\", a, b, COUNT(*) FROM \
                      (SELECT A.__time as __time, A.cid ,\
                       A.category as a, B.category as b FROM \
                      (SELECT __time, cid, category, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  category FROM\
                         \"{self.name} PRODUCTS\") AS PROD \
                         on PRODCONV.\"prod.variant\" = PROD.variant_id) AS A\
                      INNER JOIN\
                      (SELECT __time, cid, category, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  category FROM\
                         \"{self.name} PRODUCTS\") AS PROD on\
                          PRODCONV.\"prod.variant\" = PROD.variant_id) AS B\
                      ON A.__time = B.__time AND  A.cid = B.cid \
                      WHERE A.prod < B.prod\
                      GROUP BY 1,2,3,4)\
                      GROUP BY 1,2, 3"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Categories bought together {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Categories bought together"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Categories bought together"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def create_products_bought_together_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the products thar are
        bought togehter in the same conversion
        """
        sql_query = f"SELECT __time as \"Fecha\", a, b, COUNT(*) FROM\
                      (SELECT A.__time as __time, A.cid ,\
                      A.name as a, B.name as b FROM \
                      (SELECT __time, cid, name, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  name FROM\
                         \"{self.name} PRODUCTS\") AS PROD \
                         on PRODCONV.\"prod.variant\" = PROD.variant_id) AS A\
                      INNER JOIN\
                      (SELECT __time, cid, name, \"prod.variant\" as prod\
                         FROM \"{self.name} EVENT PRODS CONVERSION\" AS\
                           PRODCONV\
                      INNER JOIN (SELECT DISTINCT variant_id,  name FROM\
                         \"{self.name} PRODUCTS\") AS PROD on\
                          PRODCONV.\"prod.variant\" = PROD.variant_id) AS B\
                      ON A.__time = B.__time AND  A.cid = B.cid \
                      WHERE A.prod < B.prod\
                      GROUP BY 1,2,3,4)\
                      GROUP BY 1, 2, 3"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Products bought together {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Products bought together"] = r.json()['id']
        payload_time = {
                        "cache_timeout": 0,
                        "columns": [
                          {
                            "column_name": "Fecha",
                            "filterable": True,
                            "groupby": True,
                            "is_active": True,
                            "is_dttm": True,
                            "type": "string"
                          }
                        ],
                        "database_id": 2,
                        "is_managed_externally": False,
                        "offset": 0,
                        "owners": [],
                        "schema": "druid"
                      }
        time_url = (str(self.datasets["Products bought together"]) +
                    "?override_columns=true")
        r = requests.post(self.base_url + self.dataset_url + time_url,
                          json=payload_time, headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)

    def instance_event_conversion_dataset(self):
        """
        Instance as physical dataset the event conversion of
        the store
        """
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "druid",
                  "table_name": f"{self.name} EVENT CONVERSION"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name} EVENT CONVERSION"] = r.json()['id']

    def instance_search_dataset(self):
        """
        Instance as physical dataset the searches of
        the store
        """
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "druid",
                  "table_name": f"{self.name} SEARCH"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name} SEARCH"] = r.json()['id']

    def instance_event_prod_conversion_dataset(self):
        """
        Instance as physical dataset the event prod conversion of
        the store
        """
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "druid",
                  "table_name": f"{self.name} EVENT PRODS CONVERSION"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name} EVENT PRODS \
                        CONVERSION"] = r.json()['id']

    def instance_products_dataset(self):
        """
        Instance as physical dataset the products of
        the store
        """
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "druid",
                  "table_name": f"{self.name} PRODUCTS"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name} PRODUCTS"] = r.json()['id']

    def create_general_resultas_per_category_dataset(self) -> None:
        """
        Create a virtual dataset that calculate the general metric
        for each category
        """
        sql_query = f"SELECT\
                      tb1.category as \"Categoria\",\
                      \"UnidadesVendidas\" as \"Unidades vendidas\",\
                      total as \"Total ingresos por venta\",\
                      \"IngresosConBusqueda\" * 1.0 / total as\
                       \"Ingresos con búsqueda\",\
                      total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -1), 'P1M'))\
                                    as \"%participación\",\
                      total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -2), 'P1M'))\
                                    as \"%participación mes anterior\"\
                                    \
                      FROM \
                        (SELECT\
                          category,\
                          sum(\"stats.pconv\") as \"IngresosConBusqueda\"\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -1), 'P1M')\
                              and \"stats.vclickconv\" >= 1\
                          GROUP BY 1) as tb1 \
                          LEFT JOIN\
                      (SELECT\
                          category,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -1), 'P1M')\
                          GROUP BY 1) as tb2 \
                          ON tb1.category = tb2.category\
                          LEFT JOIN \
                          (SELECT\
                          category,\
                          sum(\"stats.pconv\") as total2\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                               'P1M', -2), 'P1M')\
                          GROUP BY 1) as tb3\
                          ON tb3.category = tb1.category\
                          GROUP BY 1, 2, 3, 4, 5, 6\
                          ORDER BY total DESC"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"General results per category {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["General results per category"] = r.json()['id']

    def create_change_participation_category_dataset(self) -> None:
        """
        Create a virtual dataset that calculates the variation of participation
        in incomes of each category in a month
        """
        sql_query = f"SELECT\
                      tb2.category as \"Categoria\",\
                      tb3.\"UnidadesVendidas\" as\
                         \"Unidades vendidas mes anterior\",\
                      total2 as \"Total ingresos por venta mes anterior\",\
                      total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                        'P1M', -2), 'P1M'))\
                                    as \"%participación mes anterior\",\
                      tb2.\"UnidadesVendidas\" as \"Unidades vendidas\",\
                      total as \"Total ingresos por venta\",\
                      total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -1), 'P1M'))\
                                    as \"%participación\",\
                      (total * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') =\
                                       TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -1), 'P1M'))) - \
                                          (total2 * 1.0 / (SELECT \
                                    sum(\"stats.pconv\")\
                                    FROM \"{self.name} PRODUCTS\"\
                                    where TIME_FLOOR(__time, 'P1M') = \
                                      TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP,\
                                         'P1M', -2), 'P1M')))\
                                    as \"Diferencia de participación\"\
                      FROM \
                      (SELECT\
                          category,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                               -1), 'P1M')\
                          GROUP BY 1) as tb2\
                          LEFT JOIN \
                          (SELECT\
                          category,\
                          sum(\"stats.nconv\") as \
                              \"UnidadesVendidas\",\
                          sum(\"stats.pconv\") as total2\
                          FROM \"{self.name} PRODUCTS\"\
                          where TIME_FLOOR(__time, 'P1M') =\
                             TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M',\
                               -2), 'P1M')\
                          GROUP BY 1) as tb3\
                          ON tb3.category = tb2.category\
                          GROUP BY 1, 2, 3, 4, 5, 6, 7, 8"
        payload = {
                  "database": 2,
                  "external_url": "",
                  "is_managed_externally": "false",
                  "owners": [],
                  "schema": "druid",
                  "sql": sql_query,
                  "table_name": f"Change participation category {self.name}"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets["Change participation category"] = r.json()['id']

    def instance_search_groups_dataset(self):
        """
        Instance as physical dataset the pre-calculated search
        groups
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_search_group"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_search_group"] = r.json()['id']

    def instance_query_groups_dataset(self):
        """
        Instance as physical dataset the pre-calculated query
        groups
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_group_query"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_group_query"] = r.json()['id']

    def instance_rise_table_dataset(self):
        """
        Instance as physical dataset the pre-calculated rise
        search tendency in the table format
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_rise_table"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_rise_table"] = r.json()['id']

    def instance_fall_table_dataset(self):
        """
        Instance as physical dataset the pre-calculated fall
        search tendency in the table format
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_fall_table"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_fall_table"] = r.json()['id']

    def instance_rise_chart_dataset(self):
        """
        Instance as physical dataset the pre-calculated rise
        search tendency in the chart format
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_rise_chart"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_rise_chart"] = r.json()['id']

    def instance_fall_chart_dataset(self):
        """
        Instance as physical dataset the pre-calculated fall
        search tendency in the chart format
        """
        payload = {
                  "database": 4,
                  "external_url": "",
                  "is_managed_externally": "False",
                  "owners": [],
                  "schema": "public",
                  "table_name": f"{self.name}_fall_chart"}
        r = requests.post(self.base_url + self.dataset_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.datasets[f"{self.name}_fall_chart"] = r.json()['id']

    def create_all(self) -> None:
        """
        Create all the datasets available in the current class
        """
        self.create_general_results_dataset()
        self.create_searches_group_by_day_dataset()
        self.create_incomes_group_by_day_dataset()
        self.create_incomes_per_searches_dataset()
        self.create_zero_hit_dataset()
        self.create_zero_hit_restock_dataset()
        self.create_zero_hit_new_dataset()
        self.create_zero_hits_old_dataset()
        self.create_top_ten_products_dataset()
        self.create_change_incomes_per_products_dataset()
        self.create_general_resultas_per_brand_dataset()
        self.create_general_resultas_per_category_dataset()
        self.create_change_participation_brand_dataset()
        self.create_change_participation_category_dataset()
        self.create_participation_per_brand_dataset()
        self.create_brands_bought_together_dataset()
        self.create_participation_per_category_dataset()
        self.create_categories_bought_together_dataset()
        self.create_products_bought_together_dataset()
        self.instance_event_conversion_dataset()
        self.instance_search_dataset()
        self.instance_event_prod_conversion_dataset()
        self.instance_products_dataset()
        self.instance_search_groups_dataset()
        self.instance_query_groups_dataset()
        self.instance_fall_chart_dataset()
        self.instance_fall_table_dataset()
        self.instance_rise_chart_dataset()
        self.instance_rise_table_dataset()
