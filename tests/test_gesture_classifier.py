"""
SignSpeak - Unit Tests for Gesture Classifier
"""

import unittest
import numpy as np
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from software.gesture_classifier import GestureClassifier

class TestGestureClassifier(unittest.TestCase):
    """Test cases for GestureClassifier"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create dummy window data (20 frames, 11 sensors)
        self.test_window = np.random.rand(20, 11).tolist()
    
    def test_classifier_initialization(self):
        """Test classifier can be initialized"""
        try:
            classifier = GestureClassifier()
            self.assertIsNotNone(classifier.model)
            self.assertIsNotNone(classifier.label_encoder)
        except FileNotFoundError:
            self.skipTest("Model files not found. Train model first.")
    
    def test_feature_extraction(self):
        """Test feature extraction from window"""
        try:
            classifier = GestureClassifier()
            features = classifier.extract_features(self.test_window)
            
            # Should have 22 features (11 sensors * 2 features each: mean + std)
            self.assertEqual(features.shape[1], 22)
            self.assertEqual(features.shape[0], 1)
        except FileNotFoundError:
            self.skipTest("Model files not found. Train model first.")
    
    def test_prediction(self):
        """Test gesture prediction"""
        try:
            classifier = GestureClassifier()
            gesture = classifier.predict(self.test_window)
            
            # Should return a string
            self.assertIsInstance(gesture, str)
            self.assertGreater(len(gesture), 0)
        except FileNotFoundError:
            self.skipTest("Model files not found. Train model first.")
    
    def test_prediction_with_confidence(self):
        """Test prediction with confidence score"""
        try:
            classifier = GestureClassifier()
            gesture, confidence = classifier.predict_with_confidence(self.test_window)
            
            # Should return tuple of (string, float)
            self.assertIsInstance(gesture, str)
            self.assertIsInstance(confidence, (float, np.floating))
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
        except FileNotFoundError:
            self.skipTest("Model files not found. Train model first.")

if __name__ == "__main__":
    unittest.main()

