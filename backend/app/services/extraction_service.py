import re
from typing import Optional
from decimal import Decimal


class ExtractionService:
    """Service for extracting structured data from text."""

    async def extract_transaction(self, text: str) -> dict:
        """
        Extract financial transaction data from text.

        Args:
            text: Input text (from voice or OCR)

        Returns:
            Dict with amount, category, description, date
        """
        data = {
            "amount": None,
            "category": "general",
            "description": text[:200],
            "date": None
        }

        # Extract dollar amounts
        amount_patterns = [
            r'\$(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:dollars?|bucks)',
            r'(?:spent|paid|used)\s*(\d+\.?\d*)',
        ]

        for pattern in amount_patterns:
            match = re.search(pattern, text.lower())
            if match:
                data["amount"] = Decimal(match.group(1))
                break

        # Extract category keywords
        category_keywords = {
            "food": ["restaurant", "food", "lunch", "dinner", "breakfast", "coffee", "cafe", "eat"],
            "transport": ["uber", "lyft", "taxi", "bus", "train", "flight", "gas", "parking"],
            "office": ["office", "supplies", "staples", "amazon", "business"],
            "utilities": ["electric", "water", "internet", "phone", "utility"],
            "entertainment": ["netflix", "spotify", "movie", "game", "entertainment"],
            "shopping": ["walmart", "target", "costco", "shop", "store", "buy"],
        }

        text_lower = text.lower()
        for category, keywords in category_keywords.items():
            if any(kw in text_lower for kw in keywords):
                data["category"] = category
                break

        # Extract date patterns
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{1,2}-\d{1,2}-\d{2,4})',
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["date"] = match.group(1)
                break

        return data

    async def extract_structured_data(self, text: str, doc_type: str = "general") -> dict:
        """
        Extract structured data based on document type.

        Args:
            text: Input text
            doc_type: Type of document (receipt, invoice, note, etc.)

        Returns:
            Structured dict with extracted data
        """
        if doc_type == "receipt":
            return await self.extract_transaction(text)
        elif doc_type == "note":
            return {"content": text, "type": "note"}
        else:
            return await self.extract_transaction(text)


extraction_service = ExtractionService()
