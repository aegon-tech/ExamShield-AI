"""
pdf_engine.py - Core Engine for PDF Watermarking, Batching, and Forensics.
Operates strictly in-memory using io.BytesIO with DoS protection.
"""

import io
import csv
import zipfile
import re
import os
import textwrap
import logging
from typing import Tuple, Dict, Any, List
import fitz  # PyMuPDF

logger = logging.getLogger("ExamShield.Engine")

# Cryptographic Forensic Envelope Pattern
FORENSIC_PATTERN = re.compile(r"\[\[SHIELD_TX:(.*?)\]\]")
MAX_BATCH_ROWS = 250  # Memory safety threshold


class PDFEngineError(Exception):
    """Custom exception class for PDF processing and forensic errors."""
    pass


def embed_watermark_stream(pdf_bytes: bytes, secret_code: str) -> bytes:
    """Embeds an invisible forensic watermark wrapped in a secure envelope."""
    if not pdf_bytes:
        raise PDFEngineError("Input PDF byte stream is empty.")
    
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        payload = f"[[SHIELD_TX:{secret_code.strip()}]]"
        
        # 1. Embed in PDF metadata
        meta = doc.metadata or {}
        existing_keywords = meta.get("keywords", "") or ""
        meta["keywords"] = f"{existing_keywords} {payload}".strip()
        doc.set_metadata(meta)
        
        # 2. Embed as invisible steganographic text on page 1
        if len(doc) > 0:
            page = doc[0]
            page.insert_text(
    fitz.Point(-1000, -1000),  # Page canvas ke bahar (Ctrl+A copy protection)
    payload,
    fontsize=0.1,
    render_mode=3
)
            
        output = io.BytesIO()
        doc.save(output, garbage=3, deflate=True)
        doc.close()
        return output.getvalue()
    except Exception as err:
        logger.error(f"Watermarking error: {str(err)}")
        raise PDFEngineError(f"Watermark embedding failed: {str(err)}") from err


def extract_watermark_stream(pdf_bytes: bytes) -> Dict[str, Any]:
    """Detects and recovers forensic watermarks from metadata and page streams."""
    if not pdf_bytes:
        raise PDFEngineError("Input PDF byte stream is empty.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        found_codes = set()
        
        # 1. Scan Metadata
        meta = doc.metadata or {}
        for value in meta.values():
            if value and isinstance(value, str):
                matches = FORENSIC_PATTERN.findall(value)
                for m in matches:
                    found_codes.add(m.strip())
                    
        # 2. Scan Text/Steganographic Stream
        for page in doc:
            text = page.get_text("text")
            matches = FORENSIC_PATTERN.findall(text)
            for m in matches:
                found_codes.add(m.strip())
                
        doc.close()
        
        if found_codes:
            codes_list = sorted(list(found_codes))
            return {
                "detected": True,
                "code": codes_list[0],
                "all_codes": codes_list,
                "confidence": "100% (Envelope Match)"
            }
        return {
            "detected": False,
            "code": None,
            "confidence": "0%"
        }
    except Exception as err:
        logger.error(f"Extraction error: {str(err)}")
        raise PDFEngineError(f"Forensic extraction failed: {str(err)}") from err


def batch_watermark_memory(pdf_bytes: bytes, csv_bytes: bytes) -> Tuple[bytes, Dict[str, Any]]:
    """Generates watermarked PDFs in memory with path traversal and DoS protection."""
    try:
        csv_text = csv_bytes.decode("utf-8-sig", errors="ignore")
        csv_reader = list(csv.DictReader(io.StringIO(csv_text)))
    except Exception as err:
        raise PDFEngineError(f"Invalid CSV structure: {str(err)}")

    if len(csv_reader) > MAX_BATCH_ROWS:
        raise PDFEngineError(f"Batch size exceeds maximum limit of {MAX_BATCH_ROWS} rows.")

    zip_buffer = io.BytesIO()
    summary = {"total": len(csv_reader), "success": 0, "failed": 0, "files": []}
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for row in csv_reader:
            code = row.get("code") or row.get("center_code") or row.get("Code")
            raw_filename = row.get("filename") or row.get("file_name") or row.get("Filename")
            
            if not code or not raw_filename:
                summary["failed"] += 1
                continue
            
            # Sanitize filename against path traversal
            filename = os.path.basename(raw_filename.strip())
            if not filename.endswith(".pdf"):
                filename += ".pdf"
                
            try:
                watermarked_pdf = embed_watermark_stream(pdf_bytes, code)
                zip_file.writestr(filename, watermarked_pdf)
                summary["success"] += 1
                summary["files"].append(filename)
            except Exception:
                summary["failed"] += 1
                
    zip_buffer.seek(0)
    return zip_buffer.getvalue(), summary


def text_to_pdf_stream(text: str) -> bytes:
    """Converts plain text to PDF without string truncation or loss."""
    try:
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # Standard A4
        margin = 50
        current_y = margin
        line_height = 14
        
        for raw_line in text.splitlines():
            wrapped_lines = textwrap.wrap(raw_line, width=80)
            
            if not wrapped_lines:
                current_y += 10
                if current_y > 780:
                    page = doc.new_page(width=595, height=842)
                    current_y = margin
                continue
                
            for line in wrapped_lines:
                if current_y > 780:
                    page = doc.new_page(width=595, height=842)
                    current_y = margin
                page.insert_text(fitz.Point(margin, current_y), line, fontsize=10)
                current_y += line_height
                
        output = io.BytesIO()
        doc.save(output)
        doc.close()
        return output.getvalue()
    except Exception as err:
        raise PDFEngineError(f"PDF generation from text failed: {str(err)}") from err