"""
Defines functions related to prime numbers
"""

import math

def is_prime(num: int) -> bool:
    """Returns True if {num} is prime, otherwise False"""
    if num==1:
        return False

    for curr_num in range(2, math.ceil(math.sqrt(num))):
        if num % curr_num == 0:
            return False

    return True
