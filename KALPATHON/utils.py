"""
Utility Module
Helper functions for text processing, validation, and formatting.
"""

import re
from typing import Optional, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_clause(clause: str, min_length: int = 10, max_length: int = 5000) -> tuple[bool, Optional[str]]:
    """
    Validate input clause text.
    
    Args:
        clause: Input clause text
        min_length: Minimum character length
        max_length: Maximum character length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not clause or not clause.strip():
        return False, "Please enter a legal clause to analyze."
    
    clause = clause.strip()
    
    if len(clause) < min_length:
        return False, f"Clause is too short. Please enter at least {min_length} characters."
    
    if len(clause) > max_length:
        return False, f"Clause is too long. Please limit to {max_length} characters."
    
    # Check if it's mostly gibberish
    word_count = len(clause.split())
    if word_count < 3:
        return False, "Please enter a complete legal clause with multiple words."
    
    return True, None


def format_risk_level(risk: str) -> str:
    """
    Format and validate risk level.
    
    Args:
        risk: Risk level string
        
    Returns:
        Standardized risk level (Low, Medium, or High)
    """
    risk = risk.strip().capitalize()
    
    if risk not in ["Low", "Medium", "High"]:
        logger.warning(f"Invalid risk level '{risk}', defaulting to Medium")
        return "Medium"
    
    return risk


def get_risk_color(risk: str) -> str:
    """
    Get the color code for a risk level.
    
    Args:
        risk: Risk level (Low, Medium, High)
        
    Returns:
        Color code string
    """
    colors = {
        "Low": "#10b981",      # Green
        "Medium": "#f59e0b",   # Amber
        "High": "#ef4444"      # Red
    }
    return colors.get(risk, "#6b7280")  # Default gray


def get_risk_emoji(risk: str) -> str:
    """
    Get an emoji for a risk level.
    
    Args:
        risk: Risk level
        
    Returns:
        Emoji string
    """
    emojis = {
        "Low": "✅",
        "Medium": "⚠️",
        "High": "🚨"
    }
    return emojis.get(risk, "ℹ️")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].strip() + suffix


def clean_whitespace(text: str) -> str:
    """
    Clean excessive whitespace from text.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def format_explanation(explanation: str, max_sentences: Optional[int] = None) -> str:
    """
    Format explanation text for display.
    
    Args:
        explanation: Raw explanation text
        max_sentences: Optional limit on number of sentences
        
    Returns:
        Formatted explanation
    """
    explanation = clean_whitespace(explanation)
    
    if max_sentences:
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', explanation)
        if len(sentences) > max_sentences:
            explanation = ' '.join(sentences[:max_sentences])
    
    return explanation


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time for text.
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in minutes
    """
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes


def create_session_id() -> str:
    """
    Create a unique session identifier.
    
    Returns:
        Session ID string
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe file operations.
    
    Args:
        filename: Input filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def log_analysis(clause: str, risk: str, explanation: str) -> None:
    """
    Log an analysis for debugging/monitoring.
    
    Args:
        clause: Input clause
        risk: Detected risk level
        explanation: Generated explanation
    """
    logger.info(
        f"Analysis completed - Risk: {risk}, "
        f"Clause length: {len(clause)}, "
        f"Explanation length: {len(explanation)}"
    )


def get_example_clauses() -> list[Dict[str, str]]:
    """
    Get example clauses for users to try.
    
    Returns:
        List of example clause dictionaries
    """
    return [
        {
            "title": "Notice Period",
            "clause": "The tenant must provide written notice of at least 30 days prior to vacating the premises. Notice must be delivered in writing to the landlord's registered address."
        },
        {
            "title": "Rent Increase",
            "clause": "The landlord reserves the right to increase the monthly rent with 30 days written notice to the tenant. Rent increases shall not exceed the maximum allowed by local rent control ordinances."
        },
        {
            "title": "Maintenance Responsibility",
            "clause": "The tenant shall be responsible for all repairs and maintenance to the premises, including but not limited to plumbing, electrical, structural, and cosmetic repairs, regardless of the cause of damage."
        },
        {
            "title": "Security Deposit",
            "clause": "A security deposit equal to one month's rent is required. The deposit will be held in an interest-bearing account and returned within 30 days of lease termination, minus any deductions for damages beyond normal wear and tear."
        }
    ]


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def get_system_info() -> Dict[str, Any]:
    """
    Get system information for debugging.
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
    }
