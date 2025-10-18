"""
Competitor Finder Tool for Market Intelligence Research Agent.

This tool finds competitors in a specific domain using the Indian Startup dataset.
"""
import pandas as pd
import os
from typing import List, Dict, Any, Optional

class CompetitorFinder:
    """
    Finds competitors in a specific domain using the Indian Startup dataset.
    """
    
    def __init__(self, dataset_path: str = "../data/indian_startup_dataset.csv"):
        """
        Initialize the competitor finder with the dataset path.
        
        Args:
            dataset_path: Path to the Indian Startup dataset CSV
        """
        self.dataset_path = dataset_path
        self.df = None
        
    def load_data(self) -> None:
        """
        Load the dataset if it exists, otherwise create a mock dataset.
        """
        if os.path.exists(self.dataset_path):
            self.df = pd.read_csv(self.dataset_path)
        else:
            # Create mock data for testing
            self.df = self._create_mock_data()
    
    def find_competitors(self, domain: str, features: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Find competitors in the specified domain with similar features.
        
        Args:
            domain: Business domain to search for
            features: List of key features to match
            
        Returns:
            List of competitor information dictionaries
        """
        if self.df is None:
            self.load_data()
        
        # Filter by domain
        domain_keywords = self._get_domain_keywords(domain)
        domain_mask = self.df['Industry'].str.lower().apply(
            lambda x: any(keyword in str(x).lower() for keyword in domain_keywords)
        )
        
        domain_df = self.df[domain_mask]
        
        # If no competitors found, return empty list
        if domain_df.empty:
            return []
        
        # If features provided, try to match them
        if features and len(features) > 0:
            # This would be more sophisticated in a real implementation
            # For now, we'll just do simple keyword matching
            feature_keywords = [f.lower() for f in features]
            
            # Check if any feature keywords appear in the description
            if 'Description' in domain_df.columns:
                feature_mask = domain_df['Description'].str.lower().apply(
                    lambda x: any(keyword in str(x).lower() for keyword in feature_keywords)
                )
                feature_df = domain_df[feature_mask]
                
                # If we found matches with features, use that
                if not feature_df.empty:
                    domain_df = feature_df
        
        # Convert to list of dictionaries
        competitors = []
        for _, row in domain_df.head(5).iterrows():
            competitor = {
                "name": row.get('Startup Name', 'Unknown'),
                "features": self._extract_features(row),
                "audience": self._extract_audience(row),
                "usp": self._extract_usp(row),
                "funding": row.get('Amount', 'Unknown'),
                "year_founded": row.get('Year', 'Unknown')
            }
            competitors.append(competitor)
        
        return competitors
    
    def _get_domain_keywords(self, domain: str) -> List[str]:
        """
        Get keywords related to a domain for better matching.
        
        Args:
            domain: Business domain
            
        Returns:
            List of related keywords
        """
        domain_map = {
            "health": ["health", "healthcare", "medical", "wellness", "fitness", "menstrual", "femtech"],
            "finance": ["finance", "fintech", "banking", "investment", "money", "payment"],
            "education": ["education", "edtech", "learning", "teaching", "school", "course"],
            "e-commerce": ["ecommerce", "e-commerce", "retail", "shop", "store", "marketplace"],
            "social": ["social", "community", "network", "connect", "share"]
        }
        
        return domain_map.get(domain.lower(), [domain.lower()])
    
    def _extract_features(self, row: pd.Series) -> List[str]:
        """
        Extract features from a competitor row.
        
        Args:
            row: DataFrame row for a competitor
            
        Returns:
            List of features
        """
        # In a real implementation, this would parse the description
        # For now, return placeholder features
        return ["Feature 1", "Feature 2", "Feature 3"]
    
    def _extract_audience(self, row: pd.Series) -> str:
        """
        Extract target audience from a competitor row.
        
        Args:
            row: DataFrame row for a competitor
            
        Returns:
            Target audience description
        """
        # In a real implementation, this would parse the description
        # For now, return a placeholder
        return "General users in this domain"
    
    def _extract_usp(self, row: pd.Series) -> str:
        """
        Extract unique selling proposition from a competitor row.
        
        Args:
            row: DataFrame row for a competitor
            
        Returns:
            USP description
        """
        # In a real implementation, this would parse the description
        # For now, return a placeholder
        return "Unique approach to solving domain problems"
    
    def _create_mock_data(self) -> pd.DataFrame:
        """
        Create mock data for testing when the dataset is not available.
        
        Returns:
            DataFrame with mock data
        """
        data = {
            'Startup Name': [
                'HealthTrack', 'MedConnect', 'WellnessAI', 'FemHealth', 'FitTech',
                'FinSmart', 'PayEasy', 'InvestPro', 'BankDigital', 'MoneyWise',
                'EduLearn', 'CourseHub', 'SchoolDigital', 'TeachTech', 'LearnAI'
            ],
            'Industry': [
                'Health', 'Healthcare', 'Wellness', 'FemTech', 'Fitness',
                'FinTech', 'Payments', 'Investments', 'Banking', 'Personal Finance',
                'EdTech', 'Online Courses', 'School Management', 'Teaching Tools', 'AI Learning'
            ],
            'Description': [
                'Health tracking app with AI features',
                'Connecting patients with doctors',
                'AI-powered wellness recommendations',
                'Women\'s health tracking and community',
                'Fitness tracking with social features',
                'Smart financial planning tools',
                'Easy payment solutions for businesses',
                'Investment platform for retail investors',
                'Digital banking solutions',
                'Personal finance management',
                'Online learning platform',
                'Marketplace for online courses',
                'Digital solutions for schools',
                'Tools for teachers and educators',
                'AI-powered learning assistant'
            ],
            'Amount': [
                '$2.5M', '$1.8M', '$3.2M', '$4.1M', '$1.2M',
                '$5.5M', '$2.7M', '$8.3M', '$12.5M', '$3.8M',
                '$4.2M', '$2.9M', '$1.5M', '$3.3M', '$6.7M'
            ],
            'Year': [
                2020, 2019, 2021, 2018, 2022,
                2019, 2020, 2018, 2017, 2021,
                2020, 2019, 2021, 2018, 2022
            ]
        }
        
        return pd.DataFrame(data)