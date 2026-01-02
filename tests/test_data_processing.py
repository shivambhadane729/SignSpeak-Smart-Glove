"""
SignSpeak - Unit Tests for Data Processing
"""

import unittest
import numpy as np

class TestDataProcessing(unittest.TestCase):
    """Test cases for data processing functions"""
    
    def test_window_normalization(self):
        """Test window data normalization"""
        # Create test window
        window = np.random.rand(20, 11) * 1000
        
        # Calculate mean and std
        means = np.mean(window, axis=0)
        stds = np.std(window, axis=0)
        
        # Verify shapes
        self.assertEqual(means.shape, (11,))
        self.assertEqual(stds.shape, (11,))
        
        # Verify values are reasonable
        self.assertTrue(np.all(means >= 0))
        self.assertTrue(np.all(stds >= 0))
    
    def test_feature_vector_creation(self):
        """Test feature vector creation from window"""
        window = np.random.rand(20, 11)
        
        means = np.mean(window, axis=0)
        stds = np.std(window, axis=0)
        
        # Create feature vector
        features = []
        for m, s in zip(means, stds):
            features.append(m)
            features.append(s)
        
        features = np.array(features)
        
        # Should have 22 features
        self.assertEqual(len(features), 22)
        self.assertEqual(features.shape, (22,))

if __name__ == "__main__":
    unittest.main()

