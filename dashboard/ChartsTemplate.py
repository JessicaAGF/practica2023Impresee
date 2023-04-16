import requests
import json
import datetime as dt
import time
import pandas as pd


class ChartsTemplate(object):
    """
    This class allows the creation of a series of graphs which will be
    added to the assigned dashboard. For this, it uses previously
    created datasets.
    """

    def __init__(self, shop_name: str, token: str, datasets: dict,
                 dashboard_id):
        self.base_url = 'http://localhost:8088'
        self.chart_url = '/api/v1/chart'
        self.headers_auth = {
            'Authorization': 'Bearer ' + token
        }
        self.name = shop_name
        self.charts = {}
        self.datasets = datasets
        self.dashboard_id = dashboard_id

    def get_charts_id(self):
        """
        Returns a dictionary containing the id of each chart associated
        with its name
        """
        return self.charts

    def create_general_results_table(self):
        """
        Create a table that shows the general metrics for the respective
        shop, such as incomes, visitors, search participation, orders
        and sell units.
        """
        params = {
                    "adhoc_filters": [],
                    "align_pn": False,
                    "all_columns": [],
                    "allow_rearrange_columns": False,
                    "color_pn": False,
                    "column_config": {
                        "Dinero en ventas": {
                            "d3NumberFormat": "$,.0f"
                            },
                        "Dinero en ventas desde el buscador": {
                            "d3NumberFormat": "$,.0f"
                            },
                        "Fecha": {
                            "columnWidth": 70
                            },
                        "Participación del buscador": {
                            "d3NumberFormat": ".2%",
                            "d3SmallNumberFormat": ".2%",
                            "showCellBars": False
                            },
                        "Visitantes que usan el buscador": {
                            "d3NumberFormat": ".2%",
                            "d3SmallNumberFormat": ".2%",
                            "showCellBars": False
                            }
                    },
                    "conditional_formatting": [],
                    "extra_form_data": {},
                    "granularity_sqla": "Fecha",
                    "groupby": [
                        "Fecha",
                        "Búsquedas del periodo",
                        "Órdenes de compra",
                        "Unidades Vendidas",
                        "Dinero en ventas",
                        "Dinero en ventas desde el buscador",
                        "Participación del buscador",
                        "Visitantes que usan el buscador"
                    ],
                    "include_search": False,
                    "include_time": False,
                    "order_by_cols": [],
                    "order_desc": True,
                    "percent_metrics": [],
                    "query_mode": "aggregate",
                    "row_limit": 10000,
                    "server_page_length": 10,
                    "show_cell_bars": False,
                    "show_totals": False,
                    "table_timestamp_format": "smart_date",
                    "time_grain_sqla": "P1M",
                    "time_range": "No filter",
                    "viz_type": "table"
                    }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["General Results"],
                    "datasource_name": f"General Results {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Resultados generales Históricos",
                    "viz_type": "table"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---charts")
        print(r)
        print(r.text)
        self.charts["General results"] = r.json()['id']

    def create_monthly_comparator_chart(self):
        """
        Create a chart that showss a resume of some generals metrics
        """
        params = {
                  "adhoc_filters": [],
                  "color_scheme": "d3Category20",
                  "column_config": {
                    "Búsquedas del periodo": {
                      "radarMetricMaxValue": "null"
                    },
                    "Dinero en ventas": {
                      "radarMetricMaxValue": "null"
                    },
                    "Dinero en ventas desde el buscador": {
                      "radarMetricMaxValue": "null"
                    },
                    "Unidades Vendidas": {
                      "radarMetricMaxValue": "null"
                    },
                    "Órdenes de compra": {
                      "radarMetricMaxValue": "null"
                    }
                  },
                  "date_format": "%m/%Y",
                  "extra_form_data": {},
                  "granularity_sqla": "Fecha",
                  "groupby": [
                    "Fecha"
                  ],
                  "is_circle": False,
                  "label_position": "bottom",
                  "label_type": "value",
                  "legendMargin": 600,
                  "legendOrientation": "right",
                  "legendType": "scroll",
                  "metrics": [
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Búsquedas del periodo",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "INT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Búsquedas del periodo",
                      "optionName": "metric_9fbwzamrteo_1ys2fbt929s",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Órdenes de compra",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "INT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Órdenes de compra",
                      "optionName": "metric_256upwbbolo_ouz62yg25ce",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Unidades Vendidas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Unidades Vendidas",
                      "optionName": "metric_vmveho8rg29_6s2pfs441gm",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Dinero en ventas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Dinero en ventas",
                      "optionName": "metric_szx9caeh9gh_4qtnzvfvi3w",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Dinero en ventas desde el buscador",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Dinero en ventas desde el buscador",
                      "optionName": "metric_hunf3e2jgkw_aqslsxhllyr",
                      "sqlExpression": "null"
                    }
                  ],
                  "number_format": "SMART_NUMBER",
                  "row_limit": 10,
                  "show_labels": False,
                  "show_legend": True,
                  "time_range": "No filter",
                  "timeseries_limit_metric": {
                    "aggregate": "COUNT",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Fecha",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": True,
                      "python_date_format": "null",
                      "type": "STRING",
                      "type_generic": 2,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "COUNT(Fecha)",
                    "optionName": "metric_wyl1ayzyer_kopl1be2gqs",
                    "sqlExpression": "null"
                  },
                  "viz_type": "radar"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["General Results"],
                    "datasource_name": f"General Results {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Comparador mensual",
                    "viz_type": "radar"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Monthly comparator"] = r.json()['id']

    def create_period_selector_generl_results(self):
        """
        Create a time filter for the general results and monthly comparator
        slides
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "Fecha",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["General Results"],
                    "datasource_name": f"General Results {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo resultados generales",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector general results"] = r.json()['id']

    def create_daily_searches_chart(self):
        """
        Create a chart that shows all the searches per day considering
        all the data available
        """
        name = f"{self.name} SEARCH"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "1",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_7budknkjtz2_mta5mpt0ydj",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "==",
                      "operatorId": "EQUALS",
                      "sqlExpression": "null",
                      "subject": "qfinal"
                    }
                  ],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [],
                  "legendMargin": "null",
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "markerEnabled": False,
                  "markerSize": 6,
                  "metrics": [
                    {
                      "aggregate": "null",
                      "column": "null",
                      "expressionType": "SQL",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Cantidad de búsquedas",
                      "optionName": "metric_ic5fzmt0bo_k9ph3ulf93",
                      "sqlExpression": "COUNT(*)"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "rich_tooltip": True,
                  "row_limit": 50000,
                  "show_legend": False,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "x_axis_time_format": "%m/%Y",
                  "x_axis_title": "Fecha",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "SMART_NUMBER",
                  "y_axis_title": "Cantidad de búsquedas",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Busquedas Diarias Históricas",
                    "viz_type": "echarts_timeseries_smooth"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        self.charts["Daily Searches"] = r.json()['id']

    def create_period_selector_daily_searches(self):
        """
        Create a time filter for the daily searches
        """
        name = f"{self.name} SEARCH"
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "Fecha",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo búsquedas diarias",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector daily searches"] = r.json()['id']

    def create_daily_conversions_chart(self):
        """
        Create a chart that shows all the conversions per day considering
        all the data available
        """
        name = f"{self.name} EVENT CONVERSION"
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "contributionMode": "null",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [],
                  "legendMargin": "null",
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "markerEnabled": True,
                  "markerSize": 2,
                  "metrics": [
                    {
                      "aggregate": "null",
                      "column": "null",
                      "expressionType": "SQL",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Cantidad de conversiones",
                      "optionName": "metric_ic5fzmt0bo_k9ph3ulf93",
                      "sqlExpression": "COUNT(*)"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "rich_tooltip": True,
                  "row_limit": 50000,
                  "show_legend": False,
                  "show_value": False,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "x_axis_time_format": "%m/%Y",
                  "x_axis_title": "Fecha",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "SMART_NUMBER",
                  "y_axis_title": "Conversiones",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params":   json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Conversiones diarias historicas",
                    "viz_type": "echarts_timeseries_smooth"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Daily Conversions"] = r.json()['id']

    def create_period_selector_daily_conversions(self):
        """
        Create a time filter for the daily conversions
        """
        name = f"{self.name} EVENT CONVERSION"
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "Fecha",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector daily conversions"] = r.json()['id']

    def create_last_3_month_daily_searches_chart(self):
        """
        Create a chart that shows comparatively the searches per day
        considering all the data in the last 3 months
        """
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "Fecha"
                  ],
                  "legendMargin": 20,
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "markerSize": 6,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Cantidad de búsquedas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "INT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": False,
                      "isNew": False,
                      "label": "SUM(Cantidad de búsquedas)",
                      "optionName": "metric_hlq72vvdm3a_y27efevrsn",
                      "sqlExpression": "null"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "rich_tooltip": True,
                  "row_limit": 1000,
                  "show_legend": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "x_axis_time_format": "%d",
                  "x_axis_title": "Día",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "SMART_NUMBER",
                  "y_axis_title": "Cantidad de búsquedas",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Searches group by day"],
                    "datasource_name": f"Searches group by day {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Comparativa mensual de búsquedas diarias",
                    "viz_type": "echarts_timeseries_smooth"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Daily searches in last 3 months"] = r.json()['id']

    def create_month_selector_grouped_daily_searches(self):
        """
        Create a time filter for the grouped daily searches
        """
        local_time = time.localtime()
        actual_date = dt.date(local_time.tm_year, local_time.tm_mon, 1)
        one_month_before = actual_date - pd.DateOffset(months=1)
        two_month_before = actual_date - pd.DateOffset(months=2)
        default = (str(two_month_before.year) + '-' +
                   str(two_month_before.month)
                   + ';' + str(one_month_before.year) + '-' +
                   str(one_month_before.month)
                   + ';' + str(actual_date.year) + '-' +
                   str(actual_date.month))
        params = {
                  "adhoc_filters": [],
                  "date_filter": False,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "Fecha",
                      "defaultValue": default,
                      "key": "6rJ3ke_tA",
                      "multiple": True,
                      "searchAllOptions": False
                    }
                  ],
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Searches group by day"],
                    "datasource_name": f"Searches group by day {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de meses búsquedas",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Month selector grouped daily searches"] = r.json()['id']

    def create_last_3_month_daily_incomes_chart(self):
        """
        Create a chart that shows comparatively the incomes per day
        considering all the data in the last 3 months
        """
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "Fecha"
                  ],
                  "legendMargin": 20,
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "markerEnabled": False,
                  "markerSize": 6,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Ingreso mes actual",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Ingresos",
                      "optionName": "metric_w6am5wts48_803ox4kcsv6",
                      "sqlExpression": "null"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "rich_tooltip": True,
                  "row_limit": 1000,
                  "show_legend": True,
                  "show_value": False,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "x_axis_time_format": "%d",
                  "x_axis_title": "Día",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "SMART_NUMBER",
                  "y_axis_title": "Ingreso",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Incomes group by day"],
                    "datasource_name": f"Incomes group by day {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Comparativa mensual de ingresos diarios",
                    "viz_type": "echarts_timeseries_smooth"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Incomes per day in last 3 months"] = r.json()['id']

    def create_month_selector_grouped_daily_incomes(self):
        """
        Create a time filter for the grouped daily incomes
        """
        local_time = time.localtime()
        actual_date = dt.date(local_time.tm_year, local_time.tm_mon, 1)
        one_month_before = actual_date - pd.DateOffset(months=1)
        two_month_before = actual_date - pd.DateOffset(months=2)
        default = (str(two_month_before.year) + '-' +
                   str(two_month_before.month)
                   + ';' + str(one_month_before.year) + '-' +
                   str(one_month_before.month)
                   + ';' + str(actual_date.year) + '-' +
                   str(actual_date.month))
        params = {
                  "adhoc_filters": [],
                  "date_filter": False,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "Fecha",
                      "defaultValue": default,
                      "key": "6rJ3ke_tA",
                      "multiple": True,
                      "searchAllOptions": False
                    }
                  ],
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Incomes group by day"],
                    "datasource_name": f"Incomes group by day {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de meses ingresos",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Month selector grouped daily incomes"] = r.json()['id']

    def create_incomes_per_searches_chart(self):
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "Fecha",
                  "groupby": [],
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "metrics": [
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Dinero en ventas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "id": 1281,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Dinero en ventas",
                      "optionName": "metric_4bxnfbln8u4_yvzj3r6eli",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Dinero en ventas desde el buscador",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Dinero en ventas desde el buscador",
                      "optionName": "metric_v89j8r9wnn_g1fodgakf0h",
                      "sqlExpression": "null"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "orientation": "vertical",
                  "percentage_threshold": 0,
                  "rich_tooltip": True,
                  "row_limit": 1000,
                  "show_legend": True,
                  "show_value": True,
                  "stack": False,
                  "time_grain_sqla": "P1M",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_bar",
                  "x_axis_time_format": "%m/%Y",
                  "x_axis_title_margin": 15,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "SMART_NUMBER",
                  "y_axis_title_margin": 15,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Incomes per searches"],
                    "datasource_name": f"Incomes per searches {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Ingresos por búsquedas historicos",
                    "viz_type": "echarts_timeseries_bar"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Incomes per searches"] = r.json()['id']

    def create_period_selector_incomes_per_searches(self):
        """
        Create a time filter for the incomes per searches
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "Fecha",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Incomes per searches"],
                    "datasource_name": f"Incomes per searches {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": ("Selección de periodo ingresos "
                                   + "por búsquedas"),
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector incomes per searches"] = r.json()['id']

    def create_zero_hits_table(self):
        """
        Create a table that shows all the zero hits considering
        all the data available
        """
        name = f"{self.name} SEARCH"
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Query",
                    "Total"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Total": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": [
                    "Query",
                    "Total"
                  ],
                  "include_search": True,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Total\", False]"
                  ],
                  "order_desc": True,
                  "page_length": 0,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": 1000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Zero hits historicos",
                    "viz_type": "table"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Zero hits"] = r.json()['id']

    def create_period_selector_zero_hits(self):
        """
        Create a time filter for the zero hits
        """
        name = f"{self.name} SEARCH"
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo zero hits",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector zero hits"] = r.json()['id']

    def create_zero_hits_restock_table(self):
        """
        Create a table that shows the zero hits that correspond
        to a product that must be stocked
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Query",
                    "Total"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Total": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Total\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": 1000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Zero hits restock"],
                    "datasource_name": f"Zero hits restock {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Restock mes actual",
                    "viz_type": "table"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Zero hits restock"] = r.json()['id']

    def create_zero_hits_new_table(self):
        """
        Create a table that shows the zero hits that for the first
        time has no results
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Query",
                    "Total"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Total": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "groupby": [
                    "Query"
                  ],
                  "include_search": True,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Total",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "INT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Total",
                      "optionName": "metric_fzwku831oo_l45hfkguufk",
                      "sqlExpression": "null"
                    }
                  ],
                  "order_by_cols": [],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "aggregate",
                  "row_limit": 1000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "timeseries_limit_metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "INT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(Total)",
                    "optionName": "metric_fs4dyi998y_n5lhqsya5s",
                    "sqlExpression": "null"
                  },
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Zero hits new"],
                    "datasource_name": f"Zero hits new {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Zero hits nuevos mes actual",
                    "viz_type": "table"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["New zero hits"] = r.json()['id']

    def create_zero_hits_old_table(self):
        """
        Create a table that zero hits present in the last 3
        months but no longer appearing
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Query",
                    "Total"
                  ],
                  "allow_rearrange_columns": False,
                  "color_pn": True,
                  "column_config": {
                    "Total": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "granularity_sqla": "null",
                  "groupby": [
                    "Query"
                  ],
                  "include_search": True,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Total",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "INT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Total",
                      "optionName": "metric_tglhm5b92u_bnaudunowz6",
                      "sqlExpression": "null"
                    }
                  ],
                  "order_by_cols": [
                    "[\"Total\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "aggregate",
                  "row_limit": 1000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "timeseries_limit_metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "INT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(Total)",
                    "optionName": "metric_64rhferozji_jvkkd0it8tc",
                    "sqlExpression": "null"
                  },
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Zero hits old"],
                    "datasource_name": f"Zero hits old {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Zero hits en el periodo de 3 meses atras",
                    "viz_type": "table"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["New zero old"] = r.json()['id']

    def create_brands_bought_together_chart(self):
        """
        Create a chart that shows the relation between brands that
        are bought in the same conversion
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_vuptx0dyyx_tedjspmbmic",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "a"
                    },
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_1xcz8geb3vs_vt73te23nt",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "b"
                    }
                  ],
                  "color_scheme": "d3Category20",
                  "columns": "b",
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": "a",
                  "metric": {
                    "aggregate": "MAX",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "EXPR$2",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "INT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "MAX(EXPR$2)",
                    "optionName": "metric_dwpkfj8dmk_ow7c8wnfd9",
                    "sqlExpression": "null"
                  },
                  "row_limit": 1000,
                  "time_range": "No filter",
                  "viz_type": "chord",
                  "y_axis_format": "SMART_NUMBER"
                  }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Brands bought together"],
                   "datasource_name": f"Brands bought together {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Marcas historicamente compradas en conjunto",
                   "viz_type": "chord"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Brands bought together"] = r.json()['id']

    def create_period_selector_brands_bought_together(self):
        """
        Create a purchase quantity and time filter for the
        brands bought together chart
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "EXPR$3",
                      "label": "Cantidad mínima de compras",
                      "multiple": True,
                      "searchAllOptions": True
                    }
                  ],
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Brands bought together"],
                    "datasource_name": f"Brands bought together {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": ("Selección de cantidad mínima de compras "
                                   + "y de periodo para marcas"),
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector brands bought together"] = r.json()['id']

    def create_categories_bought_together_chart(self):
        """
        Create a chart that shows the relation between categories that
        are bought in the same conversion
        """
        name = "Categories bought together"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_q7anr8ljnho_26bi5iz05x9",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "a"
                    },
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_70v4q1itxig_thl4jdwtsco",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "b"
                    },
                    {
                      "clause": "WHERE",
                      "comparator": "3",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_6qmwzkmvdix_894db0wix58",
                      "isExtra": False,
                      "isNew": False,
                      "operator": ">=",
                      "operatorId": "GREATER_THAN_OR_EQUAL",
                      "sqlExpression": "null",
                      "subject": "EXPR$2"
                    }
                  ],
                  "color_scheme": "d3Category20",
                  "columns": "b",
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": "a",
                  "metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "EXPR$2",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "INT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(EXPR$2)",
                    "optionName": "metric_1v6jght5b7t_ud4vtgxeqda",
                    "sqlExpression": "null"
                  },
                  "row_limit": 1000,
                  "sort_by_metric": True,
                  "time_range": "No filter",
                  "viz_type": "chord",
                  "y_axis_format": "SMART_NUMBER"
                 }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"name {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Categorías historicamente compradas "
                                 + "en conjunto",
                   "viz_type": "chord"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Categories bought together"] = r.json()['id']

    def create_period_selector_categories_bought_together(self):
        """
        Create a purchase quantity and time filter for the
        categories bought together chart
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "EXPR$3",
                      "label": "Cantidad mínima de compras",
                      "multiple": True,
                      "searchAllOptions": True
                    }
                  ],
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Categories bought "
                                                   + "together"],
                    "datasource_name": ("Categories bought together "
                                        + f"{self.name}"),
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": ("Selección de cantidad mínima de compras "
                                   + "y de periodo para categorias"),
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector categories bought together"] = (
                    r.json()['id'])

    def create_categories_behaviour_table(self):
        """
        Create a table that shows the performance of each category
        across the time
        """
        name = f"{self.name} PRODUCTS"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_9lkdvzocgkk_4iypm910wyx",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "brand"
                    }
                  ],
                  "column_collection": [
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "time",
                      "comparisonType": "value",
                      "d3format": "$,.0f",
                      "dateFormat": "",
                      "height": "",
                      "key": "wP8HxFAT2",
                      "label": "Ingresos",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "contrib",
                      "comparisonType": "",
                      "d3format": ".2%",
                      "dateFormat": "",
                      "height": "",
                      "key": "3fIwqWWX-",
                      "label": "% Participación",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        -0.1,
                        0.1
                      ],
                      "colType": "time",
                      "comparisonType": "perc_change",
                      "d3format": ".0%",
                      "dateFormat": "",
                      "height": "",
                      "key": "W9uoAljS6",
                      "label": "Respecto a mes anterior",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 1,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "spark",
                      "comparisonType": "",
                      "d3format": "$,.0f",
                      "dateFormat": "%d/%m/%Y",
                      "height": "",
                      "key": "aTIKoaPyE",
                      "label": "Evolución historica",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    }
                  ],
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": [
                    "category"
                  ],
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "stats.pconv",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "STRING",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": False,
                      "isNew": False,
                      "label": "SUM(stats.pconv)",
                      "optionName": "metric_f84ahi731dt_rocjs1bymce",
                      "sqlExpression": "null"
                    }
                  ],
                  "row_limit": 10000,
                  "time_grain_sqla": "P1M",
                  "time_range": "previous calendar year",
                  "viz_type": "time_table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": name,
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Comportamiento categorias",
                   "viz_type": "time_table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Categories behaviour"] = r.json()['id']

    def create_category_participation_chart(self):
        """
        Create a chart that shows the contribution of incomes in the
        current month of each category.
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SQL",
                      "filterOptionName": "filter_ni03kcy6bj_j27k33x4wfj",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "null",
                      "sqlExpression": "LENGTH(category) <= 30",
                      "subject": "null"
                    }
                  ],
                  "color_scheme": "d3Category20",
                  "date_format": "smart_date",
                  "donut": False,
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": [
                    "category"
                  ],
                  "innerRadius": 30,
                  "label_line": True,
                  "label_type": "key",
                  "labels_outside": True,
                  "legendMargin": 200,
                  "legendOrientation": "right",
                  "legendType": "scroll",
                  "metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(total)",
                    "optionName": "metric_ig78outo5h8_ry81knibjw",
                    "sqlExpression": "null"
                  },
                  "number_format": "$,.2f",
                  "outerRadius": 80,
                  "row_limit": 250,
                  "show_labels": True,
                  "show_labels_threshold": 5,
                  "show_legend": True,
                  "show_total": True,
                  "sort_by_metric": True,
                  "time_range": "No filter",
                  "viz_type": "pie"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Participation "
                                                  + "per category"],
                   "datasource_name": "Participation "
                                      + f"per category {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Participación historica de categorias",
                   "viz_type": "pie"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Participation per category"] = r.json()['id']

    def create_total_incomes_per_category(self):
        """
        Create a chart that shows the total sum of incomes of the
        current category selected
        """
        params = {
                  "adhoc_filters": [],
                  "extra_form_data": {},
                  "header_font_size": 0.3,
                  "metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(total)",
                    "optionName": "metric_47q9n7u9qwd_0o7yzhn28in",
                    "sqlExpression": "null"
                  },
                  "subheader_font_size": 0.15,
                  "time_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "big_number_total",
                  "y_axis_format": "$,.0f"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Participation per "
                                                  + "category"],
                   "datasource_name": ("Participation per category "
                                       + f"{self.name}"),
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Total ingresos historicos",
                   "viz_type": "big_number_total"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Total incomes categories"] = r.json()['id']

    def create_period_selector_participation_per_category(self):
        """
        Create a brand and time filter for the participation per category
        charts
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "category",
                      "label": "Categoria",
                      "multiple": True,
                      "searchAllOptions": False
                    }
                  ],
                  "granularity_sqla": "__time",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Participation per "
                                                   + "category"],
                    "datasource_name": "Participation per category "
                                       + f"{self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de categorias y periodo",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector participation per category"] = (
                    r.json()['id'])

    def create_brand_participation_chart(self):
        """
        Create a chart that shows the contribution of incomes in the
        current month of each brand.
        """
        params = {
                  "adhoc_filters": [],
                  "color_scheme": "d3Category20",
                  "date_format": "smart_date",
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": [
                    "brand"
                  ],
                  "innerRadius": 30,
                  "label_line": True,
                  "label_type": "key",
                  "labels_outside": True,
                  "legendMargin": "",
                  "legendOrientation": "right",
                  "legendType": "scroll",
                  "metric": {
                    "aggregate": "MAX",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "MAX(total)",
                    "optionName": "metric_bz1j7wb7wd_i2bpupmomrk",
                    "sqlExpression": "null"
                  },
                  "number_format": "$,.2f",
                  "outerRadius": 78,
                  "row_limit": 100,
                  "show_labels": True,
                  "show_labels_threshold": 5,
                  "show_legend": True,
                  "show_total": False,
                  "sort_by_metric": True,
                  "time_range": "No filter",
                  "viz_type": "pie"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Participation per brand"],
                   "datasource_name": f"Participation per brand{self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Participación historica de marcas",
                   "viz_type": "pie"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Participation per brand"] = r.json()['id']

    def create_total_incomes_per_brand(self):
        """
        Create a chart that shows the total sum of incomes of the
        current brands selected
        """
        params = {
                  "adhoc_filters": [],
                  "extra_form_data": {},
                  "header_font_size": 0.3,
                  "metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(total)",
                    "optionName": "metric_47q9n7u9qwd_0o7yzhn28in",
                    "sqlExpression": "null"
                  },
                  "subheader_font_size": 0.15,
                  "time_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "big_number_total",
                  "y_axis_format": "$,.0f"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Participation per brand"],
                   "datasource_name": f"Participation per brand {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Total ingresos historicos",
                   "viz_type": "big_number_total"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Total incomes brands"] = r.json()['id']

    def create_period_selector_participation_per_brand(self):
        """
        Create a brand and time filter for the participation per brand
        charts
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "brand",
                      "key": "hvcBiVnga",
                      "label": "Marca",
                      "multiple": True,
                      "searchAllOptions": False
                    }
                  ],
                  "granularity_sqla": "__time",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Participation per brand"],
                    "datasource_name": f"Participation per brand {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de marcas y periodo",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector participation per brand"] = r.json()['id']

    def create_brands_behaviour_table(self):
        """
        Create a rable that shows the performance of each brand
        across the time
        """
        name = f"{self.name} PRODUCTS"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_9lkdvzocgkk_4iypm910wyx",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "brand"
                    }
                  ],
                  "column_collection": [
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "time",
                      "comparisonType": "value",
                      "d3format": "$,.0f",
                      "dateFormat": "",
                      "height": "",
                      "key": "wP8HxFAT2",
                      "label": "Ingresos",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "contrib",
                      "comparisonType": "",
                      "d3format": ".2%",
                      "dateFormat": "",
                      "height": "",
                      "key": "3fIwqWWX-",
                      "label": "% Participación",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        -0.1,
                        0.1
                      ],
                      "colType": "time",
                      "comparisonType": "perc_change",
                      "d3format": ".0%",
                      "dateFormat": "",
                      "height": "",
                      "key": "W9uoAljS6",
                      "label": "Respecto a mes anterior",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 1,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    },
                    {
                      "bounds": [
                        "null",
                        "null"
                      ],
                      "colType": "spark",
                      "comparisonType": "",
                      "d3format": "$,.0f",
                      "dateFormat": "%d/%m/%Y",
                      "height": "",
                      "key": "aTIKoaPyE",
                      "label": "Evolución historica",
                      "popoverVisible": True,
                      "showYAxis": False,
                      "timeLag": 0,
                      "timeRatio": "",
                      "tooltip": "",
                      "width": "",
                      "yAxisBounds": [
                        "null",
                        "null"
                      ]
                    }
                  ],
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": [
                    "brand"
                  ],
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "stats.pconv",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "STRING",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": False,
                      "isNew": False,
                      "label": "SUM(stats.pconv)",
                      "optionName": "metric_f84ahi731dt_rocjs1bymce",
                      "sqlExpression": "null"
                    }
                  ],
                  "row_limit": 10000,
                  "time_grain_sqla": "P1M",
                  "time_range": "previous calendar year",
                  "viz_type": "time_table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": name,
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Comportamiento de marcas",
                   "viz_type": "time_table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Brands behaviour"] = r.json()['id']

    def create_brand_participation_rise_table(self):
        """
        Create a table that shows the top 6 brands that increase their
        participation in the last month
        """
        name = "Change participation brand"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_76jnzsi2ao_tbxqmujs9qq",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "Marca"
                    }
                  ],
                  "all_columns": [
                    "Marca",
                    "Unidades vendidas mes anterior",
                    "Total ingresos por venta mes anterior",
                    "%participación mes anterior",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "%participación",
                    "Diferencia de participación"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "%participación": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "%participación mes anterior": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "Diferencia de participación": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "Total ingresos por venta mes anterior": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#ACE1C4",
                      "column": "Diferencia de participación",
                      "operator": "≥",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Diferencia de participación\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "5",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Marcas con mayor alza en participación",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Brand participation rise"] = r.json()['id']

    def create_brand_participation_fall_table(self):
        """
        Create a table that shows the top 6 brands that decrease their
        participation in the last month
        """
        name = "Change participation brand"
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_jmmshxaulbi_wwytenn5x5",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "Marca"
                    }
                  ],
                  "all_columns": [
                    "Marca",
                    "Unidades vendidas mes anterior",
                    "Total ingresos por venta mes anterior",
                    "%participación mes anterior",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "%participación",
                    "Diferencia de participación"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "%participación": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "%participación mes anterior": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "Diferencia de participación": {
                      "d3NumberFormat": ".2%",
                      "d3SmallNumberFormat": ".2%"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    },
                    "Total ingresos por venta mes anterior": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#EFA1AA",
                      "column": "Diferencia de participación",
                      "operator": "<",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "order_by_cols": [
                    "[\"Diferencia de participación\", True]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "5",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Marcas con mayor baja en participación",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Brand participation fall"] = r.json()['id']

    def create_general_results_by_brand_table(self):
        """
        Create a table that shows general results for each brand
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_e24uyfs53o_n93n1wsr4nc",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "Marca"
                    }
                  ],
                  "all_columns": [
                    "Marca",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "Ingresos con búsqueda",
                    "%participación",
                    "%participación mes anterior"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "%participación": {
                      "d3NumberFormat": ".2%"
                    },
                    "%participación mes anterior": {
                      "d3NumberFormat": ".2%"
                    },
                    "Ingresos con búsqueda": {
                      "d3NumberFormat": ".2%"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Total ingresos por venta\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "26",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["General results per brand"],
                   "datasource_name": f"General results per brand {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Resultados generales por marca",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["General results per brand"] = r.json()['id']

    def create_product_rise_table(self):
        """
        Create a table that shows the top products that increase their
        incomes in the last month
        """
        name = "Change incomes per product"
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Producto",
                    "Marca",
                    "Unidades vendidas mes anterior",
                    "Total ingresos por venta mes anterior",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "Diferencia ($)"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Diferencia ($)": {
                      "colorPositiveNegative": True,
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    },
                    "Total ingresos por venta mes anterior": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#ACE1C4",
                      "column": "Diferencia ($)",
                      "operator": "≥",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": False,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Diferencia ($)\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "6",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Productos con mayor alza en ingresos",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Product rise per month"] = r.json()['id']

    def create_product_fall_table(self):
        """
        Create a table that shows the top products that decrease their
        incomes in the last month
        """
        name = "Change incomes per product"
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Producto",
                    "Marca",
                    "Unidades vendidas mes anterior",
                    "Total ingresos por venta mes anterior",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "Diferencia ($)"
                  ],
                  "allow_rearrange_columns": True,
                  "color_pn": True,
                  "column_config": {
                    "Diferencia ($)": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    },
                    "Total ingresos por venta mes anterior": {
                      "d3NumberFormat": "$,.0f",
                      "d3SmallNumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#EFA1AA",
                      "column": "Diferencia ($)",
                      "operator": "<",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "order_by_cols": [
                    "[\"Diferencia ($)\", True]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "6",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": f"{name} {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Productos con mayor baja en ingresos",
                    "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Product fall per month"] = r.json()['id']

    def create_top_10_products_table(self):
        """
        Create a table that shows the top products with greates incomes
        in the current month
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Producto",
                    "Marca",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "Ingresos con búsqueda"
                  ],
                  "color_pn": False,
                  "column_config": {
                    "Ingresos con búsqueda": {
                      "d3NumberFormat": ".2%"
                    },
                    "Marca": {
                      "horizontalAlign": "left"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#FDE380",
                      "column": "Ingresos con búsqueda",
                      "operator": "=",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Total ingresos por venta\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": 10,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Top ten products"],
                    "datasource_name": f"Top ten products {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Top 10 productos con mayores ingresos",
                    "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Top 10 products with greatest incomes"] = r.json()['id']

    def create_general_results_per_category_table(self):
        """
        Create a table that shows general results for each brand
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "null",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_e24uyfs53o_n93n1wsr4nc",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "IS NOT NULL",
                      "operatorId": "IS_NOT_NULL",
                      "sqlExpression": "null",
                      "subject": "Marca"
                    }
                  ],
                  "all_columns": [
                    "Categoria",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "Ingresos con búsqueda",
                    "%participación",
                    "%participación mes anterior"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "%participación": {
                      "d3NumberFormat": ".2%"
                    },
                    "%participación mes anterior": {
                      "d3NumberFormat": ".2%"
                    },
                    "Ingresos con búsqueda": {
                      "d3NumberFormat": ".2%"
                    },
                    "Total ingresos por venta": {
                      "d3NumberFormat": "$,.0f"
                    }
                  },
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Total ingresos por venta\", False]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "26",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        name = "General results per category"
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Resultados generales por categoria",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["General results per category"] = r.json()['id']

    def create_category_participation_rise_table(self):
        """
        Create a table that shows the top 6 categories that increase their
        participation in the last month
        """
        params = {
                  "params": {
                    "adhoc_filters": [
                      {
                        "clause": "WHERE",
                        "comparator": "null",
                        "expressionType": "SIMPLE",
                        "filterOptionName": "filter_75taxj8rhn8_xsoq98x9tz",
                        "isExtra": False,
                        "isNew": False,
                        "operator": "IS NOT NULL",
                        "operatorId": "IS_NOT_NULL",
                        "sqlExpression": "null",
                        "subject": "Categoría"
                      }
                    ],
                    "all_columns": [
                      "Categoría",
                      "Unidades vendidas mes anterior",
                      "Total ingresos por venta mes anterior",
                      "%participación mes anterior",
                      "Unidades vendidas",
                      "Total ingresos por venta",
                      "%participación",
                      "Diferencia de participación"
                    ],
                    "color_pn": True,
                    "conditional_formatting": [
                      {
                        "colorScheme": "#ACE1C4",
                        "column": "Diferencia de participación",
                        "operator": "≥",
                        "targetValue": 0
                      }
                    ],
                    "extra_form_data": {},
                    "granularity_sqla": "null",
                    "groupby": [],
                    "order_by_cols": [
                      "[\"Diferencia de participación\", False]"
                    ],
                    "order_desc": True,
                    "percent_metrics": [],
                    "query_mode": "raw",
                    "row_limit": "5",
                    "server_page_length": 10,
                    "show_cell_bars": False,
                    "table_timestamp_format": "smart_date",
                    "time_grain_sqla": "P1D",
                    "time_range": "No filter",
                    "viz_type": "table"
                  }
                }
        name = "Change participation category"
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Categorias con mayor alza en participación",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Categories participation rise"] = r.json()['id']

    def create_category_participation_fall_table(self):
        """
        Create a table that shows the top 6 categories that decrease their
        participation in the last month
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [
                    "Categoría",
                    "Unidades vendidas mes anterior",
                    "Total ingresos por venta mes anterior",
                    "%participación mes anterior",
                    "Unidades vendidas",
                    "Total ingresos por venta",
                    "%participación",
                    "Diferencia de participación"
                  ],
                  "color_pn": True,
                  "conditional_formatting": [
                    {
                      "colorScheme": "#EFA1AA",
                      "column": "Diferencia de participación",
                      "operator": "≤",
                      "targetValue": 0
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "metrics": [],
                  "order_by_cols": [
                    "[\"Diferencia de participación\", True]"
                  ],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": "5",
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        name = "Change participation category"
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": f"{name} {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Categorias con mayor baja en participación",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Categories participation fall"] = r.json()['id']

    def create_incomes_per_os_chart(self):
        """
        Create a chart that shows the distribution of incomes
        per os in each month
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "1",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_tehc16fjs8_97h5ta8c8aq",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "==",
                      "operatorId": "EQUALS",
                      "sqlExpression": "null",
                      "subject": "prod.wc"
                    }
                  ],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "os"
                  ],
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "metrics": [
                    {
                      "aggregate": "null",
                      "column": "null",
                      "expressionType": "SQL",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Total",
                      "optionName": "metric_7f0sbwpz7zp_zhjtu5n8o8",
                      "sqlExpression": "SUM(\"prod.p\" * \"prod.q\")"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "orientation": "vertical",
                  "rich_tooltip": True,
                  "row_limit": 10000,
                  "show_legend": True,
                  "stack": False,
                  "time_grain_sqla": "P1M",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_bar",
                  "xAxisLabelRotation": 45,
                  "x_axis_time_format": "%m/%Y",
                  "x_axis_title": "Fecha",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": "$,.0f",
                  "y_axis_title": "Ingreso",
                  "y_axis_title_margin": 100,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        name = f"{self.name} EVENT PRODS CONVERSION"
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": name,
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Ingresos historicos por OS",
                   "viz_type": "echarts_timeseries_bar"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Incomes per os"] = r.json()['id']

    def create_searches_proportion_per_os_chart(self):
        """
        Create a chart that shows the distribution of searches
        per os in each month
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "1",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_lhge40w7y1g_q9rt2uuen3h",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "==",
                      "operatorId": "EQUALS",
                      "sqlExpression": "null",
                      "subject": "qfinal"
                    },
                    {
                      "clause": "WHERE",
                      "comparator": "BOT",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_dbj4nyvfkp7_lfjaxw193v",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "!=",
                      "operatorId": "NOT_EQUALS",
                      "sqlExpression": "null",
                      "subject": "os"
                    }
                  ],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "os"
                  ],
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "logAxis": False,
                  "metrics": [
                    {
                      "aggregate": "null",
                      "column": "null",
                      "expressionType": "SQL",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Cantidad",
                      "optionName": "metric_nvbeel6ryz_2hz2stcnnta",
                      "sqlExpression": "COUNT(*)"
                    }
                  ],
                  "minorSplitLine": False,
                  "only_total": True,
                  "order_desc": True,
                  "orientation": "vertical",
                  "rich_tooltip": True,
                  "row_limit": 10000,
                  "show_legend": True,
                  "time_grain_sqla": "P1M",
                  "time_range": "No filter",
                  "tooltipTimeFormat": "smart_date",
                  "truncateYAxis": False,
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_bar",
                  "xAxisLabelRotation": 45,
                  "x_axis_time_format": "%m/%Y",
                  "x_axis_title": "Fecha",
                  "x_axis_title_margin": 30,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": ",.0f",
                  "y_axis_title": "Cantidad",
                  "y_axis_title_margin": 100,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        name = f"{self.name} SEARCH"
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[name],
                   "datasource_name": name,
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Proporción historica de búsquedas por OS",
                   "viz_type": "echarts_timeseries_bar"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Searches proportion per os"] = r.json()['id']

    def create_search_groups_table(self):
        """
        """
        params = {
                  "adhoc_filters": [],
                  "all_columns": [],
                  "color_pn": True,
                  "conditional_formatting": [],
                  "extra_form_data": {},
                  "groupby": [
                    "Búsqueda"],
                  "include_search": True,
                  "metrics": [
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Total",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Total",
                      "optionName": "metric_m31fkszf2bn_me52fazdd7l",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Unidades",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Unidades",
                      "optionName": "metric_h12n1jnc15p_kg9sq162ige",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Grupo de búsqueda",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "TEXT",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Grupo de búsqueda",
                      "optionName": "metric_ihz7d2o5p8_nm27p7t3mw",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Cantidad de busquedas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "BIGINT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Cantidad de búsquedas",
                      "optionName": "metric_edog5oq24m_l2zjarb1svg",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Top 3 Búsquedas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "TEXT",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Top 3 Búsquedas",
                      "optionName": "metric_jmlncpr0up_te072t1agfi",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Top 3 Productos",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "TEXT",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Top 3 Productos",
                      "optionName": "metric_r0hk18gwq5_bewhogdyhw4",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Top 3 Marcas",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "TEXT",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Top 3 Marcas",
                      "optionName": "metric_g3trbrrfykl_ucdfxznbz7l",
                      "sqlExpression": "null"
                    },
                    {
                      "aggregate": "MAX",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Top 3 Categorías",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "id": 1309,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "TEXT",
                        "type_generic": 1,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": True,
                      "isNew": False,
                      "label": "Top 3 Categorías",
                      "optionName": "metric_zvnox9hsjz_oyt28yjk24a",
                      "sqlExpression": "null"
                    }
                  ],
                  "order_by_cols": [],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "aggregate",
                  "row_limit": 10000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_search_group"],
                   "datasource_name": f"{self.name}_search_group",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Grupos de búsqueda de este mes",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search groups table"] = r.json()['id']

    def create_search_graph_chart(self):
        params = {
                  "adhoc_filters": [],
                  "baseEdgeWidth": "10",
                  "baseNodeSize": "40",
                  "color_scheme": "d3Category20",
                  "draggable": True,
                  "edgeLength": 300,
                  "edgeSymbol": "none,none",
                  "extra_form_data": {},
                  "friction": 0.3,
                  "granularity_sqla": "null",
                  "gravity": 0.3,
                  "layout": "force",
                  "legendMargin": "null",
                  "legendOrientation": "top",
                  "legendType": "scroll",
                  "metric": {
                    "aggregate": "SUM",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Total",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "SUM(Total)",
                    "optionName": "metric_vghyxk8seql_j6mukd9vsmb",
                    "sqlExpression": "null"
                  },
                  "repulsion": 1150,
                  "roam": True,
                  "row_limit": 1000,
                  "selectedMode": "single",
                  "showSymbolThreshold": 1000000,
                  "show_legend": False,
                  "source": "Grupo",
                  "source_category": "Grupo",
                  "target": "Query",
                  "target_category": "Grupo",
                  "time_range": "No filter",
                  "viz_type": "graph_chart"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_group_query"],
                   "datasource_name": f"{self.name}_group_query",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Grupos de búsqueda de este mes - "
                                 + "Grafo de nodos",
                   "viz_type": "graph_chart"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search groups graph"] = r.json()['id']

    def create_search_rise_tendency_table(self):
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "0",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_jd4fchcdx4g_use5prpo6wr",
                      "isExtra": False,
                      "isNew": False,
                      "operator": ">",
                      "operatorId": "GREATER_THAN",
                      "sqlExpression": "null",
                      "subject": "change"
                    }
                  ],
                  "all_columns": [
                    "query",
                    "min",
                    "max",
                    "Last week",
                    "change"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Last week": {
                      "d3NumberFormat": ".2%"
                    },
                    "change": {
                      "d3NumberFormat": ".2%"
                    },
                    "max": {
                      "d3NumberFormat": ".2%"
                    },
                    "min": {
                      "d3NumberFormat": ".2%",
                      "horizontalAlign": "right"
                    },
                    "query": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [
                    {
                      "colorScheme": "#ACE1C4",
                      "column": "change",
                      "operator": "≥",
                      "targetValue": -0.1
                    }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "order_by_cols": [],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": 10000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_rise_table"],
                   "datasource_name": f"{self.name}_rise_table",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Tendencias de búsquedas al "
                                 + "alza de esta semana",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search rise tendency table"] = r.json()['id']

    def create_search_fall_tendency_table(self):
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "0",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_jd4fchcdx4g_use5prpo6wr",
                      "isExtra": False,
                      "isNew": False,
                      "operator": "<",
                      "operatorId": "LESS_THAN",
                      "sqlExpression": "null",
                      "subject": "change"
                    }
                  ],
                  "all_columns": [
                    "query",
                    "min",
                    "max",
                    "Last week",
                    "change"
                  ],
                  "color_pn": True,
                  "column_config": {
                    "Last week": {
                      "d3NumberFormat": ".2%"
                    },
                    "change": {
                      "d3NumberFormat": ".2%"
                    },
                    "max": {
                      "d3NumberFormat": ".2%"
                    },
                    "min": {
                      "d3NumberFormat": ".2%",
                      "horizontalAlign": "right"
                    },
                    "query": {
                      "horizontalAlign": "left"
                    }
                  },
                  "conditional_formatting": [
                      {
                        "colorScheme": "#EFA1AA",
                        "column": "change",
                        "operator": "≤",
                        "targetValue": 0.1
                      }
                  ],
                  "extra_form_data": {},
                  "groupby": [],
                  "include_search": True,
                  "order_by_cols": [],
                  "order_desc": True,
                  "percent_metrics": [],
                  "query_mode": "raw",
                  "row_limit": 10000,
                  "server_page_length": 10,
                  "show_cell_bars": False,
                  "table_timestamp_format": "smart_date",
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "table"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_fall_table"],
                   "datasource_name": f"{self.name}_fall_table",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Tendencias de búsquedas a la "
                                 + "baja de esta semana",
                   "viz_type": "table"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search fall tendency table"] = r.json()['id']

    def create_search_rise_tendency_chart(self):
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "Query"
                  ],
                  "legendOrientation": "right",
                  "legendType": "scroll",
                  "limit": 10,
                  "markerEnabled": True,
                  "markerSize": 2,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Participation",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": False,
                      "isNew": False,
                      "label": "SUM(Participation)",
                      "optionName": "metric_reqfg80gy_26dgdxbwssy",
                      "sqlExpression": "null"
                    }
                  ],
                  "only_total": True,
                  "order_desc": True,
                  "rich_tooltip": True,
                  "row_limit": 10000,
                  "show_legend": True,
                  "time_grain_sqla": "P1W",
                  "time_range": "No filter",
                  "timeseries_limit_metric": {
                    "aggregate": "MAX",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Change",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "MAX(Change)",
                    "optionName": "metric_gp6d651rj1a_na2hpiu4e8",
                    "sqlExpression": "null"
                  },
                  "tooltipSortByMetric": True,
                  "tooltipTimeFormat": "%d/%m/%Y",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "xAxisLabelRotation": 45,
                  "x_axis_time_format": "%d/%m/%Y",
                  "x_axis_title": "Semana",
                  "x_axis_title_margin": 75,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": ".0%",
                  "y_axis_title": "Porcentaje de participación",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_rise_chart"],
                   "datasource_name": f"{self.name}_rise_chart",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Top 10 búsquedas con mayor "
                                 + "alza últimas 10 semanas",
                   "viz_type": "echarts_timeseries_smooth"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search rise tendency chart"] = r.json()['id']

    def create_search_fall_tendency_chart(self):
        params = {
                  "adhoc_filters": [],
                  "annotation_layers": [],
                  "color_scheme": "d3Category20",
                  "comparison_type": "values",
                  "extra_form_data": {},
                  "forecastInterval": 0.8,
                  "forecastPeriods": 10,
                  "granularity_sqla": "__time",
                  "groupby": [
                    "Query"
                  ],
                  "legendOrientation": "right",
                  "legendType": "scroll",
                  "limit": 10,
                  "markerEnabled": True,
                  "markerSize": 2,
                  "metrics": [
                    {
                      "aggregate": "SUM",
                      "column": {
                        "advanced_data_type": "null",
                        "certification_details": "null",
                        "certified_by": "null",
                        "column_name": "Participation",
                        "description": "null",
                        "expression": "null",
                        "filterable": True,
                        "groupby": True,
                        "is_certified": False,
                        "is_dttm": False,
                        "python_date_format": "null",
                        "type": "FLOAT",
                        "type_generic": 0,
                        "verbose_name": "null",
                        "warning_markdown": "null"
                      },
                      "expressionType": "SIMPLE",
                      "hasCustomLabel": False,
                      "isNew": False,
                      "label": "SUM(Participation)",
                      "optionName": "metric_reqfg80gy_26dgdxbwssy",
                      "sqlExpression": "null"
                    }
                  ],
                  "only_total": True,
                  "order_desc": False,
                  "rich_tooltip": True,
                  "row_limit": 10000,
                  "show_legend": True,
                  "time_grain_sqla": "P1W",
                  "time_range": "No filter",
                  "timeseries_limit_metric": {
                    "aggregate": "MIN",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "Change",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "FLOAT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "MIN(Change)",
                    "optionName": "metric_gp6d651rj1a_na2hpiu4e8",
                    "sqlExpression": "null"
                  },
                  "tooltipSortByMetric": True,
                  "tooltipTimeFormat": "%d/%m/%Y",
                  "truncate_metric": True,
                  "viz_type": "echarts_timeseries_smooth",
                  "xAxisLabelRotation": 45,
                  "x_axis_time_format": "%d/%m/%Y",
                  "x_axis_title": "Semana",
                  "x_axis_title_margin": 75,
                  "y_axis_bounds": [
                    "null",
                    "null"
                  ],
                  "y_axis_format": ".0%",
                  "y_axis_title": "Porcentaje de participación",
                  "y_axis_title_margin": 50,
                  "y_axis_title_position": "Left",
                  "zoomable": True
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets[f"{self.name}_fall_chart"],
                   "datasource_name": f"{self.name}_fall_chart",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Top 10 búsquedas con mayor "
                                 + "baja últimas 10 semanas",
                   "viz_type": "echarts_timeseries_smooth"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Search fall tendency chart"] = r.json()['id']

    def create_products_bought_together_chart(self):
        """
        Create a chart that shows the relation between products that
        are bought in the same conversion
        """
        params = {
                  "adhoc_filters": [
                    {
                      "clause": "WHERE",
                      "comparator": "1",
                      "expressionType": "SIMPLE",
                      "filterOptionName": "filter_mnfj89j9bkl_89vpdl472tx",
                      "isExtra": False,
                      "isNew": False,
                      "operator": ">",
                      "operatorId": "GREATER_THAN",
                      "sqlExpression": "null",
                      "subject": "EXPR$3"
                    }
                  ],
                  "color_scheme": "d3Category20",
                  "columns": "b",
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "groupby": "a",
                  "metric": {
                    "aggregate": "MAX",
                    "column": {
                      "advanced_data_type": "null",
                      "certification_details": "null",
                      "certified_by": "null",
                      "column_name": "EXPR$3",
                      "description": "null",
                      "expression": "null",
                      "filterable": True,
                      "groupby": True,
                      "is_certified": False,
                      "is_dttm": False,
                      "python_date_format": "null",
                      "type": "INT",
                      "type_generic": 0,
                      "verbose_name": "null",
                      "warning_markdown": "null"
                    },
                    "expressionType": "SIMPLE",
                    "hasCustomLabel": False,
                    "isNew": False,
                    "label": "MAX(EXPR$3)",
                    "optionName": "metric_i68w2bs7x1_bpywka7b9tb",
                    "sqlExpression": "null"
                  },
                  "row_limit": 1000,
                  "time_range": "No filter",
                  "viz_type": "chord",
                  "y_axis_format": "SMART_NUMBER"
                }
        payload = {"cache_timeout": 0,
                   "certification_details": "",
                   "certified_by": "",
                   "dashboards": [self.dashboard_id],
                   "datasource_id": self.datasets["Products bought together"],
                   "datasource_name": f"Products bought together {self.name}",
                   "datasource_type": "table",
                   "description": "",
                   "external_url": "",
                   "is_managed_externally": False,
                   "owners": [],
                   "params": json.dumps(params),
                   "query_context": "",
                   "query_context_generation": False,
                   "slice_name": "Productos historicamente compradas en "
                                 + "conjunto",
                   "viz_type": "chord"}
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Products bought together"] = r.json()['id']

    def create_period_selector_products_bought_together(self):
        """
        Create a purchase quantity and time filter for the
        products bought together chart
        """
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "filter_configs": [
                    {
                      "asc": True,
                      "clearable": True,
                      "column": "EXPR$3",
                      "defaultValue": "2;3",
                      "key": "oo9fxU8pn",
                      "label": "Cantidad mínima de compras",
                      "multiple": True,
                      "searchAllOptions": True
                    }
                  ],
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets["Products bought together"],
                    "datasource_name": f"Products bought together {self.name}",
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": ("Selección de cantidad mínima de compras "
                                   + "y de periodo para productos"),
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector products bought together"] = (
                    r.json()['id'])

    def create_period_selector_incomes_per_os(self):
        """
        Create a time filter for incomes per os chart
        """
        name = f"{self.name} EVENT PRODS CONVERSION"
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo ingresos por os",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector incomes per os"] = r.json()['id']

    def create_period_selector_searches_per_os(self):
        """
        Create a time filter for searches proportion per os chart
        """
        name = f"{self.name} SEARCH"
        params = {
                  "adhoc_filters": [],
                  "date_filter": True,
                  "extra_form_data": {},
                  "granularity_sqla": "__time",
                  "instant_filtering": True,
                  "time_grain_sqla": "P1D",
                  "time_range": "No filter",
                  "viz_type": "filter_box"
                }
        payload = {
                    "cache_timeout": 0,
                    "certification_details": "",
                    "certified_by": "",
                    "dashboards": [self.dashboard_id],
                    "datasource_id": self.datasets[name],
                    "datasource_name": name,
                    "datasource_type": "table",
                    "description": "",
                    "external_url": "",
                    "is_managed_externally": False,
                    "owners": [],
                    "params": json.dumps(params),
                    "query_context": "",
                    "query_context_generation": False,
                    "slice_name": "Selección de periodo búsquedas por os",
                    "viz_type": "filter_box"
                    }
        r = requests.post(self.base_url + self.chart_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.charts["Period selector searches per os"] = r.json()['id']

    def create_all(self):
        """
        Create all the charts available in the current class
        """
        self.create_general_results_table()
        self.create_monthly_comparator_chart()
        self.create_period_selector_generl_results()
        self.create_daily_searches_chart()
        self.create_daily_conversions_chart()
        self.create_last_3_month_daily_searches_chart()
        self.create_month_selector_grouped_daily_searches()
        self.create_last_3_month_daily_incomes_chart()
        self.create_month_selector_grouped_daily_incomes()
        self.create_incomes_per_searches_chart()
        self.create_zero_hits_table()
        self.create_period_selector_zero_hits()
        self.create_zero_hits_restock_table()
        self.create_zero_hits_new_table()
        self.create_zero_hits_old_table()
        self.create_top_10_products_table()
        self.create_product_rise_table()
        self.create_product_fall_table()
        self.create_general_results_by_brand_table()
        self.create_brand_participation_rise_table()
        self.create_brand_participation_fall_table()
        self.create_brands_behaviour_table()
        self.create_brand_participation_chart()
        self.create_total_incomes_per_brand()
        self.create_period_selector_participation_per_brand()
        self.create_brands_bought_together_chart()
        self.create_period_selector_brands_bought_together()
        self.create_general_results_per_category_table()
        self.create_category_participation_rise_table()
        self.create_category_participation_fall_table()
        self.create_category_participation_chart()
        self.create_total_incomes_per_category()
        self.create_period_selector_participation_per_category()
        self.create_categories_behaviour_table()
        self.create_categories_bought_together_chart()
        self.create_period_selector_categories_bought_together()
        self.create_incomes_per_os_chart()
        self.create_searches_proportion_per_os_chart()
        self.create_search_groups_table()
        self.create_search_graph_chart()
        self.create_search_rise_tendency_table()
        self.create_search_fall_tendency_table()
        self.create_search_rise_tendency_chart()
        self.create_search_fall_tendency_chart()
        self.create_products_bought_together_chart()
        self.create_period_selector_products_bought_together()
        self.create_period_selector_incomes_per_os()
        self.create_period_selector_searches_per_os()
