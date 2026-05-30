"""
Prime number calculation module using the Sieve of Eratosthenes algorithm.

This module provides efficient prime number calculation with support for
both standard and segmented sieve implementations for handling large numbers.
"""

import time
import math
from typing import List, Tuple, Optional, Callable
from functools import lru_cache
import threading

from .config import MAX_SIEVE_MEMORY, SEGMENT_SIZE, CACHE_SIZE


class PrimeCalculator:
    """
    Core class for prime number calculation using various sieve implementations.
    
    Features:
        - Standard Sieve of Eratosthenes for numbers up to MAX_SIEVE_MEMORY
        - Segmented Sieve for larger numbers with reduced memory usage
        - Result caching for improved performance
        - Progress callback support for long calculations
    """
    
    def __init__(self):
        """Initialize the calculator with caching."""
        self._cache = {}
        self._cache_order = []
        self._lock = threading.Lock()
        self.calculation_time = 0.0
        self._stop_calculation = False
        
    def stop_calculation(self):
        """Signal to stop the current calculation."""
        self._stop_calculation = True
        
    @lru_cache(maxsize=CACHE_SIZE)
    def is_prime(self, n: int) -> bool:
        """
        Check if a single number is prime.
        
        Args:
            n: The number to check
            
        Returns:
            True if n is prime, False otherwise
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
            
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def calculate_primes(self, n: int, progress_callback: Optional[Callable[[float], None]] = None) -> List[int]:
        """
        Calculate all prime numbers up to n.
        
        Args:
            n: The upper limit for prime calculation
            progress_callback: Optional callback for progress updates (0.0 to 1.0)
            
        Returns:
            List of all prime numbers up to n
            
        Raises:
            ValueError: If n is less than 2
            MemoryError: If n is too large for available memory
        """
        if n < 2:
            raise ValueError("Number must be at least 2")
            
        # Reset stop flag
        self._stop_calculation = False
        
        # Check cache first
        with self._lock:
            if n in self._cache:
                self.calculation_time = 0.0
                return self._cache[n].copy()
        
        start_time = time.time()
        
        # Choose algorithm based on size
        if n <= MAX_SIEVE_MEMORY:
            primes = self._standard_sieve(n, progress_callback)
        else:
            primes = self._segmented_sieve(n, progress_callback)
            
        self.calculation_time = time.time() - start_time
        
        # Cache the result
        if not self._stop_calculation:
            self._add_to_cache(n, primes)
            
        return primes if not self._stop_calculation else []
    
    def _standard_sieve(self, n: int, progress_callback: Optional[Callable[[float], None]] = None) -> List[int]:
        """
        Standard Sieve of Eratosthenes implementation.
        
        Time Complexity: O(n log log n)
        Space Complexity: O(n)
        """
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        # Calculate total operations for progress
        limit = int(math.sqrt(n)) + 1
        total_ops = sum(1 for i in range(2, limit) if i * i <= n)
        ops_done = 0
        
        for current in range(2, limit):
            if self._stop_calculation:
                return []
                
            if sieve[current]:
                # Mark multiples as composite
                for multiple in range(current * current, n + 1, current):
                    sieve[multiple] = False
                    
                ops_done += 1
                if progress_callback and total_ops > 0:
                    progress_callback(ops_done / total_ops)
        
        # Collect primes
        primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        
        if progress_callback:
            progress_callback(1.0)
            
        return primes
    
    def _segmented_sieve(self, n: int, progress_callback: Optional[Callable[[float], None]] = None) -> List[int]:
        """
        Segmented Sieve implementation for large numbers.
        
        This reduces memory usage from O(n) to O(√n + segment_size).
        """
        limit = int(math.sqrt(n)) + 1
        
        # First, find all primes up to √n
        base_primes = self._standard_sieve(limit, None)
        
        # Initialize result with base primes
        primes = [p for p in base_primes if p <= n]
        
        # Process segments
        segments = (n - limit) // SEGMENT_SIZE + 1
        processed = 0
        
        for segment in range(segments):
            if self._stop_calculation:
                return []
                
            low = limit + segment * SEGMENT_SIZE + 1
            high = min(low + SEGMENT_SIZE - 1, n)
            
            if low > n:
                break
                
            # Create segment sieve
            seg_sieve = [True] * (high - low + 1)
            
            # Mark multiples of each base prime
            for prime in base_primes:
                # Find the first multiple of prime >= low
                start = ((low - 1) // prime + 1) * prime
                
                for j in range(start, high + 1, prime):
                    seg_sieve[j - low] = False
            
            # Collect primes from this segment
            for i in range(len(seg_sieve)):
                if seg_sieve[i]:
                    num = low + i
                    if num % 2 != 0 or num == 2:  # Skip even numbers except 2
                        primes.append(num)
            
            processed += 1
            if progress_callback:
                progress_callback(processed / segments)
        
        if progress_callback:
            progress_callback(1.0)
            
        return sorted(primes)
    
    def _add_to_cache(self, n: int, primes: List[int]):
        """Add a result to the cache with LRU eviction."""
        with self._lock:
            if n in self._cache:
                self._cache_order.remove(n)
            elif len(self._cache) >= CACHE_SIZE:
                # Remove oldest entry
                oldest = self._cache_order.pop(0)
                del self._cache[oldest]
            
            self._cache[n] = primes.copy()
            self._cache_order.append(n)
    
    def find_nth_prime(self, n: int) -> int:
        """
        Find the nth prime number.
        
        Args:
            n: The position of the prime to find (1-indexed)
            
        Returns:
            The nth prime number
            
        Raises:
            ValueError: If n is less than 1
        """
        if n < 1:
            raise ValueError("n must be at least 1")
            
        # Use approximation for upper bound
        if n < 6:
            small_primes = [2, 3, 5, 7, 11, 13]
            return small_primes[n - 1]
            
        # Upper bound approximation for nth prime
        upper_bound = int(n * (math.log(n) + math.log(math.log(n)) + 2))
        
        primes = self.calculate_primes(upper_bound)
        
        if len(primes) >= n:
            return primes[n - 1]
        else:
            # Need to search higher
            return self.find_nth_prime(n)
    
    def get_prime_factors(self, n: int) -> List[Tuple[int, int]]:
        """
        Get the prime factorization of a number.
        
        Args:
            n: The number to factorize
            
        Returns:
            List of (prime, exponent) tuples
        """
        if n < 2:
            return []
            
        factors = []
        
        # Check 2 separately
        count = 0
        while n % 2 == 0:
            count += 1
            n //= 2
        if count > 0:
            factors.append((2, count))
        
        # Check odd factors
        i = 3
        while i * i <= n:
            count = 0
            while n % i == 0:
                count += 1
                n //= i
            if count > 0:
                factors.append((i, count))
            i += 2
        
        # If n is still > 1, it's prime
        if n > 1:
            factors.append((n, 1))
            
        return factors
    
    def get_statistics(self, primes: List[int]) -> dict:
        """
        Calculate statistics about a list of primes.
        
        Args:
            primes: List of prime numbers
            
        Returns:
            Dictionary with various statistics
        """
        if not primes:
            return {}
            
        stats = {
            "count": len(primes),
            "smallest": primes[0],
            "largest": primes[-1],
            "density": len(primes) / primes[-1] if primes[-1] > 0 else 0,
        }
        
        # Find largest gap
        if len(primes) > 1:
            gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
            stats["largest_gap"] = max(gaps)
            stats["average_gap"] = sum(gaps) / len(gaps)
            
            # Count twin primes
            twin_count = sum(1 for i in range(len(primes)-1) if primes[i+1] - primes[i] == 2)
            stats["twin_primes"] = twin_count
        
        return stats