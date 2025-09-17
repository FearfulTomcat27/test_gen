def greatest_common_divisor(a: int, b: int) -> int:                                                              
    """ Return a greatest common divisor of two integers a and b                                                 
    >>> greatest_common_divisor(3, 5)                                                                            
    1                                                                                                            
    >>> greatest_common_divisor(25, 15)                                                                          
    5                                                                                                            
    """                                                                                                          
    while b:                                                                                                     
        a, b = b, a % b                                                                                          
    return a                                                                                                     
                                                                                                                 
def check(candidate):                                                                                            
    assert candidate(12, 6) == 6                                                                                 
    assert candidate(0, 7) == 7                                                                                  
    assert candidate(-12, -18) == 6                                                                              
    assert candidate(0, 0) == 0                                                                                  
    assert candidate(10**18, 10**18 - 1) == 1                                                                    
check(greatest_common_divisor)