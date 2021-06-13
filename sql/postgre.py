# pip3 install psycopg2-binary
class SQLVariantStorage(VariantStorage):

    def __init__(self, host: str, port: int, database: str, username: str, password: str, prefix: str):
        self._connection = psycopg2.connect(
            host=host, port=port,
            database=database, user=username, password=password
        )
        self._connection.autocommit = False
        self._prefix = prefix

    def __del__(self):
        try:
            self._connection.close()
        except:
            pass

    def get(self, variant_key: str) -> Optional[List[str]]:
        #     cursor = self._connection.cursor()
        #     cursor.execute(f"SELECT variant_key, sku FROM {self._prefix}_variant tv LEFT JOIN {self._prefix}_sku ts ON tv.id=ts.variant_id WHERE variant_key=%s", (variant_key, ))
        #     result = cursor.fetchall()
        #     if len(result) == 1 and result[0][1] is None:
        #         # remove variant that exist without any sku
        #         cursor.execute(f"DELETE FROM {self._prefix}_variant WHERE variant_key=%s", (variant_key, ))
        #         self._connection.commit()
        #         return list()
        #     return [each_record[1] for each_record in result]
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"SELECT variant_key, sku FROM {self._prefix}_variant WHERE variant_key=%s", (variant_key,))
            return_value: List[str] = [each_record[1] for each_record in cursor.fetchall()]
            return None if len(return_value) == 0 else return_value
        except Exception as e:
            raise ReadVariantStorageException("can't obtain data from server ")
        else:
            cursor.close()

    def add_sku(self, variant_key: str, sku: str) -> List[str]:
        """
        add sku under variant_key
        :param variant_key:
        :raise ~AlreadyExistsVariantStorageException: when record already exist
        :raise ~WriteVariantStorageException: general exception of adding record to table
        :return:
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"INSERT INTO testaccount01_variant (variant_key, sku) VALUES (%s, %s);", (variant_key, sku))
            self._connection.commit()
            return self.get(variant_key)
        except Exception as e:
            self._connection.rollback()
            if "UniqueViolation" in str(type(e)):
                raise AlreadyExistsVariantStorageException()
            else:
                raise WriteVariantStorageException(f"can't write data {e}")
        else:
            cursor.close()

    def remove_sku(self, variant_key: str, sku: str) -> List[str]:
        """
        remove sku under variant_key
        :param data:
        :return:
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"DELETE FROM testaccount01_variant WHERE variant_key=%s AND sku=%s;", (variant_key, sku))
            self._connection.commit()
        except Exception as e:
            raise WriteVariantStorageException(f"can't remove data from server {e}")
        else:
            cursor.close()

    def remove_variant(self, variant_key: str) -> None:
        """
        remove variant by key
        :param variant_key:
        :return:
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"DELETE FROM testaccount01_variant WHERE variant_key=%s;", (variant_key,))
            self._connection.commit()
        except Exception as e:
            raise WriteVariantStorageException(f"can't remove data from server {e}")
        else:
            cursor.close()

