import os
import tempfile
from typing import Optional
from PIL import Image
import pytesseract


class OCRService:
    """Service for OCR document processing."""

    async def process_document(self, file_path: str) -> dict:
        """
        Process document and extract text via OCR.

        Args:
            file_path: Path to the document file

        Returns:
            Dict with 'text' and 'extracted_data'
        """
        ext = os.path.splitext(file_path).lower()

        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
            return await self._process_image(file_path)
        elif ext == '.pdf':
            return await self._process_pdf(file_path)
        elif ext in ['.doc', '.docx']:
            return await self._process_doc(file_path)
        else:
            return await self._process_generic(file_path)

    async def _process_image(self, image_path: str) -> dict:
        """Process image file with OCR."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)

            # Try to extract structured data
            extracted_data = self._extract_receipt_data(text)

            return {
                "text": text,
                "extracted_data": extracted_data
            }
        except Exception as e:
            return {
                "text": "",
                "extracted_data": {"error": str(e)}
            }

    async def _process_pdf(self, pdf_path: str) -> dict:
        """Process PDF file."""
        # For MVP, convert first page to image and OCR it
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, first_page=1, last_page=1)
            if images:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
                    images[0].save(f.name, 'PNG')
                    result = await self._process_image(f.name)
                    os.unlink(f.name)
                    return result
        except ImportError:
            pass

        return {"text": "PDF processing not available", "extracted_data": {}}

    async def _process_doc(self, doc_path: str) -> dict:
        """Process Word document."""
        try:
            from docx import Document
            doc = Document(doc_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return {"text": text, "extracted_data": {}}
        except ImportError:
            return {"text": "DOC processing not available", "extracted_data": {}}

    async def _process_generic(self, file_path: str) -> dict:
        """Process generic file by reading as text if possible."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return {"text": text[:5000], "extracted_data": {}}
        except Exception:
            return {"text": "", "extracted_data": {}}

    def _extract_receipt_data(self, text: str) -> dict:
        """Extract structured data from receipt text."""
        import re

        data = {}

        # Extract total amount
        total_patterns = [
            r'total[:\s]*\$?(\d+\.?\d*)',
            r'grand total[:\s]*\$?(\d+\.?\d*)',
            r'amount[:\s]*\$?(\d+\.?\d*)',
        ]
        for pattern in total_patterns:
            match = re.search(pattern, text.lower())
            if match:
                data['total'] = float(match.group(1))
                break

        # Extract date
        date_patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{2,4})',
            r'(\d{1,2})-(\d{1,2})-(\d{2,4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                data['date'] = match.group(0)
                break

        # Extract merchant name (first line usually)
        lines = text.strip().split('\n')
        if lines:
            data['merchant'] = lines[0].strip()

        # Extract items (lines with prices)
        item_pattern = r'(.+?)[\s]+(\d+\.?\d*)'
        items = []
        for line in lines[1:]:
            match = re.search(item_pattern, line)
            if match:
                items.append({"item": match.group(1).strip(), "price": float(match.group(2))})
        if items:
            data['items'] = items

        return data


ocr_service = OCRService()
