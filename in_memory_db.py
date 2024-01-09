class InMemoryDB():
    def __init__(self):
        self.db = {}

    def _set(self, query):
        # timestamp = int(query[0])
        key = query[1]
        field = query[2]
        value = query[3]
        key_record = self.db[key] if key in self.db else {}
        key_record[field] = [value, -1]
        self.db[key] = key_record
        return ""
    
    def _compare_and_set(self, query):
        # timestamp = int(query[0])
        key = query[1]
        field = query[2]
        compare_value = query[3]
        new_value = query[4]
        key_record = self.db[key] if key in self.db else {}
        if key_record.get(field, [""])[0] == compare_value:
            key_record[field] = [new_value, -1]
            self.db[key] = key_record
            return "true"
        return "false"

    def _compare_and_delete(self, query):
        key = query[1]
        field = query[2]
        compare_value = query[3]
        key_record = self.db[key] if key in self.db else {}
        if key_record.get(field, [""])[0] == compare_value:
            del key_record[field]
            self.db[key] = key_record
            return "true"
        return "false"

    def _get(self, query):
        timestamp = int(query[0])
        key = query[1]
        field = query[2]
        key_record = self.db[key] if key in self.db else {}
        value = key_record.get(field, ["", -1])
        return value[0] if value[1] > timestamp or value[1] == -1 else ""

    def _scan(self, query):
        timestamp = int(query[0])
        key = query[1]
        key_record = self.db[key] if key in self.db else {}
        return ",".join([f"{k}({v[0]})" for k, v in key_record.items() if v[1] > timestamp or v[1] == -1])


    def _scan_by_prefix(self, query):
        key = query[1]
        prefix = query[2]
        length = len(prefix)
        key_record = self.db[key] if key in self.db else {}
        return ",".join([f"{k}({v[0]})" for k, v in key_record.items() if prefix == k[:length]])
    
    def _set_with_ttl(self, query):
        timestamp = int(query[0])
        key = query[1]
        field = query[2]
        value = query[3]
        ttl = int(query[4])
        key_record = self.db[key] if key in self.db else {}
        key_record[field] = [value, timestamp + ttl]
        self.db[key] = key_record
        return ""

    def _compare_and_set_with_ttl(self, query):
        timestamp = int(query[0])
        key = query[1]
        field = query[2]
        compare_value = query[3]
        new_value = query[4]
        ttl = int(query[5])
        key_record = self.db[key] if key in self.db else {}
        if key_record.get(field, [""])[0] == compare_value:
            key_record[field] = [new_value, ttl+timestamp]
            self.db[key] = key_record
            return "true"
        return "false"
    
    def get_function(self, command):
        if command == 'SET':
            return self._set
        elif command == 'GET':
            return self._get
        elif command == 'COMPARE_AND_SET':
            return self._compare_and_set
        elif command == 'COMPARE_AND_DELETE':
            return self._compare_and_delete
        elif command == 'SCAN':
            return self._scan
        elif command == 'SCAN_BY_PREFIX':
            return self._scan_by_prefix
        elif command == 'SET_WITH_TTL':
            return self._set_with_ttl
        elif command == 'COMPARE_AND_SET_WITH_TTL':
            return self._compare_and_set_with_ttl
        else:
            raise Exception('Invalid command')

    def execute(self, query):
        func = self.get_function(query[0])
        return func(query[1:])
    
    def execute_sequence(self, queries):
        results = []
        for query in queries:
            results.append(self.execute(query))
        return results