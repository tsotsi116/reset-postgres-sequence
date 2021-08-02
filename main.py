from typing import List, Tuple, Union
import psycopg2


class Runner:
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str) -> None:
        connection_string = "dbname={dbname} user={user} password={password} host={host} port={port}"
        self.conn = psycopg2.connect(connection_string.format(
            dbname=dbname, user=user, password=password, host=host, port=port))

    def fetchAll(self, query: str) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res

    def fetchOne(self, query: str) -> Union[Tuple, None]:
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        return res

    def listTables(self, schema: str) -> List[Tuple]:
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'"
        return self.fetchAll(query.format(schema=schema))

    def getTablePrimaryKey(self, table: str) -> Union[str, None]:
        query = "SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE i.indrelid = '{table}'::regclass AND i.indisprimary"
        records = self.fetchOne(query.format(table=table))
        if records != None:
            if records[1] == 'integer':
                return records[0]

        return None

    def getTableSequence(self, table: str, primaryKey: str):
        query = "select pg_get_serial_sequence('{table}', '{primaryKey}')"
        records = self.fetchOne(query.format(
            table=table, primaryKey=primaryKey))
        return records[0]

    def updateSequence(self, table: str, pk: str, seq: str) -> None:
        query = "SELECT setval('{seq}', COALESCE((SELECT MAX({id})+1 FROM {table}), 1), false)"
        self.fetchOne(query.format(seq=seq, id=pk, table=table))
        print("Updated {s}".format(s=seq))


if __name__ == "__main__":
    host = "localhost"
    port = 5432
    user = "demo"
    password = "demo"
    database_name = "db"
    schema = "public"

    runner = Runner(host, port, database_name, user, password)
    tables = []  # stores (tablename, primaryKey, sequence)
    dbTables = runner.listTables(schema)

    print("{l} tables found from the database".format(l=len(dbTables)))

    for x in dbTables:
        pk = runner.getTablePrimaryKey(x[0])
        if pk != None:
            seq = runner.getTableSequence(
                "{schema}.{table}".format(schema=schema, table=x[0]), pk)
            if seq != None:
                tables.append((x[0], pk, seq))
                print("Found: {s} from table: {t} with primary key: {p}".format(
                    s=seq, t=x[0], p=pk))

    print("Processing {l} tables".format(l=len(tables)))
    for i in tables:
        try:
            runner.updateSequence(i[0], i[1], i[2])
        except:
            print("Something went wrong")

    runner.conn.close()
