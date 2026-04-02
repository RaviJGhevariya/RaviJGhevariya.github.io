#!/usr/bin/env python3
"""
Sample Monthly Donation Report Generator using mock data
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Tuple, Optional

import requests
import matplotlib.pyplot as plt
from fpdf import FPDF


class SampleDonationReportGenerator:
    """
    Class for generating sample monthly donation reports using mock data
    """
    
    def __init__(self):
        pass  # No API token needed for sample data
        
    def get_mock_donations_for_month(self, year: int, month: int) -> List[Dict]:
        """
        Generate mock donation data for a specific month
        """
        print(f"Generating mock donations for {year}-{month:02d}...")
        
        # Generate some sample donation data
        mock_donations = []
        
        # Add sample supporters
        supporters = [
            {'id': 1, 'name': 'Alice Johnson'},
            {'id': 2, 'name': 'Bob Smith'},
            {'id': 3, 'name': 'Carol Davis'},
            {'id': 4, 'name': 'David Wilson'},
            {'id': 5, 'name': 'Emma Brown'},
            {'id': 6, 'name': 'Frank Miller'},
            {'id': 7, 'name': 'Grace Lee'},
            {'id': 8, 'name': 'Henry Taylor'},
            {'id': 9, 'name': 'Ivy Chen'},
            {'id': 10, 'name': 'Jack Anderson'}
        ]
        
        # Calculate number of days in the month
        num_days = calendar.monthrange(year, month)[1]
        
        # Generate mock donations for each day
        for day in range(1, min(num_days + 1, 15)):  # Just first 15 days for sample
            # Random number of donations per day (between 2-8)
            num_donations_today = (day % 6) + 2  # Varies by day
            
            for _ in range(num_donations_today):
                # Select a random supporter
                import random
                supporter = supporters[random.randint(0, len(supporters) - 1)]
                
                # Random donation amount between $5 and $100
                amount = round(random.uniform(5.0, 100.0), 2)
                
                # Create donation record
                donation = {
                    'supporter_id': supporter['id'],
                    'supporter_name': supporter['name'],
                    'amount': amount,
                    'created_at': f'{year}-{month:02d}-{day:02d}T{random.randint(8, 22):02d}:{random.randint(0, 59):02d}:00Z'
                }
                mock_donations.append(donation)
        
        return mock_donations
    
    def analyze_donations(self, donations: List[Dict]) -> Dict:
        """
        Analyze donation data to extract key statistics
        """
        if not donations:
            return {
                'total_supporters': 0,
                'unique_supporters': 0,
                'total_donations': 0,
                'total_revenue': 0.0,
                'average_donation': 0.0,
                'top_supporters': [],
                'daily_revenue': {}
            }
        
        # Extract supporter IDs and donation amounts
        supporter_ids = []
        donation_amounts = []
        daily_revenue = {}
        
        for donation in donations:
            supporter_id = donation.get('supporter_id')
            amount = float(donation.get('amount', 0))
            created_at = donation.get('created_at', '')
            
            supporter_ids.append(supporter_id)
            donation_amounts.append(amount)
            
            # Group by date for daily revenue
            if created_at:
                date_str = created_at.split('T')[0]  # Extract date part from ISO format
                if date_str in daily_revenue:
                    daily_revenue[date_str] += amount
                else:
                    daily_revenue[date_str] = amount
        
        # Calculate statistics
        total_supporters = len(supporter_ids)
        unique_supporters = len(set(supporter_ids)) if supporter_ids else 0
        total_donations = len(donations)
        total_revenue = sum(donation_amounts)
        average_donation = total_revenue / total_donations if total_donations > 0 else 0.0
        
        # Get top supporters
        supporter_totals = {}
        for donation in donations:
            supporter_id = donation.get('supporter_id')
            supporter_name = donation.get('supporter_name', f'Supporter {supporter_id}')
            amount = float(donation.get('amount', 0))
            
            if supporter_id in supporter_totals:
                supporter_totals[supporter_id]['total'] += amount
                supporter_totals[supporter_id]['count'] += 1
            else:
                supporter_totals[supporter_id] = {
                    'name': supporter_name,
                    'total': amount,
                    'count': 1
                }
        
        # Sort supporters by total donation amount
        sorted_supporters = sorted(
            supporter_totals.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        top_supporters = [
            {
                'name': supporter_data['name'],
                'total_donated': supporter_data['total'],
                'donation_count': supporter_data['count']
            }
            for _, supporter_data in sorted_supporters[:10]
        ]
        
        return {
            'total_supporters': total_supporters,
            'unique_supporters': unique_supporters,
            'total_donations': total_donations,
            'total_revenue': total_revenue,
            'average_donation': average_donation,
            'top_supporters': top_supporters,
            'daily_revenue': daily_revenue
        }
    
    def create_visualizations(self, analysis_data: Dict, year: int, month: int) -> Tuple[str, str]:
        """
        Create visualization charts and save them as images
        Returns paths to the saved images
        """
        # Create directory for images if it doesn't exist
        img_dir = "report_images"
        os.makedirs(img_dir, exist_ok=True)
        
        # Daily Revenue Chart
        daily_revenue_path = os.path.join(img_dir, f"daily_revenue_{year}_{month}_sample.png")
        if analysis_data['daily_revenue']:
            dates = list(analysis_data['daily_revenue'].keys())
            revenues = list(analysis_data['daily_revenue'].values())
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, revenues, marker='o')
            plt.title(f'Daily Revenue - {calendar.month_name[month]} {year} (Sample Data)')
            plt.xlabel('Date')
            plt.ylabel('Revenue ($)')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(daily_revenue_path)
            plt.close()
        else:
            # Create an empty chart image
            plt.figure(figsize=(12, 6))
            plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
            plt.title(f'Daily Revenue - {calendar.month_name[month]} {year} (Sample Data)')
            plt.savefig(daily_revenue_path)
            plt.close()
        
        # Top Supporters Chart
        top_supporters_path = os.path.join(img_dir, f"top_supporters_{year}_{month}_sample.png")
        if analysis_data['top_supporters']:
            names = [s['name'] for s in analysis_data['top_supporters']]
            totals = [s['total_donated'] for s in analysis_data['top_supporters']]
            
            plt.figure(figsize=(12, 8))
            bars = plt.barh(names, totals)
            plt.title(f'Top 10 Supporters - {calendar.month_name[month]} {year} (Sample Data)')
            plt.xlabel('Total Donated ($)')
            plt.gca().invert_yaxis()  # Show highest donors at top
            
            # Add value labels on bars
            for bar, total in zip(bars, totals):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height()/2, f'${total:.2f}', 
                        ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(top_supporters_path)
            plt.close()
        else:
            # Create an empty chart image
            plt.figure(figsize=(12, 8))
            plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
            plt.title(f'Top 10 Supporters - {calendar.month_name[month]} {year} (Sample Data)')
            plt.savefig(top_supporters_path)
            plt.close()
        
        return daily_revenue_path, top_supporters_path
    
    def generate_pdf_report(self, analysis_data: Dict, year: int, month: int, 
                           daily_revenue_img: str, top_supporters_img: str) -> str:
        """
        Generate the final PDF report
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'SAMPLE Monthly Donation Report - {calendar.month_name[month]} {year}', 0, 1, 'C')
        pdf.ln(5)
        
        # Add note about sample data
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, '(This report uses sample data for demonstration purposes)', 0, 1, 'C')
        pdf.ln(5)
        
        # Statistics section
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Key Statistics', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        stats = [
            f'Total Supporters: {analysis_data["total_supporters"]}',
            f'Unique Supporters: {analysis_data["unique_supporters"]}',
            f'Total Donations: {analysis_data["total_donations"]}',
            f'Total Revenue: ${analysis_data["total_revenue"]:,.2f}',
            f'Average Donation: ${analysis_data["average_donation"]:,.2f}'
        ]
        
        for stat in stats:
            pdf.cell(0, 8, stat, 0, 1)
        
        pdf.ln(10)
        
        # Daily Revenue Chart
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Daily Revenue', 0, 1)
        pdf.image(daily_revenue_img, x=10, y=None, w=190)
        pdf.ln(10)
        
        # Top Supporters Section
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Top 10 Supporters', 0, 1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 10, 'Supporter Name', 1)
        pdf.cell(50, 10, 'Total Donated', 1)
        pdf.cell(40, 10, 'Donation Count', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 10)
        for supporter in analysis_data['top_supporters']:
            pdf.cell(60, 8, supporter['name'], 1)
            pdf.cell(50, 8, f'${supporter["total_donated"]:,.2f}', 1)
            pdf.cell(40, 8, str(supporter['donation_count']), 1)
            pdf.ln()
        
        # Top Supporters Chart
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Top Supporters Visualization', 0, 1)
        pdf.image(top_supporters_img, x=10, y=None, w=190)
        
        # Output file
        filename = f"sample_donation_report_{year}_{month:02d}.pdf"
        pdf.output(filename)
        return filename


