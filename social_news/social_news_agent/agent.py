# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk import Agent
from google.genai import types


async def get_social_media_data(topic: str = "all") -> str:
    """Get current social media posts and trending topics for Bangalore.
    
    Args:
        topic: The topic to filter by. Options: "traffic", "weather", "tech", "food", "general", or "all" for all topics.
    
    Returns:
        A string with current social media activity and trends.
    """
    social_data = {
        "trending_topics": ["#BangaloreTraffic", "#PowerCut", "#AirQuality", "#BangaloreWeather", "#TechCity", "#BLRMusic", "#NammaMetro"],
        "recent_posts": [
            {
                "username": "FrustratedCommuter",
                "text": "Another hour stuck in Bangalore traffic. This is getting ridiculous! 😠 #TrafficNightmare #BangaloreProblems",
                "platform": "Twitter",
                "retweets": 30,
                "category": "traffic",
                "created_at": "2025-07-26T20:32:26Z",
                "time_ago": "2 hours ago"
            },
            {
                "username": "MusicExplorer", 
                "text": "Bangalore's music scene is so diverse. Caught an amazing indie band performance tonight! #BLRMusic #LiveMusic",
                "platform": "Twitter",
                "retweets": 13,
                "category": "entertainment",
                "created_at": "2025-07-26T11:24:56Z",
                "time_ago": "11 hours ago"
            },
            {
                "username": "TechEnthusiast",
                "text": "Excited for the tech meetup tonight in Electronic City! #BangaloreTech #StartupIndia",
                "platform": "Twitter",
                "retweets": 12,
                "category": "tech",
                "created_at": "2025-07-26T15:15:47Z",
                "time_ago": "7 hours ago"
            },
            {
                "username": "BLRFoodie",
                "text": "Another fantastic evening at a microbrewery in Indiranagar. Bangalore's craft beer scene is booming! #CraftBeerBLR #Microbrewery",
                "platform": "Twitter",
                "retweets": 10,
                "category": "food",
                "created_at": "2025-07-26T11:17:35Z",
                "time_ago": "11 hours ago"
            },
            {
                "username": "WorkFromHomeBLR",
                "text": "Power cuts are becoming a daily occurrence in Bangalore. So frustrating when you're trying to work. #PowerCut #BLRProblems", 
                "platform": "Twitter",
                "retweets": 20,
                "category": "infrastructure",
                "created_at": "2025-07-26T17:05:44Z",
                "time_ago": "5 hours ago"
            },
            {
                "username": "NatureLoverBLR",
                "text": "The lakes in Bangalore need urgent attention. So much pollution! #SaveLakes #BengaluruEnvironment",
                "platform": "Twitter",
                "retweets": 25,
                "category": "environment",
                "created_at": "2025-07-26T17:24:27Z",
                "time_ago": "5 hours ago"
            },
            {
                "username": "RoadRageBLR",
                "text": "Another flat tire thanks to Bangalore's roads. This is getting ridiculous. #PotholeProblems #Bengaluru",
                "platform": "Twitter",
                "retweets": 30,
                "category": "infrastructure",
                "created_at": "2025-07-26T02:14:04Z",
                "time_ago": "20 hours ago"
            },
            {
                "username": "TechRecruiterBLR",
                "text": "The tech talent pool in Bangalore is truly world-class. Proud to be part of it! #BangaloreTech #GlobalTalent",
                "platform": "Twitter",
                "retweets": 22,
                "category": "tech",
                "created_at": "2025-07-26T18:39:19Z",
                "time_ago": "4 hours ago"
            }
        ]
    }
    
    # Filter by topic if specified
    if topic != "all":
        filtered_posts = [post for post in social_data["recent_posts"] if post["category"] == topic]
        if filtered_posts:
            social_data["recent_posts"] = filtered_posts
    
    result = f"Trending in Bangalore: {', '.join(social_data['trending_topics'][:5])}\n\n"
    result += "Recent Social Media Activity:\n"
    for post in social_data['recent_posts'][:6]:
        result += f"@{post['username']} ({post['platform']}) - {post['time_ago']}:\n"
        result += f"   {post['text']}\n"
        result += f"   Retweets: {post['retweets']} | Posted: {post['created_at']}\n\n"
    
    return result


