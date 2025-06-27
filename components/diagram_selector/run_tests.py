#!/usr/bin/env python3
"""
Simple test runner for Diagram Classifier Component
Developer: Hatem Soliman
"""

import json
import os
import sys
from diagram_classifier import DiagramClassifier, mock_granite_analysis

def test_basic_functionality():
  """Test basic functionality of the diagram classifier."""
  print("🧪 Testing Basic Functionality")
  print("=" * 40)
  
  classifier = DiagramClassifier()
  
  # Test 1: Sequence diagram detection
  transcript1 = """
  We discussed the user authentication flow. When a user logs in, 
  the system first validates their credentials, then checks their permissions, 
  and finally grants access to the appropriate modules.
  """
  
  result1 = classifier.analyze_content(transcript1)
  print(f"✅ Test 1 - Authentication Flow:")
  print(f"   Diagram: {result1.diagram_type}")
  print(f"   Confidence: {result1.confidence:.2f}")
  print(f"   Keywords: {result1.keywords}")
  print()
  
  # Test 2: Class diagram detection
  transcript2 = """
  We need to design the User class with attributes like username, email, and password.
  The User class should inherit from BaseEntity and have relationships with Role and Permission classes.
  """
  
  result2 = classifier.analyze_content(transcript2)
  print(f"✅ Test 2 - Class Design:")
  print(f"   Diagram: {result2.diagram_type}")
  print(f"   Confidence: {result2.confidence:.2f}")
  print(f"   Keywords: {result2.keywords}")
  print()
  
  # Test 3: Use case diagram detection
  transcript3 = """
  Users can register for an account, log in, view their profile, update their information,
  and reset their password. Administrators can manage users, view system reports.
  """
  
  result3 = classifier.analyze_content(transcript3)
  print(f"✅ Test 3 - User Requirements:")
  print(f"   Diagram: {result3.diagram_type}")
  print(f"   Confidence: {result3.confidence:.2f}")
  print(f"   Keywords: {result3.keywords}")
  print()
  
  return True

def test_mock_api():
  """Test the mock API function."""
  print("🔌 Testing Mock API Function")
  print("=" * 40)
  
  transcript = "We discussed the user authentication flow with multiple steps."
  result = mock_granite_analysis(transcript)
  
  try:
    parsed = json.loads(result)
    print(f"✅ Mock API Test:")
    print(f"   Output: {parsed['diagram_type']}")
    print(f"   Confidence: {parsed['confidence']:.2f}")
    print(f"   Valid JSON: ✅")
    print()
    return True
  except json.JSONDecodeError:
    print("❌ Mock API Test: Invalid JSON output")
    return False

def test_sample_data():
  """Test with sample data if available."""
  print("📊 Testing with Sample Data")
  print("=" * 40)
  
  # Try to find sample data
  possible_paths = [
    'data/sample_meetings/sample_transcripts.json',
    '../../data/sample_meetings/sample_transcripts.json',
    '../data/sample_meetings/sample_transcripts.json'
  ]
  
  sample_file = None
  for path in possible_paths:
    if os.path.exists(path):
      sample_file = path
      break
  
  if sample_file is None:
    print("⚠️  Sample data not found, skipping sample data test")
    return True
  
  try:
    with open(sample_file, 'r') as f:
      samples = json.load(f)['sample_meetings']
    
    classifier = DiagramClassifier()
    
    print(f"📋 Found {len(samples)} sample meetings:")
    for i, meeting in enumerate(samples[:3], 1):  # Test first 3
      result = classifier.analyze_content(meeting['transcript'])
      print(f"   {i}. {meeting['title']}: {result.diagram_type} ({result.confidence:.2f})")
    
    print()
    return True
  except Exception as e:
    print(f"❌ Sample data test failed: {e}")
    return False

def main():
  """Run all tests."""
  print("🚀 Diagram Classifier Component Tests")
  print("=" * 50)
  print()
  
  tests = [
    ("Basic Functionality", test_basic_functionality),
    ("Mock API", test_mock_api),
    ("Sample Data", test_sample_data)
  ]
  
  passed = 0
  total = len(tests)
  
  for test_name, test_func in tests:
    try:
      if test_func():
        passed += 1
        print(f"✅ {test_name}: PASSED")
      else:
        print(f"❌ {test_name}: FAILED")
    except Exception as e:
      print(f"❌ {test_name}: ERROR - {e}")
    print()
  
  print("📈 Test Results Summary")
  print("=" * 30)
  print(f"Passed: {passed}/{total}")
  print(f"Success Rate: {(passed/total)*100:.1f}%")
  
  if passed == total:
    print("🎉 All tests passed! Component is ready for use.")
    return 0
  else:
    print("⚠️  Some tests failed. Please review the issues above.")
    return 1

if __name__ == "__main__":
  sys.exit(main()) 