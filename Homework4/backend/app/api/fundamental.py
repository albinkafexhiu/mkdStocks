from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json
import glob
from datetime import datetime
from app.data.companies import COMPANY_SYMBOLS

router = APIRouter()

def get_latest_news_file() -> str:
    """Get the most recent analyzed news file"""
    files = glob.glob('analyzed_news_*.json')
    if not files:
        raise HTTPException(status_code=404, detail="No analyzed news data found")
    return max(files)

def get_symbol_for_company(company_name: str) -> str:
    """Get stock symbol for company name"""
    return COMPANY_SYMBOLS.get(company_name, company_name)

@router.get("/news/{symbol}")
def get_company_news(symbol: str) -> Dict[str, Any]:
    """
    Get analyzed news and sentiment for a specific company symbol
    """
    try:
        # Load latest analyzed news
        with open(get_latest_news_file(), 'r', encoding='utf-8') as f:
            all_news = json.load(f)
        
        # Find company by symbol
        company_news = None
        found_company = None
        
        # Look through all companies to find matching symbol
        for company_name, data in all_news.items():
            if get_symbol_for_company(company_name) == symbol:
                company_news = data
                found_company = company_name
                break
        
        if not company_news:
            raise HTTPException(status_code=404, detail=f"No news found for symbol {symbol}")
        
        return {
            "symbol": symbol,
            "company_name": found_company,
            "data": company_news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{symbol}/latest")
def get_latest_company_news(symbol: str, limit: int = 5) -> Dict[str, Any]:
    """
    Get most recent news articles for a company
    """
    try:
        full_news = get_company_news(symbol)
        articles = full_news["data"]["articles"]
        
        # Sort articles by date and get the most recent ones
        sorted_articles = sorted(articles, key=lambda x: x["date"], reverse=True)
        latest_articles = sorted_articles[:limit]
        
        return {
            "symbol": symbol,
            "company_name": full_news["company_name"],
            "latest_news": latest_articles,
            "overall_sentiment": full_news["data"]["overall_recommendation"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{symbol}/sentiment")
def get_company_sentiment(symbol: str) -> Dict[str, Any]:
    """
    Get overall sentiment analysis for a company
    """
    try:
        company_data = get_company_news(symbol)
        
        sentiment_data = {
            "symbol": symbol,
            "company_name": company_data["company_name"],
            "average_sentiment": company_data["data"]["average_sentiment"],
            "recommendation": company_data["data"]["overall_recommendation"],
            "article_count": len(company_data["data"]["articles"])
        }
        
        return sentiment_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/sentiment")
def get_market_sentiment() -> Dict[str, Any]:
    """
    Get overall market sentiment based on all companies
    """
    try:
        with open(get_latest_news_file(), 'r', encoding='utf-8') as f:
            all_news = json.load(f)
            
        buy_count = 0
        sell_count = 0
        hold_count = 0
        total_sentiment = 0
        company_count = 0
        
        for company, data in all_news.items():
            if data["average_sentiment"] > 0:  # Only count if we have sentiment data
                total_sentiment += data["average_sentiment"]
                company_count += 1
                
                if data["overall_recommendation"] == "BUY":
                    buy_count += 1
                elif data["overall_recommendation"] == "SELL":
                    sell_count += 1
                else:
                    hold_count += 1
        
        avg_market_sentiment = total_sentiment / company_count if company_count > 0 else 0
        
        return {
            "market_sentiment": avg_market_sentiment,
            "recommendations": {
                "buy": buy_count,
                "sell": sell_count,
                "hold": hold_count
            },
            "total_companies_analyzed": company_count,
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))