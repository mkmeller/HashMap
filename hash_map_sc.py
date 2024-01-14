# Name: Mike Meller
# Date: 12/7/23
# Description: Implementation of a hash map data structure using dynamic arrays and singly linked lists with chaining for collision resolution.

from da_and_sll import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

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
        Resizes the hash map if the load factor is >=1.
        Return None.
        """

        # Check if we need to resize
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Find where to insert the new key value pair
        target_bucket = self._hash(key)

        # Check if the key is already present, otherwise insert it
        target_node =  self._buckets[target_bucket].contains(key)
        if target_node:
            target_node.value = value
        else:
            self._buckets[target_bucket].insert(key, value)
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash map and re-populate with all existing key:value pairs.
        The supplied capacity must exceed 1.
        If supplied capacity is not prime, instead use next nearest prime.
        Returns None.
        """
        
        # New capcity must be 1 or more
        if new_capacity < 1:
            return
        
        # Hold the old hash map
        old_map = self._buckets
        old_capacity = self._capacity

        # New capacity should be prime and result in table load <= 1
        if not self._is_prime(new_capacity):
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity

        while self.table_load() > 1:
            self._capacity = self._next_prime(self._capacity * 2)

        # Create the new hash map
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        # Iterate through the old hash map moving all values to the new map
        for index in range(old_capacity):
            for node in old_map[index]:
                self.put(node.key, node.value)
    

    def table_load(self) -> float:
        """
        Return the current load factor for the hash map.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of un-populated buckets in the hash map.
        """
        empty = 0

        for index in range(self._capacity): 
            if self._buckets[index].length() == 0:
                empty +=1

        return empty
                

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

        # Check if the bucket contains the key, if so return value
        target_node = self._buckets[target_bucket].contains(key)
        if target_node:
            return target_node.value


    def contains_key(self, key: str) -> bool:
        """
        Returns whether the input key exists in the hash map.
        """
        
        # Check if hash map is empty
        if self._size == 0:
            return False
        
        # Find what bucket key should be in
        target_bucket = self._hash(key)
        if self._buckets[target_bucket].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove the input key and its associated value from the hash map.
        If the key is not in the hash map, do nothing.
        Return None.
        """

        # Find what bucket key should be in and remove it
        target_bucket = self._hash(key)
        if self._buckets[target_bucket].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array populated with tuples of every key:value pair in the hash map.
        """

        # Create an array
        return_arr = DynamicArray()

        # Iterate through the hash map adding all key:value pairs to the dynamic array
        for index in range(self._capacity):
            for node in self._buckets[index]:
                return_arr.append((node.key, node.value))
        
        return return_arr

    def clear(self) -> None:
        """
        Clears all existing key:value pairs from the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple containing a dynamic array of the mode(s) of the da followed by the frequency of the mode(s).
    Utilizes a hash map for storing frequency of each value.
    """

    # Create and populate a hash map
    # Key is the dynamic array entry, value is the frequency
    map = HashMap()
    for index in range(da.length()):
        current_freq = map.get(da[index])
        if current_freq:
            map.put(da[index], current_freq + 1)
        else:
            map.put(da[index], 1)

    most_freq = 0

    # Get all keys and values, iterate through them
    keys_and_vals = map.get_keys_and_values()
    for index in range(keys_and_vals.length()):
        curr_val = keys_and_vals[index][0]
        curr_freq = keys_and_vals[index][1]

        # If we found a new mode, re-set our dynamic array
        if curr_freq > most_freq:
            most_freq = curr_freq
            most_occuring = DynamicArray([curr_val])
        # If we found a value with our current mode, append to our dynamic array
        elif curr_freq == most_freq:
            most_occuring.append(curr_val)

    return (most_occuring, most_freq)
