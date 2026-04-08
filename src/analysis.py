"""
Uber Rides Data Analysis Module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class UberDataAnalyzer:
    """Analyze Uber rides data for business insights"""
    
    def __init__(self, data_path):
        """Initialize the analyzer with data"""
        self.data = pd.read_csv(data_path)
        self._preprocess_data()
    
    def _preprocess_data(self):
        """Clean and preprocess the data"""
        # Convert date columns
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            self.data['hour'] = self.data['timestamp'].dt.hour
            self.data['day_of_week'] = self.data['timestamp'].dt.day_name()
            self.data['date'] = self.data['timestamp'].dt.date
            self.data['month'] = self.data['timestamp'].dt.month
        
        # Handle missing values
        self.data = self.data.fillna(0)
    
    def explore_data(self):
        """Basic data exploration"""
        print("Dataset Shape:", self.data.shape)
        print("\nFirst 5 rows:")
        print(self.data.head())
        print("\nBasic Statistics:")
        print(self.data.describe())
        print("\nMissing Values:")
        print(self.data.isnull().sum())
    
    def temporal_analysis(self):
        """Analyze temporal patterns"""
        if 'hour' not in self.data.columns:
            print("Timestamp column required")
            return
        
        # Hourly pattern
        hourly_counts = self.data['hour'].value_counts().sort_index()
        
        plt.figure(figsize=(14, 10))
        
        # Hourly rides
        plt.subplot(2, 2, 1)
        hourly_counts.plot(kind='bar', color='steelblue')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Rides')
        plt.title('Ride Demand by Hour')
        plt.grid(True, alpha=0.3)
        
        # Day of week pattern
        if 'day_of_week' in self.data.columns:
            plt.subplot(2, 2, 2)
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
            day_counts = self.data['day_of_week'].value_counts().reindex(day_order)
            day_counts.plot(kind='bar', color='coral')
            plt.xlabel('Day of Week')
            plt.ylabel('Number of Rides')
            plt.title('Ride Demand by Day of Week')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizations/temporal_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return hourly_counts
    
    def fare_analysis(self):
        """Analyze fare distribution and patterns"""
        if 'fare' not in self.data.columns:
            print("Fare column required")
            return
        
        plt.figure(figsize=(14, 5))
        
        # Fare distribution
        plt.subplot(1, 2, 1)
        self.data['fare'].hist(bins=50, color='skyblue', edgecolor='black')
        plt.xlabel('Fare Amount ($)')
        plt.ylabel('Frequency')
        plt.title('Fare Distribution')
        plt.grid(True, alpha=0.3)
        
        # Fare vs Distance
        if 'distance' in self.data.columns:
            plt.subplot(1, 2, 2)
            plt.scatter(self.data['distance'], self.data['fare'], alpha=0.5, color='green')
            plt.xlabel('Distance (km)')
            plt.ylabel('Fare Amount ($)')
            plt.title('Fare vs Distance')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizations/fare_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def geographic_analysis(self):
        """Analyze geographic patterns"""
        if 'pickup_latitude' not in self.data.columns:
            print("Geographic coordinates required")
            return
        
        # Popular pickup locations
        plt.figure(figsize=(10, 8))
        plt.scatter(
            self.data['pickup_longitude'], 
            self.data['pickup_latitude'],
            alpha=0.1,
            s=1,
            c='blue'
        )
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Geographic Distribution of Pickup Locations')
        plt.grid(True, alpha=0.3)
        plt.savefig('visualizations/geographic_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def surge_pricing_analysis(self):
        """Analyze surge pricing patterns"""
        if 'surge_multiplier' not in self.data.columns:
            print("Surge multiplier column required")
            return
        
        surge_data = self.data[self.data['surge_multiplier'] > 1]
        
        plt.figure(figsize=(14, 5))
        
        # Surge multiplier distribution
        plt.subplot(1, 2, 1)
        surge_data['surge_multiplier'].hist(bins=20, color='orange', edgecolor='black')
        plt.xlabel('Surge Multiplier')
        plt.ylabel('Frequency')
        plt.title('Surge Pricing Distribution')
        plt.grid(True, alpha=0.3)
        
        # Surge by hour
        if 'hour' in self.data.columns:
            plt.subplot(1, 2, 2)
            surge_by_hour = surge_data.groupby('hour')['surge_multiplier'].mean()
            surge_by_hour.plot(kind='bar', color='red')
            plt.xlabel('Hour of Day')
            plt.ylabel('Average Surge Multiplier')
            plt.title('Surge Pricing by Hour')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizations/surge_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = {
            'total_rides': len(self.data),
            'average_fare': self.data['fare'].mean() if 'fare' in self.data.columns else None,
            'median_fare': self.data['fare'].median() if 'fare' in self.data.columns else None,
            'peak_hour': self.data['hour'].value_counts().idxmax() if 'hour' in self.data.columns else None,
            'peak_day': self.data['day_of_week'].value_counts().idxmax() if 'day_of_week' in self.data.columns else None,
        }
        
        if 'distance' in self.data.columns:
            report['average_distance'] = self.data['distance'].mean()
            report['total_distance'] = self.data['distance'].sum()
        
        return report
