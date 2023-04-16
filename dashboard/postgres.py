import psycopg2
import csv
import sys
import os

class postgres_export():
    """
    """
    def __init__(self, store):
        self.connector = psycopg2.connect(database="testdb",
                                          user='postgres', password='admin',
                                          host='localhost', port='5432')
        self.cursor = self.connector.cursor()
        self.connector.autocommit = True
        self.store = store

    def search_group(self, create=False, copy=False):
        if create:
            sql = f'''CREATE TABLE {self.store}_search_group(Index int NOT NULL,\
            Búsqueda char(30),\
            Total int,\
            Unidades int,\
            Grupo_de_búsqueda VARCHAR,\
            Cantidad_de_busquedas int,\
            Top_3_Búsquedas VARCHAR(300),\
            Top_3_Productos VARCHAR(300),\
            Top_3_Marcas VARCHAR(300),\
            Top_3_Categorías VARCHAR(300));'''
            self.cursor.execute(sql)

        if copy:
            sql1 = f'''DELETE FROM {self.store}_search_group'''
            sql2 = f'''COPY {self.store}_search_group(Index,\
            Búsqueda,\
            Total,\
            Unidades,\
            Grupo_de_búsqueda,\
            Cantidad_de_busquedas,\
            Top_3_Búsquedas,\
            Top_3_Productos,\
            Top_3_Marcas,\
            Top_3_Categorías)
            FROM '/tmp/datasources/{self.store}_search_group.csv'
            DELIMITER ','
            CSV HEADER;'''
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)

    def group_query(self, create=False, copy=False):
        if create:
            sql = f'''CREATE TABLE {self.store}_group_query(Index int NOT NULL,\
            Grupo char(200),\
            Query char(200),\
            Total int);'''
            self.cursor.execute(sql)

        if copy:
            sql1 = f'''DELETE FROM {self.store}_group_query'''
            sql2 = f'''COPY {self.store}_group_query(Index,\
            Grupo,\
            Query,\
            Total)
            FROM '/tmp/datasources/{self.store}_group_query.csv'
            DELIMITER ','
            CSV HEADER;'''
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)

    def rise_chart(self, create=False, copy=False):
        if create:
            sql = f'''CREATE TABLE {self.store}_rise_chart(
            _time  DATE  NOT NULL PRIMARY KEY
            ,Query  VARCHAR(30) NOT NULL
            ,Participation FLOAT NOT NULL
            ,Change FLOAT NOT NULL
            );'''
            self.cursor.execute(sql)

        if copy:
            sql1 = f'''DELETE FROM {self.store}_rise_chart'''
            sql2 = f'''COPY {self.store}_rise_chart(_time,Query,Participation,Change)
            FROM '/tmp/datasources/{self.store}_rise_chart.csv'
            DELIMITER ','
            CSV HEADER;'''
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)

    def rise_table(self, create=False, copy=False):
        with open(f'{self.store}_search_group.csv') as csvFile:
            reader = csv.reader(csvFile)
            header = reader[0]
            if create:
                sql = f'''
                CREATE TABLE {self.store}_rise_table(
                  Query            FLOAT(30) NOT NULL PRIMARY KEY
                  ,Change           FLOAT(30) NOT NULL
                  ,MAX              FLOAT(30) NOT NULL
                  ,MIN              FLOAT(30) NOT NULL
                  ,"{header[4]}" FLOAT(30) NOT NULL
                  ,"{header[5]}" FLOAT(30) NOT NULL
                  ,"{header[6]}" FLOAT(30) NOT NULL
                  ,"{header[7]}" FLOAT(30) NOT NULL
                  ,"{header[8]}" FLOAT(30) NOT NULL
                  ,"{header[9]}" FLOAT(30) NOT NULL
                  ,"{header[10]}" FLOAT(30) NOT NULL
                  ,"{header[11]}" FLOAT(30) NOT NULL
                  ,"{header[12]}" FLOAT(30) NOT NULL
                  ,"{header[13]}" FLOAT(30) NOT NULL
                  ,"{header[14]}" FLOAT(30) NOT NULL
                );'''
                self.cursor.execute(sql)

            if copy:
                sql1 = f'''DELETE FROM {self.store}_rise_table'''
                sql2 = (f"COPY {self.store}_rise_table(Query,Change,MAX,MIN,"
                       + f"{header[4]},{header[5]},{header[6]},{header[7]},"
                       + f"{header[8]},{header[9]},{header[10]},{header[11]},"
                       + f"{header[12]},{header[13]},{header[14]})"
                       + f"FROM '/tmp/datasources/{self.store}_rise_table.csv'"
                       + "DELIMITER ',' "
                       + "CSV HEADER; ")
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)

    def fall_chart(self, create=False, copy=False):
        if create:
            sql = f'''CREATE TABLE {self.store}_fall_chart(
            _time  DATE  NOT NULL PRIMARY KEY
            ,Query  VARCHAR(30) NOT NULL
            ,Participation FLOAT NOT NULL
            ,Change FLOAT NOT NULL
            );'''
            self.cursor.execute(sql)

        if copy:
            sql1 = f'''DELETE FROM {self.store}_fall_chart'''
            sql2 = f'''COPY {self.store}_fall_chart(_time,Query,Participation,Change)
            FROM '/tmp/datasources/{self.store}_fall_chart.csv'
            DELIMITER ','
            CSV HEADER;'''
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)

    def fall_table(self, create=False, copy=False):
        with open(f'{self.store}_search_group.csv') as csvFile:
            reader = csv.reader(csvFile)
            header = reader[0]
            if create:
                sql = f'''
                CREATE TABLE {self.store}_fall_table(
                  Query            VARCHAR(30) NOT NULL PRIMARY KEY
                  ,Change           FLOAT(30) NOT NULL
                  ,MAX              FLOAT(30) NOT NULL
                  ,MIN              FLOAT(30) NOT NULL
                  ,"{header[4]}" FLOAT(30) NOT NULL
                  ,"{header[5]}" FLOAT(30) NOT NULL
                  ,"{header[6]}" FLOAT(30) NOT NULL
                  ,"{header[7]}" FLOAT(30) NOT NULL
                  ,"{header[8]}" FLOAT(30) NOT NULL
                  ,"{header[9]}" FLOAT(30) NOT NULL
                  ,"{header[10]}" FLOAT(30) NOT NULL
                  ,"{header[11]}" FLOAT(30) NOT NULL
                  ,"{header[12]}" FLOAT(30) NOT NULL
                  ,"{header[13]}" FLOAT(30) NOT NULL
                  ,"{header[14]}" FLOAT(30) NOT NULL
                );'''
                self.cursor.execute(sql)

            if copy:
                sql1 = f'''DELETE FROM {self.store}_fall_table'''
                sql2 = (f"COPY {self.store}_rise_table(Query,Change,MAX,MIN,"
                       + f"{header[4]},{header[5]},{header[6]},{header[7]},"
                       + f"{header[8]},{header[9]},{header[10]},{header[11]},"
                       + f"{header[12]},{header[13]},{header[14]})"
                       + f"FROM '/tmp/datasources/{self.store}_fall_table.csv'"
                       + "DELIMITER ',' "
                       + "CSV HEADER; ")
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)

    def finish(self):
        self.connector.commit()
        self.connector.close()

store = sys.argv[1]
psql = postgres_export(store)

#Para crear y poblar las tablas

psql.search_group(create=True, copy=True)
psql.group_query(create=True, copy=True)
psql.rise_chart(create=True, copy=True)
psql.rise_table(create=True, copy=True)
psql.fall_chart(create=True, copy=True)
psql.fall_table(create=True, copy=True)

#Para solamentre poblar tablas (la información existente se borra y se insertan
# datos nuevos)

psql.search_group(copy=True)
psql.group_query(copy=True)
psql.rise_chart(copy=True)
psql.rise_table(copy=True)
psql.fall_chart(copy=True)
psql.fall_table(copy=True)

psql.finish()