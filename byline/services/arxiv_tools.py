import logging
import arxiv
import tempfile
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
import PyPDF2
import io
import requests

class ArxivTools:
    """Tools for searching and downloading papers from arXiv"""
    
    def __init__(self):
        self.client = arxiv.Client()
        logging.info("ArxivTools initialized")
    
    def search_papers_by_time_interval(self, query: str, days_back: int = 1, max_results: int = 10) -> Dict[str, Any]:
        """
        Search for papers within a specified time interval
        
        Args:
            query: Search query string
            days_back: Number of days to search back from today
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        logging.info(f"Searching arXiv for query: '{query}', days_back: {days_back}, max_results: {max_results}")
        
        try:
            # Create date range query
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for arXiv API (YYYYMMDD format)
            start_date_str = start_date.strftime("%Y%m%d")
            end_date_str = end_date.strftime("%Y%m%d")
            
            # Construct search query with date range
            date_query = f"submittedDate:[{start_date_str}* TO {end_date_str}*]"
            if query:
                full_query = f"{query} AND {date_query}"
            else:
                full_query = date_query
            
            # Create search
            search = arxiv.Search(
                query=full_query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            # Execute search
            results = list(self.client.results(search))
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.entry_id,
                    "title": result.title,
                    "authors": [str(author) for author in result.authors],
                    "summary": result.summary,
                    "published": result.published.isoformat(),
                    "updated": result.updated.isoformat(),
                    "categories": result.categories,
                    "pdf_url": result.pdf_url,
                    "primary_category": result.primary_category
                })
            
            logging.info(f"Found {len(formatted_results)} papers")
            return {
                "results": formatted_results,
                "total_found": len(formatted_results),
                "search_query": full_query,
                "date_range": f"{start_date_str} to {end_date_str}"
            }
            
        except Exception as e:
            logging.error(f"Error searching arXiv: {str(e)}")
            return {
                "error": str(e),
                "results": [],
                "total_found": 0
            }