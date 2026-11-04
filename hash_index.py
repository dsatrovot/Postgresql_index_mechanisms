class HashIndex:
    def __init__(self,size=5):
        self.size = size
        self.buckets=[ [] for i in range(size) ]
        print(self.buckets)
    def _hash(self,key):
        return key % self.size
    def insert(self,key,value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            # print(f"i -> {i}, existing_key -> {existing_key}, _ -> {_}")
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key,value))
    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None
    def show(self):
        for i, bucket in enumerate(self.buckets):
            print(f"Бакет {i}: {bucket}")

index = HashIndex(5)
index.insert(1, "Alex")

index.insert(6, "Ivan")
index.insert(12, "Maria")
index.show()