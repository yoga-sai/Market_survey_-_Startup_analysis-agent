"""
RAG Query Tool for Market Intelligence Research Agent.

This tool performs semantic search using a vector database for retrieval-augmented generation.
"""
import os
import numpy as np
from typing import List, Dict, Any, Optional

class RAGQueryTool:
    """
    Performs semantic search using a vector database for retrieval-augmented generation.
    """
    
    def __init__(self, embeddings_dir: str = "../vector_db/embeddings_store"):
        """
        Initialize the RAG query tool.
        
        Args:
            embeddings_dir: Directory containing vector embeddings
        """
        self.embeddings_dir = embeddings_dir
        
    def query(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Query the vector database for relevant information.
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with similarity scores
        """
        # In a production system, this would use a real vector database
        # For now, we'll return mock results
        
        domain = self._extract_domain(query)
        
        return self._get_mock_results(domain, top_k)
    
    def _extract_domain(self, query: str) -> str:
        """
        Extract domain from query for generating relevant mock results.
        
        Args:
            query: Query string
            
        Returns:
            Domain extracted from query
        """
        domains = ["health", "finance", "education", "e-commerce", "social"]
        
        for domain in domains:
            if domain.lower() in query.lower():
                return domain
        
        # Default domain if none found
        return "technology"
    
    def _get_mock_results(self, domain: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Generate mock results for testing.
        
        Args:
            domain: Domain to generate results for
            top_k: Number of results to return
            
        Returns:
            List of mock results
        """
        mock_data = {
            "health": [
                {
                    "content": "The health tech market is growing rapidly, with a focus on personalized medicine and AI-driven diagnostics. Key success factors include user experience, data privacy, and integration with existing healthcare systems.",
                    "source": "Healthcare Industry Report 2023",
                    "similarity": 0.92
                },
                {
                    "content": "Women's health startups raised over $1.3 billion in funding in 2022, with menstrual health tracking apps being a significant category. The most successful apps combine tracking with community features and personalized insights.",
                    "source": "FemTech Market Analysis",
                    "similarity": 0.88
                },
                {
                    "content": "Health app retention rates average 23% after 30 days, significantly lower than other app categories. Apps that incorporate social features and gamification show 45% higher retention rates.",
                    "source": "Mobile Health App Engagement Study",
                    "similarity": 0.85
                },
                {
                    "content": "Regulatory compliance is a major challenge for health tech startups. Successful companies allocate 15-20% of their initial budget to compliance and privacy measures.",
                    "source": "Health Tech Startup Guide",
                    "similarity": 0.82
                }
            ],
            "finance": [
                {
                    "content": "Fintech adoption rates have reached 64% globally, with highest penetration in money transfer and payments. Emerging markets show faster adoption than developed markets.",
                    "source": "Global Fintech Adoption Index",
                    "similarity": 0.91
                },
                {
                    "content": "Successful fintech startups focus on solving specific pain points rather than offering comprehensive solutions initially. The 'land and expand' strategy has proven most effective for market penetration.",
                    "source": "Fintech Success Patterns",
                    "similarity": 0.87
                },
                {
                    "content": "Regulatory technology (RegTech) is the fastest growing fintech subsector, with a CAGR of 25.5% projected through 2025.",
                    "source": "Fintech Sector Analysis",
                    "similarity": 0.84
                }
            ],
            "education": [
                {
                    "content": "EdTech funding reached $16.1 billion in 2020, with K-12 and enterprise learning solutions receiving the largest share. Successful startups demonstrate measurable learning outcomes.",
                    "source": "EdTech Investment Report",
                    "similarity": 0.93
                },
                {
                    "content": "Personalized learning platforms show 40% better engagement than traditional online courses. Adaptive learning algorithms and spaced repetition are key technological differentiators.",
                    "source": "Online Education Effectiveness Study",
                    "similarity": 0.89
                },
                {
                    "content": "The B2B education market is growing faster than B2C, with enterprise training solutions commanding higher customer lifetime values and lower acquisition costs.",
                    "source": "Education Market Trends",
                    "similarity": 0.86
                }
            ],
            "e-commerce": [
                {
                    "content": "Direct-to-consumer (DTC) brands with strong community engagement show 3x higher customer lifetime value. Social commerce integration is a key success factor.",
                    "source": "E-commerce Business Models Analysis",
                    "similarity": 0.94
                },
                {
                    "content": "Marketplace startups face a critical 'chicken and egg' problem. Successful platforms focus on supply-side acquisition first, ensuring quality before scaling demand.",
                    "source": "Marketplace Startup Playbook",
                    "similarity": 0.90
                },
                {
                    "content": "Subscription e-commerce has grown by 100% annually over the past five years. Curation and personalization are the primary drivers of customer satisfaction.",
                    "source": "Subscription Economy Report",
                    "similarity": 0.87
                }
            ],
            "social": [
                {
                    "content": "Niche social platforms show higher engagement rates than general platforms. Communities focused on specific interests have 5x the engagement and 3x the retention.",
                    "source": "Social Platform Engagement Study",
                    "similarity": 0.95
                },
                {
                    "content": "Content moderation costs average 20% of operating expenses for social platforms. AI-based moderation can reduce this to 8-12% while maintaining quality.",
                    "source": "Social Media Operations Analysis",
                    "similarity": 0.91
                },
                {
                    "content": "Social platforms with integrated creator monetization tools show 70% higher content production rates and 50% higher user retention.",
                    "source": "Creator Economy Impact Report",
                    "similarity": 0.88
                }
            ],
            "technology": [
                {
                    "content": "SaaS startups with product-led growth strategies show 2x faster revenue growth compared to sales-led companies in the early stages.",
                    "source": "SaaS Growth Strategies Report",
                    "similarity": 0.92
                },
                {
                    "content": "AI startups require 30% more capital to reach product-market fit compared to traditional software startups, but achieve 2.5x higher valuations at Series A.",
                    "source": "AI Startup Benchmarks",
                    "similarity": 0.89
                },
                {
                    "content": "Open source business models are gaining traction, with 70% of enterprise software companies now incorporating open source components in their strategy.",
                    "source": "Open Source Business Models Analysis",
                    "similarity": 0.86
                }
            ]
        }
        
        # Return results for the specified domain
        return mock_data.get(domain.lower(), mock_data["technology"])[:top_k]