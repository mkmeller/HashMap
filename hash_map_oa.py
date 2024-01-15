# Name: Mike Meller
# Date: 12/7/23
# Description: Implementation of a hash map data structure using a dynamic arrays and open adrressing with quadratic probing for collision resolution.

from da_and_sll import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def _hash(self, key: str) -> int:
        '''
        Return the output of applying a hash function to a key.
        Output is scaled based on the current number of buckets in the hashmap.
        '''

        return self._hash_function(key) % self._capacity
    
    def put(self, key: str, value: object) -> None:
        """
        Add a key:value pair to the hash map.
        If the provided key is already in the hash map, overwrite the value.
        Resizes the hash map if the load factor is >=0.5.
        Return None.
        """
    
        # Check if we need to resize
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Find where to insert the new key value pair
        target_bucket = self._hash(key)    
        probe = 0

        # Iterate through the array with quadratic probing with wrap around
        # If we find a tombstone, take its place
        # If we find the key, replace its value
        # If we find an empty spot, insert new HashEntry there
        while self._buckets[target_bucket]:
            if self._buckets[target_bucket].is_tombstone:
                self._buckets[target_bucket] = HashEntry(key, value)
                self._size += 1
                return
            if self._buckets[target_bucket].key == key:
                self._buckets[target_bucket].value = value
                return

            target_bucket += (probe + 1)**2 - probe**2
            target_bucket %= self._capacity
            probe += 1

        self._buckets[target_bucket] = HashEntry(key, value)
        self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash map and re-populate with all existing key:value pairs.
        The supplied capacity must exceed 1.
        If supplied capacity is not prime, instead use next nearest prime.
        Returns None.
        """
        
        # New capcity must be able to hold all key:value pairs
        if new_capacity < self._size:
            return
        
        # Hold the old hash map
        old_map = self._buckets
        old_capacity = self._capacity

        # New capacity should be prime
        if not self._is_prime(new_capacity):
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity

        # Create the new hash map
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        # Iterate through the old hash map moving all values to the new hash map
        for index in range(old_capacity):
            curr = old_map[index]
            if curr and not curr.is_tombstone:
                self.put(curr.key, curr.value )


    def table_load(self) -> float:
        """
        Return the current load factor for the hash map.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of un-populated buckets in the hash map.
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Return the value associated with the input key.
        If the key is not in the hash map, return None.
        """

        # Check if hash map is empty
        if self._size == 0:
            return

        # Find what bucket key should be in
        target_bucket = self._hash(key)
        probe = 0

        # Iterate through the array with quadratic probing with wrap around
        # If we find a tombstone, keep going
        # If we find the key, return its value
        # If we find an empty spot, key is not present
        while self._buckets[target_bucket]:
            curr = self._buckets[target_bucket]
            if curr.key == key and not curr.is_tombstone:
                return curr.value

            target_bucket += (probe + 1)**2 - probe**2
            target_bucket %= self._capacity
            probe += 1


    def contains_key(self, key: str) -> bool:
        """
        Returns whether the input key exists in the hash map.
        """
        
        # Check if hash map is empty
        if self._size == 0:
            return False

        # Find what bucket key should be in
        target_bucket = self._hash(key)
        probe = 0

       # Iterate through the array with quadratic probing with wrap around
        # If we find a tombstone, keep going
        # If we find the key, return True
        # If we find an empty spot, return False
        while self._buckets[target_bucket]:
            curr = self._buckets[target_bucket]
            if curr.key == key and not curr.is_tombstone:
                return True

            target_bucket += (probe + 1)**2 - probe**2
            target_bucket %= self._capacity
            probe += 1

        return False

    def remove(self, key: str) -> None:
        """
        Remove the input key and its associated value from the hash map.
        If the key is not in the hash map, do nothing.
        Return None.
        """

        # Find what bucket key should be in and remove it
        target_bucket = self._hash(key)
        probe = 0

        # Iterate through the array with quadratic probing with wrap around
        # If we find our key and its not a tombstone, turn it into a tombstone.
        while self._buckets[target_bucket]:
            curr = self._buckets[target_bucket]
            if curr.key == key and not curr.is_tombstone:
                curr.is_tombstone = True
                self._size -= 1
                return

            target_bucket += (probe + 1)**2 - probe**2
            target_bucket %= self._capacity
            probe += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array populated with tuples of every key:value pair in the hash map.
        """

        # Create an array
        return_arr = DynamicArray()

        # Iterate through the hash map adding all key:value pairs to the dynamic array
        for index in range(self._capacity):
            curr = self._buckets[index]
            if curr and not curr.is_tombstone:
                return_arr.append((curr.key, curr.value))
        
        return return_arr

    def clear(self) -> None:
        """
        Clears all existing key:value pairs from the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0


    def __iter__(self):
        """
        Create an iterator for the hashmap.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next HashEntry that is not a tombstone and advance iterator.
        """

        # Keep searching while the index is valid by advancing iterator
        # If we find a non-tombstone HashEntry, advance iterator and return the entry.
        while self._index < self._buckets.length():
            val = self._buckets[self._index]
            if val and not val.is_tombstone:
                self._index += 1
                return val
            self._index += 1

        # If index goes out of bounds, stop iterating
        raise StopIteration