async def get_news_articles(category: str = "all", include_breaking: bool = True) -> str:
    """Get current news articles for Bangalore, including breaking news.
    
    Args:
        category: The category to filter by. Options: "technology", "business", "healthcare", "education", "culture", "governance", or "all" for all categories.
        include_breaking: Whether to include breaking news at the top of the results.
    
    Returns:
        A string with current news articles.
    """
    # Single news article
    news_data = {
        "article": {
            "title": "🔴 BBMP Announces New Digital Governance Platform",
            "description": "Citizens can now access all municipal services through a single digital platform. This groundbreaking initiative will streamline civic services and improve transparency in municipal operations across Bangalore.",
            "author": "Civic Reporter",
            "source": "BBMP Official",
            "time": "8:00 PM",
            "date": "2025-07-26",
            "category": "governance"
        }
    }
    
    # Return the single news article
    article = news_data["article"]
    
    # Filter by category if specified and it doesn't match
    if category != "all" and article["category"] != category:
        return f"No news articles found for category: {category}"
    
    result = "📰 Latest News from Bengaluru:\n\n"
    result += f"• {article['title']}\n"
    result += f"  {article['description']}\n"
    result += f"  Source: {article['source']} | Category: {article['category'].title()}\n"
    result += f"  Date: {article['date']} | Time: {article['time']}\n"
    result += f"  Author: {article['author']}\n"
    
    return result


async def get_news_by_area(area: str = "bangalore") -> str:
    """Get news articles specific to certain areas in Bangalore.
    
    Args:
        area: The area to get news for (e.g., "koramangala", "indiranagar", "whitefield", "electronic_city")
    
    Returns:
        A string with area-specific news.
    """
    area_news = {
        "koramangala": [
            {
                "title": "New Co-working Spaces Open in Koramangala",
                "description": "Several new co-working facilities cater to the growing startup community",
                "time": "2:30 PM",
                "date": "2025-07-26",
                "source": "Bangalore Mirror"
            },
            {
                "title": "Koramangala Gets New Cultural Center",
                "description": "A multi-purpose cultural space opens to promote local arts and events",
                "time": "10:15 AM",
                "date": "2025-07-26",
                "source": "Deccan Herald"
            }
        ],
        "indiranagar": [
            {
                "title": "Indiranagar's Nightlife Scene Expands",
                "description": "New restaurants and pubs add to the area's vibrant entertainment options",
                "time": "4:45 PM",
                "date": "2025-07-26",
                "source": "Bangalore Times"
            },
            {
                "title": "Heritage Building Restoration in Indiranagar",
                "description": "Historic structures being preserved while adding modern amenities",
                "time": "9:20 AM",
                "date": "2025-07-26",
                "source": "The Hindu"
            }
        ],
        "electronic_city": [
            {
                "title": "Electronic City Sees Major Tech Expansion",
                "description": "Multiple IT companies announce new campuses and job opportunities",
                "time": "1:00 PM",
                "date": "2025-07-26",
                "source": "Economic Times"
            },
            {
                "title": "New Educational Institute Opens in Electronic City",
                "description": "Advanced technology training center launches to meet industry demands",
                "time": "11:30 AM",
                "date": "2025-07-26",
                "source": "Business Standard"
            }
        ],
        "whitefield": [
            {
                "title": "Whitefield's IT Corridor Gets Infrastructure Boost",
                "description": "New roads and utilities enhance connectivity for tech workers",
                "time": "3:20 PM",
                "date": "2025-07-26",
                "source": "Times of India"
            },
            {
                "title": "Shopping Mall Complex Opens in Whitefield",
                "description": "Large retail destination provides shopping and entertainment options",
                "time": "8:45 AM",
                "date": "2025-07-26",
                "source": "Bangalore Mirror"
            }
        ]
    }
    
    area_lower = area.lower()
    if area_lower not in area_news:
        return f"No specific news available for {area}. Please try: koramangala, indiranagar, electronic_city, or whitefield."
    
    result = f"📍 News from {area.title()}:\n\n"
    for news in area_news[area_lower]:
        result += f"• {news['title']}\n"
        result += f"  {news['description']}\n"
        result += f"  Source: {news['source']} | Date: {news['date']} | Time: {news['time']}\n\n"
    
    return result


root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='social_news_agent',
    description='Combined social media and news agent that provides social media posts, trending topics, news articles with breaking news, and area-specific updates for Bangalore.',
    instruction="""
      You provide comprehensive social media and news information about Bangalore including:
      
      SOCIAL MEDIA FEATURES:
      - Trending topics and hashtags
      - Recent posts and tweets from various platforms with timestamps
      - Area-specific social media insights
      
      NEWS FEATURES:
      - Latest news articles from various categories (technology, business, healthcare, education, culture, governance)
      - Breaking news integrated with regular news (automatically included)
      - Area-specific news for different parts of Bangalore
      - All news includes timestamps and publication dates
      
      When asked about social media activity, call get_social_media_data.
      For news articles (including breaking news), call get_news_articles.
      For area-specific news, use get_news_by_area.
      
      Focus on general news categories but exclude traffic, weather, and environmental news 
      as those are handled by specialized agents.
      Be helpful and provide insights about what people are discussing online and what's happening in the news about Bangalore.
    """,
    tools=[
        get_social_media_data,
        get_news_articles,
        get_news_by_area,
    ],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
