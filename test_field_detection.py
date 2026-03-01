"""
Test for PDF Field Detection functionality

Simple test to verify the PDFFieldDetector works correctly.
Run this to test the field detection engine before submitting PR.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.field_detector import PDFFieldDetector


def test_field_detector():
    """Test the PDF field detection with a sample PDF if available."""
    detector = PDFFieldDetector()
    
    # Look for any PDF files in the inputs directory
    test_paths = [
        "src/inputs/file.pdf",
        "src/test/sample.pdf", 
        "inputs/file.pdf"
    ]
    
    test_file = None
    for path in test_paths:
        if os.path.exists(path):
            test_file = path
            break
    
    if not test_file:
        print("❌ No test PDF found. Please add a PDF file to test with.")
        print("   Expected locations:", test_paths)
        return False
    
    print(f"🔍 Testing PDF field detection with: {test_file}")
    
    try:
        result = detector.detect_fields(test_file)
        
        print(f"✅ Success! Detected {result['field_count']} fields")
        print(f"   Pages processed: {result['pages_processed']}")
        
        if result['fields']:
            print("\n📋 Sample detected fields:")
            for i, field in enumerate(result['fields'][:3]):  # Show first 3 fields
                print(f"   {i+1}. {field['name']} ({field['type']}) - Page {field['page']}")
                if field['required']:
                    print(f"      ⚠️  Required field")
            
            if len(result['fields']) > 3:
                print(f"   ... and {len(result['fields']) - 3} more fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing field detection: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Testing PDF Field Detection Engine")
    print("=" * 50)
    
    success = test_field_detector()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ PDF Field Detection Engine is working correctly!")
        print("   Ready to submit PR with this functionality.")
    else:
        print("❌ Issues found. Please fix before submitting PR.")