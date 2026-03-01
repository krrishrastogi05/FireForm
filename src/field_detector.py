"""
PDF Field Detection Engine

Extracts form field information and coordinates from PDF templates.
This module provides the foundation for the Field Mapping Wizard by detecting
and analyzing all interactive form fields within PDF documents.
"""

import pypdf
import os
from typing import List, Dict, Optional


class PDFFieldDetector:
    """Extracts form field information and coordinates from PDF templates."""
    
    def detect_fields(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract all form fields from PDF with position and type information.
        
        Args:
            pdf_path: Path to the PDF template file
            
        Returns:
            Dictionary containing field information and metadata
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            RuntimeError: If PDF processing fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        fields = []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages):
                    if not page.get('/Annots'):
                        continue
                        
                    for annotation in page['/Annots']:
                        try:
                            annot_obj = annotation.get_object()
                            if annot_obj.get('/Subtype') == '/Widget':
                                field_info = self._extract_field(annot_obj, page_num)
                                if field_info:
                                    fields.append(field_info)
                        except Exception as e:
                            # Skip problematic annotations but continue processing
                            print(f"Warning: Could not process annotation on page {page_num}: {e}")
                            continue
                            
        except Exception as e:
            raise RuntimeError(f"Error processing PDF: {str(e)}")
        
        return {
            "success": True,
            "field_count": len(fields),
            "fields": fields,
            "pages_processed": len(reader.pages) if 'reader' in locals() else 0
        }

    def _extract_field(self, annotation, page_num: int) -> Optional[Dict]:
        """
        Extract field information from a single PDF annotation.
        
        Args:
            annotation: PDF annotation object
            page_num: Page number (0-based)
            
        Returns:
            Dictionary with field information or None if extraction fails
        """
        try:
            # Extract field name
            name = str(annotation.get('/T', f'unknown_page_{page_num}')).strip()
            
            # Extract position coordinates
            rect = annotation.get('/Rect', [0, 0, 0, 0])
            position = {
                "x": float(rect[0]), 
                "y": float(rect[1]), 
                "w": float(rect[2]), 
                "h": float(rect[3])
            }
            
            # Determine field type from PDF field type annotation
            ft = annotation.get('/FT')
            field_type = 'unknown'
            if ft == '/Tx':
                field_type = 'text'
            elif ft == '/Btn':
                field_type = 'checkbox_or_radio'
            elif ft == '/Ch':
                field_type = 'dropdown'
            elif ft == '/Sig':
                field_type = 'signature'

            # Check if field is required
            required = bool(annotation.get('/Ff', 0) & 2)  # PDF Required flag

            return {
                "name": name,
                "type": field_type,
                "page": page_num,
                "position": position,
                "required": required
            }
            
        except Exception as e:
            print(f"Warning: Could not extract field info: {e}")
            return None