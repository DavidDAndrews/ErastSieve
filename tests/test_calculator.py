"""
Unit tests for the PrimeCalculator class.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.prime_calculator import PrimeCalculator


class TestPrimeCalculator(unittest.TestCase):
    """Test cases for prime calculation functionality."""
    
    def setUp(self):
        """Set up test calculator instance."""
        self.calculator = PrimeCalculator()
        
    def test_small_primes(self):
        """Test calculation of small prime numbers."""
        primes = self.calculator.calculate_primes(10)
        self.assertEqual(primes, [2, 3, 5, 7])
        
    def test_primes_up_to_100(self):
        """Test calculation up to 100."""
        primes = self.calculator.calculate_primes(100)
        self.assertEqual(len(primes), 25)
        self.assertEqual(primes[0], 2)
        self.assertEqual(primes[-1], 97)
        
    def test_edge_cases(self):
        """Test edge cases."""
        # Test n < 2
        with self.assertRaises(ValueError):
            self.calculator.calculate_primes(1)
            
        # Test n = 2
        primes = self.calculator.calculate_primes(2)
        self.assertEqual(primes, [2])
        
    def test_is_prime(self):
        """Test single prime checking."""
        self.assertTrue(self.calculator.is_prime(2))
        self.assertTrue(self.calculator.is_prime(17))
        self.assertTrue(self.calculator.is_prime(97))
        
        self.assertFalse(self.calculator.is_prime(1))
        self.assertFalse(self.calculator.is_prime(4))
        self.assertFalse(self.calculator.is_prime(100))
        
    def test_nth_prime(self):
        """Test finding nth prime."""
        self.assertEqual(self.calculator.find_nth_prime(1), 2)
        self.assertEqual(self.calculator.find_nth_prime(10), 29)
        self.assertEqual(self.calculator.find_nth_prime(100), 541)
        
    def test_prime_factors(self):
        """Test prime factorization."""
        factors = self.calculator.get_prime_factors(12)
        self.assertEqual(factors, [(2, 2), (3, 1)])
        
        factors = self.calculator.get_prime_factors(100)
        self.assertEqual(factors, [(2, 2), (5, 2)])
        
        factors = self.calculator.get_prime_factors(17)
        self.assertEqual(factors, [(17, 1)])
        
    def test_statistics(self):
        """Test statistics calculation."""
        primes = self.calculator.calculate_primes(100)
        stats = self.calculator.get_statistics(primes)
        
        self.assertEqual(stats["count"], 25)
        self.assertEqual(stats["smallest"], 2)
        self.assertEqual(stats["largest"], 97)
        self.assertGreater(stats["largest_gap"], 0)
        self.assertGreater(stats["twin_primes"], 0)
        
    def test_caching(self):
        """Test result caching."""
        # First calculation
        primes1 = self.calculator.calculate_primes(1000)
        time1 = self.calculator.calculation_time
        
        # Second calculation (should be cached)
        primes2 = self.calculator.calculate_primes(1000)
        time2 = self.calculator.calculation_time
        
        self.assertEqual(primes1, primes2)
        self.assertEqual(time2, 0.0)  # Cached result
        

if __name__ == "__main__":
    unittest.main()