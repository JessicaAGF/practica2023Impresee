import json
import DatasetsTemplate as dt
import ChartsTemplate as ct
import requests


# crear metodo para extrar id del store desde algun json**
class DashboardTemplate(object):
    """
    This class allows to create a full dashboard for a store
    """

    def __init__(self, shop_name: str) -> None:
        self.base_url = 'http://localhost:8088'
        self.dashboard_url = '/api/v1/dashboard'
        self.name = shop_name
        self.databases = {'druid': 2, 'extra': 3}

    def authentication(self) -> None:
        """
        Realize the autentication of this session in the api
        """
        payload = {
                    'username': 'admin',
                    'password': 'admin',
                    'provider': 'db'
                   }
        r = requests.post(self.base_url + '/api/v1/security/login',
                          json=payload)

        access_token = r.json()
        self.token = access_token['access_token']
        self.headers_auth = {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

    def create_dashboard(self) -> None:
        """
        Create a dashboard with the given name
        """
        payload = {
                   "certification_details": "",
                   "certified_by": "",
                   "css": ".css-1bwh6rl {\r\n\
                                background: rgb(255 243 199);\r\n}\r\n\
                           .css-1gsicwv {\r\n \
                                margin: 20px 0px 20px 0px;\r\n}\r\n\
                           .table-striped>tbody>tr:nth-of-type(odd) {\r\n\
                                background-color: #d9d8d4;\r\n}\r\n\
                           .header-large {\r\n  font-size: 65px;\r\n\
                                font-family:'Raleway',Helvetica,Arial,"
                          + "Lucida,sans-serif;\r\n\
                                color: #334060;\r\n}\r\n\
                           .header-medium{\r\n\
                                font-size: 45px;\r\n\
                                color:#334060;\r\n\
                                font-family: 'Raleway',Helvetica,"
                            + "Arial,Lucida,sans-serif;\r\n}\r\n\
                            .header-small{\r\n\
                                font-size: 25px;\r\n\
                                color: #334060;\r\n\
                                font-family: 'Raleway',Helvetica,Arial,"
                            + "Lucida,sans-serif;\r\n}\r\n.\
                            header-title{\r\n\
                                font-size:14px;\r\n\
                                color: #032066;\r\n\
                                font-family:'Raleway',Helvetica,Arial,"
                            + "Lucida,sans-serif;\r\n}\r\n\
                            .css-jik4gi {\r\n\
                                color: #334060;\r\n\
                                font-family: 'Raleway',Helvetica,Arial,"
                            + "Lucida,sans-serif;\r\n}\r\n\
                            .css-tvoj80 {\r\n\
                                display: inline-flex;\r\n\
                                align-items: flex-end;\r\n\
                                color: #334060;\r\n\
                                font-family: 'Raleway',Helvetica,Arial,"
                            + "Lucida,sans-serif;\r\n}\r\n\
                            .dashboard-component-chart-holder {\r\n\
                                background-color: #fff;\r\n\
                                border: 2px solid #0000;\r\n\
                                color: #334060;\r\n\
                                height: 100%;\r\n\
                                overflow-y: visible;\r\n\
                                padding: 16px;\r\n\
                                position: relative;\r\n\
                                transition: opacity .2s,\
                                    border-color .2s,box-shadow .2s;\r\n\
                                width: 100%;\r\n\
                                font-family: 'Raleway',Helvetica,Arial,"
                            + "Lucida,sans-serif;\r\n}\r\n\
                            .vx-linepath{\r\n\
                                stroke: #E06100;\r\n}",
                   "dashboard_title": "pruebapepe",
                   "external_url": "",
                   "is_managed_externally": "false",
                   "json_metadata": "",
                   "owners": [],
                   "position_json": "",
                   "published": "false",
                   "roles": [],
                   "slug": self.name + "1234"
                   }
        r = requests.post(self.base_url + self.dashboard_url, json=payload,
                          headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)
        self.dashboard_id = r.json()['id']

    def create_datasets(self) -> None:
        """
        Instance and create all the dataset available
        """
        this_template = dt.DatasetsTemplate(self.name, self.token)
        this_template.create_all()
        self.datasets = this_template.get_datasets_id()

    def create_charts(self) -> None:
        """
        Instance and create all the charts available
        """
        this_template = ct.ChartsTemplate(self.name, self.token, self.datasets,
                                          self.dashboard_id)
        this_template.create_all()
        self.charts = this_template.get_charts_id()

    def get_all_info(self):
        """
        Show the id's for the dashboard, datasets and chars
        """
        print("Dashboard Id", self.dashboard_id)
        print("-------------------------------")
        # print("Datasets:", self.datasets)
        print("-------------------------------")
        print("Charts:", self.charts)

    def change_position(self):
        """
        Update the position of each chart in the
        current dashboard
        """
        position = {
                    "CHART-explore-186-1": {
                        "children": [],
                        "id": "CHART-explore-186-1",
                        "meta": {
                            "chartId": self.charts["Daily Searches"],
                            "height": 50,
                            "sliceName": "Búsquedas diarias",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen",
                            "TAB-cj-fo8X2vo",
                            "ROW-D80671f0-"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-187-1": {
                        "children": [],
                        "id": "CHART-explore-187-1",
                        "meta": {
                            "chartId": self.charts["Daily Conversions"],
                            "height": 50,
                            "sliceName": "Conversiones diarias",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "ROW-wvvsibxaMA"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-188-1": {
                        "children": [],
                        "id": "CHART-explore-188-1",
                        "meta": {
                            "chartId": self.charts["Daily searches in "
                                                   + "last 3 months"],
                            "height": 50,
                            "sliceName": "Búsquedas diarias ultimos 3 meses",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen",
                            "TAB-xRCbfMbxI",
                            "ROW-i4hh1kmgx"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-189-1": {
                        "children": [],
                        "id": "CHART-explore-189-1",
                        "meta": {
                            "chartId": self.charts["Incomes per day in "
                                                   + "last 3 months"],
                            "height": 50,
                            "sliceName": "Ingresos diarios ultimos 3 meses",
                            "sliceNameOverride": "Ingresos diarios últimos 3 "
                                                 + "meses",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB",
                            "TAB-TdmIa3B1aG",
                            "ROW-L-K1gBWTh"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-190-1": {
                        "children": [],
                        "id": "CHART-explore-190-1",
                        "meta": {
                            "chartId": self.charts["Incomes per searches"],
                            "height": 50,
                            "sliceName": "Incomes per searches",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB",
                            "TAB-Ydskjo7xo",
                            "ROW-vjq4KoyT7"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-191-1": {
                        "children": [],
                        "id": "CHART-explore-191-1",
                        "meta": {
                            "chartId": self.charts["Top 10 products "
                                                   + "with greatest incomes"],
                            "height": 50,
                            "sliceName": "Top 10 productos con "
                                         + "mayores ingresos",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-0hFRm5nUMN",
                            "ROW-Zr69P3Flp"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-192-1": {
                        "children": [],
                        "id": "CHART-explore-192-1",
                        "meta": {
                            "chartId": self.charts["Product rise per month"],
                            "height": 50,
                            "sliceName": "Productos con mayor "
                                         + "alza en ingresos",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-Y-dm92GF_",
                            "ROW-82bWfRm1T"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-193-1": {
                        "children": [],
                        "id": "CHART-explore-193-1",
                        "meta": {
                            "chartId": self.charts["Product fall per month"],
                            "height": 50,
                            "sliceName": "Productos con mayor "
                                         + "baja en ingresos",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-mhWuw8PG4",
                            "ROW-ngurRQiY0"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-194-1": {
                        "children": [],
                        "id": "CHART-explore-194-1",
                        "meta": {
                            "chartId": self.charts["General results "
                                                   + "per brand"],
                            "height": 50,
                            "sliceName": "Resultados generales por marca",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-eYdyOURAcC",
                            "ROW-Wwy79INLw"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-195-1": {
                        "children": [],
                        "id": "CHART-explore-195-1",
                        "meta": {
                            "chartId": self.charts["Brand participation rise"],
                            "height": 50,
                            "sliceName": "Marcas con mayor "
                                         + "alza en participación",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-78ZdW9GjM",
                            "ROW-iOI_RKeLt"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-196-1": {
                        "children": [],
                        "id": "CHART-explore-196-1",
                        "meta": {
                            "chartId": self.charts["Brand participation fall"],
                            "height": 50,
                            "sliceName": "Marcas con mayor baja "
                                         + "en participación",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-zr_QcGwBt",
                            "ROW-YbLFDisgB"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-197-1": {
                        "children": [],
                        "id": "CHART-explore-197-1",
                        "meta": {
                            "chartId": self.charts["Brands behaviour"],
                            "height": 77,
                            "sliceName": "Comportamiento de marcas",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "ROW-UG22azNEiA"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-198-1": {
                        "children": [],
                        "id": "CHART-explore-198-1",
                        "meta": {
                            "chartId": self.charts["Participation per brand"],
                            "height": 83,
                            "sliceName": "Participación de marcas",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8",
                            "TAB-GynnQxwc-O",
                            "ROW-6eQbDTsos"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-199-1": {
                        "children": [],
                        "id": "CHART-explore-199-1",
                        "meta": {
                            "chartId": self.charts["Brands bought together"],
                            "height": 81,
                            "sliceName": "Marcas compradas en conjunto",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8",
                            "TAB-_9_nF3Met",
                            "ROW-MY6dSIK1r"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-200-1": {
                        "children": [],
                        "id": "CHART-explore-200-1",
                        "meta": {
                            "chartId": self.charts["General results per "
                                                   + "category"],
                            "height": 50,
                            "sliceName": "Resultados generales por categoria",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-qZDd5UGCTw",
                            "ROW-4sZTuB-Mc"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-201-1": {
                        "children": [],
                        "id": "CHART-explore-201-1",
                        "meta": {
                            "chartId": self.charts["Categories participation "
                                                   + "fall"],
                            "height": 50,
                            "sliceName": "Categorias con mayor "
                                         + "baja en participación",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-ECh-F4cLj",
                            "ROW-h_JuIv09H"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-202-1": {
                        "children": [],
                        "id": "CHART-explore-202-1",
                        "meta": {
                            "chartId": self.charts["Categories participation "
                                                   + "rise"],
                            "height": 50,
                            "sliceName": "Categorias con mayor "
                                         + "alza en participación",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-SO1zpo1nc",
                            "ROW-HWGg00Zv7"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-203-1": {
                        "children": [],
                        "id": "CHART-explore-203-1",
                        "meta": {
                            "chartId": self.charts["Participation per "
                                                   + "category"],
                            "height": 76,
                            "sliceName": "Participación de categorias",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r",
                            "TAB-87c-X8Lg0-",
                            "ROW-zD_wPQ9Na"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-204-1": {
                        "children": [],
                        "id": "CHART-explore-204-1",
                        "meta": {
                            "chartId": self.charts["Categories behaviour"],
                            "height": 80,
                            "sliceName": "Comportamiento categorias",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "ROW-Yarc6OL3Z"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-205-1": {
                        "children": [],
                        "id": "CHART-explore-205-1",
                        "meta": {
                            "chartId": self.charts["Categories bought "
                                                   + "together"],
                            "height": 70,
                            "sliceName": "Categorías compradas en conjunto",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r",
                            "TAB-iAkNtQdVF",
                            "ROW-madfaDbdc"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-206-1": {
                        "children": [],
                        "id": "CHART-explore-206-1",
                        "meta": {
                            "chartId": self.charts["General results"],
                            "height": 50,
                            "sliceName": "Resultados generales",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA",
                            "TAB-0ohneoYEq9",
                            "ROW-rWP-ylhki"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-207-1": {
                        "children": [],
                        "id": "CHART-explore-207-1",
                        "meta": {
                            "chartId": self.charts["Monthly comparator"],
                            "height": 50,
                            "sliceName": "Comparador mensual",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA",
                            "TAB-mF-1VrPVW",
                            "ROW-PBLz1fdQX"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-208-1": {
                        "children": [],
                        "id": "CHART-explore-208-1",
                        "meta": {
                            "chartId": self.charts["Incomes per os"],
                            "height": 60,
                            "sliceName": "Ingresos por os",
                            "sliceNameOverride": "Ingresos por OS "
                                                 + "desde el buscador",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "ROW--ROuGnKxh"
                        ],
                        "type": "CHART"
                    },
                    "CHART-explore-209-1": {
                        "children": [],
                        "id": "CHART-explore-209-1",
                        "meta": {
                            "chartId": self.charts["Searches proportion "
                                                   + "per os"],
                            "height": 61,
                            "sliceName": "Proporción de búsquedas por OS",
                            "uuid": "0e307e57-c06d-472f-a012-e3348ca92879",
                            "width": 12
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "ROW-pGSR8X0Uz"
                        ],
                        "type": "CHART"
                    },
                    "DASHBOARD_VERSION_KEY": "v2",
                    "DIVIDER-5Puij1uK88": {
                        "children": [],
                        "id": "DIVIDER-5Puij1uK88",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-GXiFqbo3ME": {
                        "children": [],
                        "id": "DIVIDER-GXiFqbo3ME",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-P-Klf6Lb_M": {
                        "children": [],
                        "id": "DIVIDER-P-Klf6Lb_M",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-R4OXV_AKmX": {
                        "children": [],
                        "id": "DIVIDER-R4OXV_AKmX",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-WCeqVXkZG7": {
                        "children": [],
                        "id": "DIVIDER-WCeqVXkZG7",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-Z2APZcvp_T": {
                        "children": [],
                        "id": "DIVIDER-Z2APZcvp_T",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-clpKy9fkcx": {
                        "children": [],
                        "id": "DIVIDER-clpKy9fkcx",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "DIVIDER-ge6iOEA0X6": {
                        "children": [],
                        "id": "DIVIDER-ge6iOEA0X6",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "DIVIDER"
                    },
                    "GRID_ID": {
                        "children": [
                            "HEADER-1gO7GTQjVo",
                            "HEADER-xjWlSkmAjx",
                            "TABS-X3lXOdQphA",
                            "DIVIDER-Z2APZcvp_T",
                            "HEADER-csBwvRFRBX",
                            "TABS-I_uPLwGPen",
                            "DIVIDER-5Puij1uK88",
                            "HEADER-CL8QBbtqfZ",
                            "ROW-wvvsibxaMA",
                            "DIVIDER-GXiFqbo3ME",
                            "HEADER-CLhBnbSPZL",
                            "TABS-TSrKieR_oB",
                            "DIVIDER-R4OXV_AKmX",
                            "HEADER-XX2XkLVaHx",
                            "TABS-UULYCj6_OB",
                            "DIVIDER-P-Klf6Lb_M",
                            "HEADER-i3G7FZ7vag",
                            "HEADER-qUNDzT_jSv",
                            "TABS-TEp0hRjbkP",
                            "ROW-UG22azNEiA",
                            "TABS-d8BycgkYb8",
                            "DIVIDER-WCeqVXkZG7",
                            "HEADER-zQsGwG26Vh",
                            "TABS-gZ99jIfT_0",
                            "ROW-Yarc6OL3Z",
                            "TABS-RUyJeDhf_r",
                            "DIVIDER-ge6iOEA0X6",
                            "HEADER-UiRxGCG_zy",
                            "ROW--ROuGnKxh",
                            "ROW-pGSR8X0Uz",
                            "DIVIDER-clpKy9fkcx"
                        ],
                        "id": "GRID_ID",
                        "parents": [
                            "ROOT_ID"
                        ],
                        "type": "GRID"
                    },
                    "HEADER-1gO7GTQjVo": {
                        "children": [],
                        "id": "HEADER-1gO7GTQjVo",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT",
                            "headerSize": "LARGE_HEADER",
                            "text": "Insights & Métricas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-CL8QBbtqfZ": {
                        "children": [],
                        "id": "HEADER-CL8QBbtqfZ",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "SMALL_HEADER",
                            "text": "Performance de conversiones"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-CLhBnbSPZL": {
                        "children": [],
                        "id": "HEADER-CLhBnbSPZL",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "SMALL_HEADER",
                            "text": "Performance de ingresos"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-UiRxGCG_zy": {
                        "children": [],
                        "id": "HEADER-UiRxGCG_zy",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT",
                            "headerSize": "MEDIUM_HEADER",
                            "text": "Análisis por dispositivo"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-XX2XkLVaHx": {
                        "children": [],
                        "id": "HEADER-XX2XkLVaHx",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "MEDIUM_HEADER",
                            "text": "Análisis por Producto"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-csBwvRFRBX": {
                        "children": [],
                        "id": "HEADER-csBwvRFRBX",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "SMALL_HEADER",
                            "text": "Performance de búsquedas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-i3G7FZ7vag": {
                        "children": [],
                        "id": "HEADER-i3G7FZ7vag",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT",
                            "headerSize": "MEDIUM_HEADER",
                            "text": "Análisis por Marca y Categoría"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-qUNDzT_jSv": {
                        "children": [],
                        "id": "HEADER-qUNDzT_jSv",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "SMALL_HEADER",
                            "text": "Marcas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-xjWlSkmAjx": {
                        "children": [],
                        "id": "HEADER-xjWlSkmAjx",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "MEDIUM_HEADER",
                            "text": "Métricas Generales"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER-zQsGwG26Vh": {
                        "children": [],
                        "id": "HEADER-zQsGwG26Vh",
                        "meta": {
                            "background": "BACKGROUND_WHITE",
                            "headerSize": "SMALL_HEADER",
                            "text": "Categorías"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "HEADER"
                    },
                    "HEADER_ID": {
                        "id": "HEADER_ID",
                        "meta": {
                            "text": "Pepeganga"
                        },
                        "type": "HEADER"
                        },
                    "ROOT_ID": {
                        "children": [
                            "GRID_ID"
                        ],
                        "id": "ROOT_ID",
                        "type": "ROOT"
                    },
                    "ROW--ROuGnKxh": {
                        "children": [
                            "CHART-explore-208-1"
                        ],
                        "id": "ROW--ROuGnKxh",
                        "meta": {
                            "0": "ROOT_ID",
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "ROW"
                    },
                    "ROW-4sZTuB-Mc": {
                        "children": [
                            "CHART-explore-200-1"
                        ],
                        "id": "ROW-4sZTuB-Mc",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-qZDd5UGCTw"
                        ],
                        "type": "ROW"
                    },
                    "ROW-6eQbDTsos": {
                        "children": [
                            "CHART-explore-198-1"
                        ],
                        "id": "ROW-6eQbDTsos",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8",
                            "TAB-GynnQxwc-O"
                        ],
                        "type": "ROW"
                    },
                    "ROW-82bWfRm1T": {
                        "children": [
                            "CHART-explore-192-1"
                        ],
                        "id": "ROW-82bWfRm1T",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-Y-dm92GF_"
                        ],
                        "type": "ROW"
                    },
                    "ROW-D80671f0-": {
                        "children": [
                            "CHART-explore-186-1"
                        ],
                        "id": "ROW-D80671f0-",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen",
                            "TAB-cj-fo8X2vo"
                        ],
                        "type": "ROW"
                    },
                    "ROW-HWGg00Zv7": {
                        "children": [
                            "CHART-explore-202-1"
                        ],
                        "id": "ROW-HWGg00Zv7",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-SO1zpo1nc"
                        ],
                        "type": "ROW"
                    },
                    "ROW-L-K1gBWTh": {
                        "children": [
                            "CHART-explore-189-1"
                        ],
                        "id": "ROW-L-K1gBWTh",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB",
                            "TAB-TdmIa3B1aG"
                        ],
                        "type": "ROW"
                    },
                    "ROW-MY6dSIK1r": {
                        "children": [
                            "CHART-explore-199-1"
                        ],
                        "id": "ROW-MY6dSIK1r",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8",
                            "TAB-_9_nF3Met"
                        ],
                        "type": "ROW"
                    },
                    "ROW-PBLz1fdQX": {
                        "children": [
                            "CHART-explore-207-1"
                        ],
                        "id": "ROW-PBLz1fdQX",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA",
                            "TAB-mF-1VrPVW"
                        ],
                        "type": "ROW"
                    },
                    "ROW-UG22azNEiA": {
                        "children": [
                            "CHART-explore-197-1"
                        ],
                        "id": "ROW-UG22azNEiA",
                        "meta": {
                            "0": "ROOT_ID",
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "ROW"
                    },
                    "ROW-Wwy79INLw": {
                        "children": [
                            "CHART-explore-194-1"
                        ],
                        "id": "ROW-Wwy79INLw",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-eYdyOURAcC"
                        ],
                        "type": "ROW"
                    },
                    "ROW-Yarc6OL3Z": {
                        "children": [
                            "CHART-explore-204-1"
                        ],
                        "id": "ROW-Yarc6OL3Z",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "ROW"
                    },
                    "ROW-YbLFDisgB": {
                        "children": [
                            "CHART-explore-196-1"
                        ],
                        "id": "ROW-YbLFDisgB",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-zr_QcGwBt"
                        ],
                        "type": "ROW"
                    },
                    "ROW-Zr69P3Flp": {
                        "children": [
                            "CHART-explore-191-1"
                        ],
                        "id": "ROW-Zr69P3Flp",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-0hFRm5nUMN"
                        ],
                        "type": "ROW"
                    },
                    "ROW-h_JuIv09H": {
                        "children": [
                            "CHART-explore-201-1"
                        ],
                        "id": "ROW-h_JuIv09H",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0",
                            "TAB-ECh-F4cLj"
                        ],
                        "type": "ROW"
                    },
                    "ROW-i4hh1kmgx": {
                        "children": [
                            "CHART-explore-188-1"
                        ],
                        "id": "ROW-i4hh1kmgx",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen",
                            "TAB-xRCbfMbxI"
                        ],
                        "type": "ROW"
                    },
                    "ROW-iOI_RKeLt": {
                        "children": [
                            "CHART-explore-195-1"
                        ],
                        "id": "ROW-iOI_RKeLt",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP",
                            "TAB-78ZdW9GjM"
                        ],
                        "type": "ROW"
                    },
                    "ROW-madfaDbdc": {
                        "children": [
                            "CHART-explore-205-1"
                        ],
                        "id": "ROW-madfaDbdc",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r",
                            "TAB-iAkNtQdVF"
                        ],
                        "type": "ROW"
                    },
                    "ROW-ngurRQiY0": {
                        "children": [
                            "CHART-explore-193-1"
                        ],
                        "id": "ROW-ngurRQiY0",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB",
                            "TAB-mhWuw8PG4"
                        ],
                        "type": "ROW"
                    },
                    "ROW-pGSR8X0Uz": {
                        "children": [
                            "CHART-explore-209-1"
                        ],
                        "id": "ROW-pGSR8X0Uz",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "ROW"
                    },
                    "ROW-rWP-ylhki": {
                        "children": [
                            "CHART-explore-206-1"
                        ],
                        "id": "ROW-rWP-ylhki",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA",
                            "TAB-0ohneoYEq9"
                        ],
                        "type": "ROW"
                    },
                    "ROW-vjq4KoyT7": {
                        "children": [
                            "CHART-explore-190-1"
                        ],
                        "id": "ROW-vjq4KoyT7",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB",
                            "TAB-Ydskjo7xo"
                        ],
                        "type": "ROW"
                    },
                    "ROW-wvvsibxaMA": {
                        "children": [
                            "CHART-explore-187-1"
                        ],
                        "id": "ROW-wvvsibxaMA",
                        "meta": {
                            "0": "ROOT_ID",
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "ROW"
                    },
                    "ROW-zD_wPQ9Na": {
                        "children": [
                            "CHART-explore-203-1"
                        ],
                        "id": "ROW-zD_wPQ9Na",
                        "meta": {
                            "background": "BACKGROUND_TRANSPARENT"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r",
                            "TAB-87c-X8Lg0-"
                        ],
                        "type": "ROW"
                    },
                    "TAB-0hFRm5nUMN": {
                        "children": [
                            "ROW-Zr69P3Flp"
                        ],
                        "id": "TAB-0hFRm5nUMN",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Top 10 productos mayor ingreso"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB"
                        ],
                        "type": "TAB"
                    },
                    "TAB-0ohneoYEq9": {
                        "children": [
                            "ROW-rWP-ylhki"
                        ],
                        "id": "TAB-0ohneoYEq9",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Tabla"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA"
                        ],
                        "type": "TAB"
                        },
                    "TAB-78ZdW9GjM": {
                        "children": [
                            "ROW-iOI_RKeLt"
                        ],
                        "id": "TAB-78ZdW9GjM",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Marcas con mayor alza en participación "
                                    + "de ventas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP"
                        ],
                        "type": "TAB"
                        },
                    "TAB-87c-X8Lg0-": {
                        "children": [
                            "ROW-zD_wPQ9Na"
                        ],
                        "id": "TAB-87c-X8Lg0-",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Participación de categorías"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r"
                        ],
                        "type": "TAB"
                    },
                    "TAB-ECh-F4cLj": {
                        "children": [
                            "ROW-h_JuIv09H"
                        ],
                        "id": "TAB-ECh-F4cLj",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Categorías con mayor baja en "
                                    + "participación de ventas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0"
                        ],
                        "type": "TAB"
                        },
                    "TAB-GynnQxwc-O": {
                        "children": [
                            "ROW-6eQbDTsos"
                        ],
                        "id": "TAB-GynnQxwc-O",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Participación marcas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8"
                        ],
                        "type": "TAB"
                        },
                    "TAB-SO1zpo1nc": {
                        "children": [
                            "ROW-HWGg00Zv7"
                        ],
                        "id": "TAB-SO1zpo1nc",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Categorías con mayor alza en "
                                    + "participación de ventas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0"
                        ],
                        "type": "TAB"
                        },
                    "TAB-TdmIa3B1aG": {
                        "children": [
                            "ROW-L-K1gBWTh"
                        ],
                        "id": "TAB-TdmIa3B1aG",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Ingreso"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB"
                        ],
                        "type": "TAB"
                        },
                    "TAB-Y-dm92GF_": {
                        "children": [
                            "ROW-82bWfRm1T"
                        ],
                        "id": "TAB-Y-dm92GF_",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Productos con mayo alza en ingresos"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB"
                        ],
                        "type": "TAB"
                        },
                    "TAB-Ydskjo7xo": {
                        "children": [
                            "ROW-vjq4KoyT7"
                        ],
                        "id": "TAB-Ydskjo7xo",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Ingreso por búsqueda"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TSrKieR_oB"
                        ],
                        "type": "TAB"
                    },
                    "TAB-_9_nF3Met": {
                        "children": [
                            "ROW-MY6dSIK1r"
                        ],
                        "id": "TAB-_9_nF3Met",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Compras en conjunto"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-d8BycgkYb8"
                        ],
                        "type": "TAB"
                    },
                    "TAB-cj-fo8X2vo": {
                        "children": [
                            "ROW-D80671f0-"
                        ],
                        "id": "TAB-cj-fo8X2vo",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Búsquedas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen"
                        ],
                        "type": "TAB"
                    },
                    "TAB-eYdyOURAcC": {
                        "children": [
                            "ROW-Wwy79INLw"
                        ],
                        "id": "TAB-eYdyOURAcC",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Resultados generales"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP"
                        ],
                        "type": "TAB"
                    },
                    "TAB-iAkNtQdVF": {
                        "children": [
                            "ROW-madfaDbdc"
                        ],
                        "id": "TAB-iAkNtQdVF",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Compras en conjunto"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-RUyJeDhf_r"
                        ],
                        "type": "TAB"
                    },
                    "TAB-mF-1VrPVW": {
                        "children": [
                            "ROW-PBLz1fdQX"
                        ],
                        "id": "TAB-mF-1VrPVW",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Gráfico"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-X3lXOdQphA"
                        ],
                        "type": "TAB"
                    },
                    "TAB-mhWuw8PG4": {
                        "children": [
                            "ROW-ngurRQiY0"
                        ],
                        "id": "TAB-mhWuw8PG4",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Productos con mayor baja en ingresos"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-UULYCj6_OB"
                        ],
                        "type": "TAB"
                    },
                    "TAB-qZDd5UGCTw": {
                        "children": [
                            "ROW-4sZTuB-Mc"
                        ],
                        "id": "TAB-qZDd5UGCTw",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Resultados Generales"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-gZ99jIfT_0"
                        ],
                        "type": "TAB"
                    },
                    "TAB-xRCbfMbxI": {
                        "children": [
                            "ROW-i4hh1kmgx"
                        ],
                        "id": "TAB-xRCbfMbxI",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Búsquedas últimos 3 meses"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-I_uPLwGPen"
                        ],
                        "type": "TAB"
                    },
                    "TAB-zr_QcGwBt": {
                        "children": [
                            "ROW-YbLFDisgB"
                        ],
                        "id": "TAB-zr_QcGwBt",
                        "meta": {
                            "defaultText": "Tab title",
                            "placeholder": "Tab title",
                            "text": "Marcas con mayor baja en "
                                    + "participación de ventas"
                        },
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID",
                            "TABS-TEp0hRjbkP"
                        ],
                        "type": "TAB"
                        },
                    "TABS-I_uPLwGPen": {
                        "children": [
                            "TAB-cj-fo8X2vo",
                            "TAB-xRCbfMbxI"
                        ],
                        "id": "TABS-I_uPLwGPen",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                    },
                    "TABS-RUyJeDhf_r": {
                        "children": [
                            "TAB-87c-X8Lg0-",
                            "TAB-iAkNtQdVF"
                        ],
                        "id": "TABS-RUyJeDhf_r",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-TEp0hRjbkP": {
                        "children": [
                            "TAB-eYdyOURAcC",
                            "TAB-78ZdW9GjM",
                            "TAB-zr_QcGwBt"
                        ],
                        "id": "TABS-TEp0hRjbkP",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-TSrKieR_oB": {
                        "children": [
                            "TAB-TdmIa3B1aG",
                            "TAB-Ydskjo7xo"
                        ],
                        "id": "TABS-TSrKieR_oB",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-UULYCj6_OB": {
                        "children": [
                            "TAB-0hFRm5nUMN",
                            "TAB-Y-dm92GF_",
                            "TAB-mhWuw8PG4"
                        ],
                        "id": "TABS-UULYCj6_OB",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-X3lXOdQphA": {
                        "children": [
                            "TAB-0ohneoYEq9",
                            "TAB-mF-1VrPVW"
                        ],
                        "id": "TABS-X3lXOdQphA",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-d8BycgkYb8": {
                        "children": [
                            "TAB-GynnQxwc-O",
                            "TAB-_9_nF3Met"
                        ],
                        "id": "TABS-d8BycgkYb8",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        },
                    "TABS-gZ99jIfT_0": {
                        "children": [
                            "TAB-qZDd5UGCTw",
                            "TAB-SO1zpo1nc",
                            "TAB-ECh-F4cLj"
                        ],
                        "id": "TABS-gZ99jIfT_0",
                        "meta": {},
                        "parents": [
                            "ROOT_ID",
                            "GRID_ID"
                        ],
                        "type": "TABS"
                        }
                }
        payload = {
                    "position_json": json.dumps(position),
                  }
        r = requests.put(self.base_url + self.dashboard_url + "/" +
                         str(self.dashboard_id), json=payload,
                         headers=self.headers_auth)
        print("---")
        print(r)
        print(r.text)


dst = DashboardTemplate("Pepeganga")
dst.authentication()
# dst.create_datasets()
dst.datasets = {"General Results": 79,
                "Searches group by day": 80,
                "Incomes group by day": 81,
                "Incomes per searches": 82,
                "Change incomes per product": 84,
                "General results per brand": 85,
                "General results per category": 86,
                "Change participation brand": 87,
                "Change participation category": 88,
                "Participation per brand": 89,
                "Brands bought together": 90,
                "Participation per category": 91,
                "Categories bought together": 92,
                "Products bought together": 93,
                "Pepeganga EVENT CONVERSION": 94,
                "Pepeganga SEARCH": 95,
                "Pepeganga EVENT PRODS CONVERSION": 96,
                "Pepeganga PRODUCTS": 97,
                "Top ten products": 98}
dst.create_dashboard()
dst.create_charts()
dst.change_position()
dst.get_all_info()
