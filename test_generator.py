#!/usr/bin/env python3
"""
Simple test script to verify the donation report generator functionality
"""

import os
import tempfile
from datetime import datetime
from donation_report_generator import DonationReportGenerator


def test_basic_functionality():
    """Test the basic functionality of the donation report generator"""
    print("Testing basic functionality...")
    
    # Create a mock generator with a fake token for testing purposes
    # Note: This won't actually connect to an API since we don't have real credentials
    generator = DonationReportGenerator("fake_token")
    
    # Test date calculation functions
    year = 2023
    month = 2  # February
    
    print(f"✓ Created DonationReportGenerator instance")
    
    # Test that the analysis function works with empty data
    empty_analysis = generator.analyze_donations([])
    assert empty_analysis['total_supporters'] == 0
    assert empty_analysis['unique_supporters'] == 0
    assert empty_analysis['total_donations'] == 0
    assert empty_analysis['total_revenue'] == 0.0
    assert empty_analysis['average_donation'] == 0.0
    assert len(empty_analysis['top_supporters']) == 0
    assert len(empty_analysis['daily_revenue']) == 0
    
    print(f"✓ Empty data analysis works correctly")
    
    # Test with sample donation data
    sample_donations = [
        {
            'supporter_id': 1,
            'supporter_name': 'John Doe',
            'amount': 25.00,
            'created_at': '2023-02-15T10:30:00Z'
        },
        {
            'supporter_id': 2,
            'supporter_name': 'Jane Smith',
            'amount': 50.00,
            'created_at': '2023-02-15T14:20:00Z'
        },
        {
            'supporter_id': 1,  # Same supporter as first donation
            'supporter_name': 'John Doe',
            'amount': 15.00,
            'created_at': '2023-02-16T09:15:00Z'
        },
        {
            'supporter_id': 3,
            'supporter_name': 'Bob Johnson',
            'amount': 100.00,
            'created_at': '2023-02-17T16:45:00Z'
        }
    ]
    
    analysis = generator.analyze_donations(sample_donations)
    
    # Verify the analysis results
    assert analysis['total_supporters'] == 4  # 4 donations total
    assert analysis['unique_supporters'] == 3  # 3 unique supporters
    assert analysis['total_donations'] == 4
    assert analysis['total_revenue'] == 190.00  # 25+50+15+100
    assert analysis['average_donation'] == 47.50  # 190/4
    assert len(analysis['top_supporters']) == 3  # We have 3 unique supporters
    assert analysis['daily_revenue']['2023-02-15'] == 75.00  # 25+50
    assert analysis['daily_revenue']['2023-02-16'] == 15.00
    assert analysis['daily_revenue']['2023-02-17'] == 100.00
    
    print(f"✓ Sample data analysis works correctly")
    
    # Test visualization creation (will create empty charts since no real data)
    daily_img, top_supporters_img = generator.create_visualizations(analysis, year, month)
    assert os.path.exists(daily_img)
    assert os.path.exists(top_supporters_img)
    
    print(f"✓ Visualization creation works correctly")
    
    # Test PDF generation
    pdf_path = generator.generate_pdf_report(analysis, year, month, daily_img, top_supporters_img)
    assert os.path.exists(pdf_path)
    
    print(f"✓ PDF generation works correctly")
    print(f"✓ Generated report: {pdf_path}")
    
    # Clean up test files
    os.remove(daily_img)
    os.remove(top_supporters_img)
    os.remove(pdf_path)
    os.rmdir("report_images")  # Remove the directory if it's empty
    
    print(f"✓ Test files cleaned up")
    
    print("\nAll basic functionality tests passed!")


def test_command_line_interface():
    """Test the command line interface by importing and checking the main function"""
    print("\nTesting command line interface...")
    
    # Import the main function and verify it exists
    from donation_report_generator import main as cli_main
    assert callable(cli_main)
    
    print("✓ Command line interface exists")
    

if __name__ == "__main__":
    print("Running tests for donation report generator...\n")
    
    try:
        test_basic_functionality()
        test_command_line_interface()
        
        print("\n✅ All tests passed! The donation report generator is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        raise