def main():
    parser = argparse.ArgumentParser(description='Generate sample monthly donation report using mock data')
    parser.add_argument('--year', type=int, required=True, help='Year to generate report for')
    parser.add_argument('--month', type=int, required=True, help='Month to generate report for (1-12)')
    
    args = parser.parse_args()
    
    if not (1 <= args.month <= 12):
        print("Error: Month must be between 1 and 12")
        sys.exit(1)
    
    # Validate date
    try:
        datetime(args.year, args.month, 1)
    except ValueError:
        print(f"Error: Invalid date {args.year}-{args.month}")
        sys.exit(1)
    
    print(f"Generating sample donation report for {calendar.month_name[args.month]} {args.year}...")
    
    # Initialize the sample report generator
    generator = SampleDonationReportGenerator()
    
    try:
        # Get mock donations for the month
        donations = generator.get_mock_donations_for_month(args.year, args.month)
        print(f"Generated {len(donations)} mock donations")
        
        # Analyze the data
        analysis = generator.analyze_donations(donations)
        print("Analysis complete")
        
        # Create visualizations
        daily_revenue_img, top_supporters_img = generator.create_visualizations(analysis, args.year, args.month)
        print(f"Visualizations created: {daily_revenue_img}, {top_supporters_img}")
        
        # Generate PDF report
        pdf_filename = generator.generate_pdf_report(analysis, args.year, args.month, 
                                                     daily_revenue_img, top_supporters_img)
        print(f"Sample report generated successfully: {pdf_filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()