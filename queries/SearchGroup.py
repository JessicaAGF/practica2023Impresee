import json
import os
import requests
import pandas as pd
import sys
from unidecode import unidecode
import inflector
from operator import itemgetter


class search_group():
    """
    """

    def __init__(self, store, month) -> None:
        self.date = f"TIME_FLOOR(TIME_SHIFT(CURRENT_TIMESTAMP, 'P1M', {-month}), 'P1M')"
        self.store = store
        self.month = month
        self.url = "http://localhost:8888/druid/v2/sql/"

    # Retorna la respuesta a una query en forma de lista
    # str -> list(any)
    def response(self, query):
        """ Returns the response to a query as a list
        """
        payload = json.dumps({
                "query": query,
                "resultFormat": "array",
                "context": {
                    "maxNumTasks": 4
                }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        return requests.request("POST", self.url, headers=headers,
                                data=payload).json()

    # A partir de una lista de strings, retorna el string más frecuente
    # list -> str
    def most_frequent_word(self, arr):
        """ With a list of strings as input, returns the most frequent words
        """
        n = len(arr)
        # freq to store the freq of the most occurring variable
        freq = 0
        # res to store the most occurring string in the array of strings
        res = ""
        # running nested for loops to find the most occurring
        # word in the array of strings
        for i in range(0, n, 1):
            count = 0
            for j in range(i + 1, n, 1):
                if arr[j] == arr[i]:
                    count += 1
            # updating our max freq of occurred string in the
            # array of strings
            if count >= freq:
                res = arr[i]
                freq = count
        return res

    # Retorna a partir de una lista de listas, con el primer elemento de cada
    # lista siendo un string, todos las palabras contenidas en la lista
    # list(list(str,any)) -> list
    def search_group_list(self, query_result):
        """
        With a list of lists, which first element is a string, as input,
        returns all of the words contained in every string
        """
        res = []
        for i in query_result:
            res += i[0].split(' ')
        return res

    # A partir de una lista de posibles keywords, determina la suma de ventas
    # y la cantidad de unidades vendidas totales del grupo de búsqueda para
    # cada posible keyword, y lo ordena por la suma de ventas totales
    # list(str) -> list((str, num, num))
    def get_list_keyword_income_sorted(self, keywords):
        """
        With a list of possible keywords as input, this functions definesa
        list of these keywords, its total sales and total units sold,
        and sorts this list by total sales.
        """
        keyword_ingreso = []
        for w in keywords:
            ingreso_grupo = "SELECT SUM(\"prod.p\"*\"prod.q\"), SUM(\"prod.q\")\
                             FROM \"{} EVENT PRODS CONVERSION\" \
                             WHERE TIME_FLOOR(__time, 'P1M') = {} \
                             AND CONTAINS_STRING(LOWER(\"prod.qt\"), '{}') \
                             AND \"prod.wc\" = 1".format(self.store,
                                                         self.date, w)

            response_ingreso_grupo = self.response(ingreso_grupo)[0]

            keyword_ingreso += [[w, int(response_ingreso_grupo[0]),
                                 int(response_ingreso_grupo[1])]]

        keyword_ingreso = sorted(keyword_ingreso, key=itemgetter(1),
                                 reverse=True)

        return keyword_ingreso

    # A partir de dos listas de strings, una de posibles de keywords y
    # otra de stopwords, entrega una lista de strings
    # que cumplen con las condiciones para ser keywords
    # list(str), list(str) -> list(str)
    def clean_keywords(self, stopwords, words):
        """
        With a list of stopwords and a list ofr words as input,
        this functions returns a list of strings that meet the
        requirements of a keyword
        """
        keywords = []
        inflectobj = inflector.Inflector()
        for i in words:
            word = inflectobj.singularize(i[0])
            if (word in stopwords or len(word) <= 2
                    or word in keywords or "'" in word or word.isnumeric()):
                pass
            else:
                keywords += [word]
        return keywords

    def array_to_str(self, arr):
        """
        With an array as input, this function returns
        the array in a string format
        """
        res = ''
        for e in arr:
            if e[0] == '':
                res += 'Nulo' + ' (' + str(int(e[1])) + '), '
            else:
                res += str(e[0]) + ' (' + str(int(e[1])) + '), '
        res = res[0:-2] + '.'
        return res

    def group_query(self, lista):
        """
        With a list of keywords as input, this function returns their
        related queries and incomes
        """
        res = []
        for i in lista:
            query = "SELECT '{}', LOWER(\"prod.qt\") as busqueda, \
                     SUM(\"prod.p\"*\"prod.q\") as total \
                     FROM \"{} EVENT PRODS CONVERSION\" \
                     WHERE TIME_FLOOR(__time, 'P1M') = {} \
                     AND \"prod.wc\" = 1 AND \
                     ARRAY_CONTAINS(STRING_TO_MV(LOWER(\"prod.qt\"), \
                        ' '),'{}')\
                     GROUP BY 2".format(i, self.store,
                                        self.date, i)
            response_query = self.response(query)
            for r in response_query:
                res += [[r[0], r[1], int(r[2])]]
        return res

    # A partir de una lista de listas, con el primer elemento de cada
    # lista siendo un string, retorna en el orden original los primeros
    # 30 strings que no estén contenidos en otros strings de la lista
    # list(list(str,any,any)) -> list(list(str,any,any))
    def get_first_30(self, keyword_income_quantity_list):
        """
        With a list of lists, which first element is a string, as input,
        this functions returns in the original order, the first 30 elements
        which strings are not contained in another string of the list of
        lists.
        """
        # Obtengo las primeras 30 keywords, intentando no repetir
        # grupos de búsqueda
        index = 0
        first_30 = []
        # Mientras no tenga las primeras 30 keywords
        while(index < 30):
            # add = True
            # Chequeo que no hayan palabras que se contengan unas a las
            # otras en las primeras 30 keywords
            i = index + 1
            while(i < len(keyword_income_quantity_list)):
                if (unidecode(keyword_income_quantity_list[index][0]) in
                        unidecode(keyword_income_quantity_list[i][0])):
                    keyword_income_quantity_list.pop(index)
                    i = index
                elif (unidecode(keyword_income_quantity_list[i][0]) in
                        unidecode(keyword_income_quantity_list[index][0])):
                    keyword_income_quantity_list.pop(i)
                i += 1
            first_30 += [keyword_income_quantity_list[index]]
            index += 1
        return first_30

    # A partir de una lista de keyword, ingreso y ventas totales,
    # retorna esta misma lista con los siguientes atributos adicionales;
    # grupo de busqueda, total de visitantes únicos, top 3 búsquedas,
    # top 3 productos y top 3 marcas.
    # list(list(str, num, num)) ->
    #   list(list(str, num, num, list(list(str, num)), num,
    #       list(list(str, num)), list(list(str, num)),
    #           list(list(str, num))))
    def get_first_30_full_info(self, keyword_income_quantity_list):
        """
        With a list of keywords, their total incomes and units sold,
        this function returns the following additional atributes:
            search group, total unique visitors, top 3 searches,
            top 3 products, top 3 brands and top 3 categories.
        """
        i = 0
        while(i < 30):
            # Calculamos el grupo de busqueda para cada keyword,
            # total de visitantes únicos, top 3 búsquedas, top 3 productos,
            # y top 3 marcas
            w = keyword_income_quantity_list[i][0]
            grupo_busqueda = "SELECT LOWER(\"in.intxt\"), COUNT(*)\
                              FROM \"{} SEARCH\" WHERE zero = 0 AND \
                              qfinal = 1 AND TIME_FLOOR(__time, 'P1M') = {}\
                              AND CONTAINS_STRING(LOWER(\"in.intxt\"), '{}')\
                              GROUP BY 1 \
                              ORDER BY 2 DESC \
                              LIMIT 30".format(self.store, self.date, w)
            response_grupo_busqueda = self.response(grupo_busqueda)
            # Calculamos el total de visitantes únicos por keyword
            total_busquedas = "SELECT COUNT(DISTINCT vid) FROM \"{} SEARCH\"\
                               WHERE zero = 0 AND qfinal = 1 AND\
                               TIME_FLOOR(__time, 'P1M') = {}\
                               AND CONTAINS_STRING(LOWER(\"in.intxt\"),\
                               '{}')".format(self.store, self.date, w)
            response_total_busquedas = self.response(total_busquedas)

            # Calculamos el top 3 búsquedas por keyword
            top3_busquedas = "SELECT \"prod.qt\", SUM(\"prod.q\"),\
                              SUM(\"prod.p\"*\"prod.q\") as total\
                              FROM \"{} EVENT PRODS CONVERSION\" \
                              WHERE TIME_FLOOR(__time, 'P1M') = {} \
                              AND CONTAINS_STRING(LOWER(\"prod.qt\") , '{}') AND\
                              \"prod.wc\" = 1 \
                              GROUP BY 1 \
                              ORDER BY 3 DESC \
                              LIMIT 3".format(self.store, self.date, w)
            response_top3_busquedas = self.response(top3_busquedas)

            # Calculamos el top 3 productos por keyword
            top3_productos = "SELECT name, SUM(\"prod.q\"), \
                              SUM(\"prod.p\"*\"prod.q\") as total\
                              FROM \"{} EVENT PRODS CONVERSION\" \
                              INNER JOIN (SELECT DISTINCT name, variant_id \
                              FROM \"{} PRODUCTS\") AS \"PROD\" ON\
                              \"{} EVENT PRODS CONVERSION\".\"prod.variant\" \
                              = \"PROD\".variant_id \
                              WHERE TIME_FLOOR(__time, 'P1M') = {}\
                              AND CONTAINS_STRING(LOWER(\"prod.qt\") , '{}') AND\
                              \"prod.wc\" = 1 \
                              GROUP BY 1 \
                              ORDER BY 3 DESC \
                              LIMIT 3".format(self.store, self.store,
                                              self.store, self.date, w)
            response_top3_productos = self.response(top3_productos)

            # Calculamos el top 3 marcas por keyword
            top3_marcas = "SELECT \"brand\", SUM(\"prod.q\"),\
                           SUM(\"prod.p\"*\"prod.q\") \
                           FROM \"{} EVENT PRODS CONVERSION\" AS PRODCONV \
                           INNER JOIN (SELECT DISTINCT variant_id,  brand\
                           FROM \"{} PRODUCTS\") AS PROD on\
                           PRODCONV.\"prod.variant\" = PROD.variant_id \
                           WHERE TIME_FLOOR(__time, 'P1M') = {}\
                           AND CONTAINS_STRING(LOWER(\"prod.qt\"), '{}') \
                           AND \"prod.wc\" = 1 \
                           GROUP BY 1 \
                           ORDER BY 3 DESC \
                           LIMIT 3".format(self.store, self.store,
                                           self.date, w)
            response_top3_marcas = self.response(top3_marcas)

            # Calculamos el top 3 categorías por keyword
            top3_categorias = "SELECT \"category\", SUM(\"prod.q\"), \
                               SUM(\"prod.p\"*\"prod.q\") \
                               FROM \"{} EVENT PRODS CONVERSION\" AS PRODCONV \
                               INNER JOIN (SELECT DISTINCT variant_id,\
                               category FROM \"{} PRODUCTS\") AS PROD on\
                               PRODCONV.\"prod.variant\" = PROD.variant_id \
                               WHERE TIME_FLOOR(__time, 'P1M') = {}\
                               AND CONTAINS_STRING(LOWER(\"prod.qt\"), '{}') \
                               AND \"prod.wc\" = 1 \
                               GROUP BY 1 \
                               ORDER BY 3 DESC \
                               LIMIT 3".format(self.store, self.store,
                                               self.date, w)
            response_top3_categorias = self.response(top3_categorias)
            keyword_income_quantity_list[i] = (keyword_income_quantity_list[i]
                                               + [response_grupo_busqueda]
                                               + [int(response_total_busquedas[0][0])]
                                               + [self.array_to_str(
                                                    response_top3_busquedas)]
                                               + [self.array_to_str(response_top3_productos)]
                                               + [self.array_to_str(
                                                    response_top3_marcas)]
                                               + [self.array_to_str(
                                                    response_top3_categorias)])

            i += 1
        return keyword_income_quantity_list

    def main(self):
        """
        This function writes out 2 files, {store}_search_group and
        {store}_group_query.
        """
        # Palabras distintas de queries que generaron ventas
        palabras_distintas = "SELECT DISTINCT STRING_TO_MV(LOWER(\"prod.qt\"), ' ') FROM \"{} EVENT PRODS CONVERSION\" \
        WHERE TIME_FLOOR(__time, 'P1M') = {} \
        AND \"prod.wc\" = 1".format(self.store, self.date)
        response_palabras_distintas = self.response(palabras_distintas)[1:]

        # Elimino stopwords de las lista de palabras obtenida, elimino
        # palabras de largo menor o igual a dos y elimino palabras que ya
        # existen
        stopwords = ["el", "la", "con", "en", "de", "las", "los", "a", "o",
                     "y", "un", "una", "para"]
        keywords = self.clean_keywords(stopwords, response_palabras_distintas)
        # Determino la suma de ventas y la cantidad de unidades vendidas del
        # grupo de búsqueda para cada psoible keyword
        keyword_income_sorted = self.get_list_keyword_income_sorted(keywords)

        # Obtengo las primeras 30 keywords preliminares con sus ingresos
        # totales
        first_30 = self.get_first_30(keyword_income_sorted)

        # Para cada keyword, adicionalmente calculamos su grupo de busqueda,
        # cantidad de visitantes únicos, top 3 búsquedas, top 3 productos y t
        # op 3 marcas
        first_30 = self.get_first_30_full_info(first_30)

        # Defino las keywords definitivas
        i = 0
        grupos_de_busqueda = []
        while(i < len(first_30)):
            search_group_list_i = self.search_group_list(first_30[i][3])
            first_30[i][0] = self.most_frequent_word(search_group_list_i)
            first_30[i][3] = self.array_to_str(first_30[i][3])
            grupos_de_busqueda += [first_30[i][0]]
            i += 1

        group_query_list = self.group_query(grupos_de_busqueda)

        os.chdir("/tmp/datasources/")
        # Traspasamos la información de las primeras 30 keywords con mayores
        # ventas a un archivo csv
        pd.DataFrame(first_30).to_csv(f'{self.store.lower()}_search_group_{self.month}.csv',
                                      encoding='utf-8-sig',
                                      index_label="Index",
                                      header=['Búsqueda', 'Total', 'Unidades',
                                              'Grupo de búsqueda',
                                              'Cantidad de busquedas',
                                              'Top 3 Búsquedas',
                                              'Top 3 Productos',
                                              'Top 3 Marcas',
                                              'Top 3 Categorías'])
        pd.DataFrame(group_query_list).to_csv(
                                    f'{self.store.lower()}_group_query_{self.month}.csv',
                                    encoding='utf-8-sig',
                                    index_label="Index", header=['Grupo',
                                                                 'Query',
                                                                 'Total'])

store = sys.argv[1]

# Meses y tienda a evaluar 
# Calcula los grupos de búsqueda de hace 1 mes
sg = search_group(store, 1)
sg.main()
