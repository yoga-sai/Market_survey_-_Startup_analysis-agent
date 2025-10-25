"""
Funding Retriever Tool for Market Intelligence Research Agent.

This tool retrieves funding data for companies using the Crunchbase dataset.
"""
import pandas as pd
import os
from typing import List, Dict, Any

class FundingRetriever:
    """
    Retrieves funding data for companies using the Crunchbase dataset.
    """
    
    def __init__(self, dataset_path: str = "../data/crunchbase_investments.csv"):
        """
        Initialize the funding retriever with the dataset path.
        
        Args:
            dataset_path: Path to the Crunchbase dataset CSV
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
    
    def get_funding_data(self, companies: List[str]) -> Dict[str, Any]:
        """
        Retrieve funding data for the specified companies.
        
        Args:
            companies: List of company names to search for
            
        Returns:
            Dictionary with funding data for each company
        """
        if self.df is None:
            self.load_data()
        
        funding_data = {
            "companies": {},
            "summary": {
                "total_funding": 0,
                "avg_funding": 0,
                "funding_rounds": 0
            }
        }
        
        total_funding = 0
        total_rounds = 0
        
        for company in companies:
            # Case-insensitive partial matching
            company_mask = self.df['company_name'].str.lower().str.contains(
                company.lower(), na=False
            )
            
            company_df = self.df[company_mask]
            
            if not company_df.empty:
                # Group by funding round
                rounds = []
                for _, row in company_df.iterrows():
                    round_data = {
                        "round_type": row.get('funding_round_type', 'Unknown'),
                        "amount": row.get('raised_amount_usd', 0),
                        "date": row.get('funded_at', 'Unknown'),
                        "investors": row.get('investor_names', '').split(',') if pd.notna(row.get('investor_names', '')) else []
                    }
                    rounds.append(round_data)
                    
                    # Add to totals if amount is available
                    if pd.notna(row.get('raised_amount_usd', 0)):
                        total_funding += float(row.get('raised_amount_usd', 0))
                        total_rounds += 1
                
                # Calculate company total funding
                company_total = sum(round_data['amount'] for round_data in rounds if isinstance(round_data['amount'], (int, float)))
                
                funding_data["companies"][company] = {
                    "total_funding": company_total,
                    "rounds": rounds,
                    "latest_round": rounds[-1] if rounds else None,
                    "first_funding": rounds[0] if rounds else None
                }
            else:
                # No data found for this company
                funding_data["companies"][company] = {
                    "total_funding": 0,
                    "rounds": [],
                    "latest_round": None,
                    "first_funding": None
                }
        
        # Calculate summary statistics
        num_companies = len([c for c in funding_data["companies"].values() if c["total_funding"] > 0])
        
        funding_data["summary"]["total_funding"] = total_funding
        funding_data["summary"]["funding_rounds"] = total_rounds
        funding_data["summary"]["avg_funding"] = total_funding / num_companies if num_companies > 0 else 0
        
        return funding_data
    
    def _create_mock_data(self) -> pd.DataFrame:
        """
        Create mock data for testing when the dataset is not available.
        
        Returns:
            DataFrame with mock data
        """
        data = {
            'company_name': [
                'HealthTrack', 'HealthTrack', 'MedConnect', 'WellnessAI', 'FemHealth', 
                'FemHealth', 'FemHealth', 'FitTech', 'FinSmart', 'PayEasy'
            ],
            'funding_round_type': [
                'Seed', 'Series A', 'Seed', 'Series A', 'Seed',
                'Series A', 'Series B', 'Seed', 'Seed', 'Series A'
            ],
            'raised_amount_usd': [
                500000, 2000000, 750000, 3200000, 600000,
                2500000, 8000000, 1200000, 800000, 2700000
            ],
            'funded_at': [
                '2019-05-15', '2021-08-22', '2018-11-30', '2021-03-10', '2017-09-05',
                '2019-02-18', '2022-01-30', '2020-07-12', '2019-04-25', '2020-10-08'
            ],
            'investor_names': [
                'Angel Investors', 'Venture Fund A, Growth Capital', 'Seed Fund X', 
                'Tech Ventures, AI Capital', 'Women Health Fund',
                'Venture Fund B, Health Investors', 'Growth Fund C, Major Capital', 
                'Fitness Angels', 'Fintech Seed Fund', 'Payment Ventures, Capital X'
            ]
        }
        
        return pd.DataFrame(data)