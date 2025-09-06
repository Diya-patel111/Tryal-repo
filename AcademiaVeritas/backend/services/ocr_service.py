"""
OCR service module for AcademiaVeritas project.

This module provides intelligent optical character recognition (OCR) functionality
for extracting key information from academic certificate images and PDF files.
It uses Tesseract OCR engine with custom regex patterns for accurate data extraction.
"""

import re
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def parse_details_from_image(file_path: str) -> dict:
    """
    Extract key information from an academic certificate image or PDF file.
    
    This function serves as the main entry point for OCR processing. It handles
    both image files (PNG, JPG, JPEG) and PDF files, converting them to text
    using Tesseract OCR and then extracting structured data using intelligent
    regex patterns.
    
    Args:
        file_path (str): Path to the certificate file (image or PDF)
        
    Returns:
        dict: Dictionary containing extracted certificate details with keys:
            - student_name (str or None): Full name of the student
            - roll_number (str or None): Student's roll/enrollment number
            - course_name (str or None): Name of the course or degree
            - grade (str or None): Grade or classification achieved
            - issue_date (str or None): Date when certificate was issued
            - institution_name (str or None): Name of the issuing institution
            - error (str or None): Error message if extraction failed
            
    Example:
        >>> details = parse_details_from_image("/path/to/certificate.pdf")
        >>> print(details)
        {
            'student_name': 'Jane Doe',
            'roll_number': 'R-98765',
            'course_name': 'Bachelor of Information Technology',
            'grade': 'First Class',
            'issue_date': '2025-10-15',
            'institution_name': 'University of Technology',
            'error': None
        }
    """
    try:
        # Validate file path
        if not os.path.exists(file_path):
            return {
                "student_name": None,
                "roll_number": None,
                "course_name": None,
                "grade": None,
                "issue_date": None,
                "institution_name": None,
                "error": "File not found"
            }
        
        # Get file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Initialize image object
        image_object = None
        
        # Handle PDF files
        if file_extension == '.pdf':
            try:
                # Convert first page of PDF to image
                images = convert_from_path(file_path, first_page=1, last_page=1, dpi=300)
                if images:
                    image_object = images[0]
                else:
                    return {
                        "student_name": None,
                        "roll_number": None,
                        "course_name": None,
                        "grade": None,
                        "issue_date": None,
                        "institution_name": None,
                        "error": "Failed to convert PDF to image"
                    }
            except Exception as e:
                return {
                    "student_name": None,
                    "roll_number": None,
                    "course_name": None,
                    "grade": None,
                    "issue_date": None,
                    "institution_name": None,
                    "error": f"PDF conversion error: {str(e)}"
                }
        
        # Handle image files
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            try:
                image_object = Image.open(file_path)
            except Exception as e:
                return {
                    "student_name": None,
                    "roll_number": None,
                    "course_name": None,
                    "grade": None,
                    "issue_date": None,
                    "institution_name": None,
                    "error": f"Image loading error: {str(e)}"
                }
        
        # Handle unsupported file types
        else:
            return {
                "student_name": None,
                "roll_number": None,
                "course_name": None,
                "grade": None,
                "issue_date": None,
                "institution_name": None,
                "error": f"Unsupported file type: {file_extension}"
            }
        
        # Perform OCR on the image
        try:
            # Configure Tesseract for better accuracy
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,-/:() '
            raw_text = pytesseract.image_to_string(image_object, config=custom_config)
        except Exception as e:
            return {
                "student_name": None,
                "roll_number": None,
                "course_name": None,
                "grade": None,
                "issue_date": None,
                "institution_name": None,
                "error": f"OCR processing error: {str(e)}"
            }
        
        # Extract structured data using regex patterns
        extracted_details = _extract_details_with_regex(raw_text)
        
        # Add raw text for debugging (remove in production)
        extracted_details["raw_text"] = raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
        
        return extracted_details
        
    except Exception as e:
        return {
            "student_name": None,
            "roll_number": None,
            "course_name": None,
            "grade": None,
            "issue_date": None,
            "institution_name": None,
            "error": f"Unexpected error: {str(e)}"
        }


def _extract_details_with_regex(text: str) -> dict:
    """
    Extract structured data from raw OCR text using intelligent regex patterns.
    
    This helper function uses a comprehensive set of regular expressions to identify
    and extract key information from academic certificates. The patterns are designed
    to handle various certificate formats and layouts commonly used by educational
    institutions.
    
    Args:
        text (str): Raw text extracted from OCR processing
        
    Returns:
        dict: Dictionary containing extracted certificate details
    """
    # Initialize result dictionary
    details = {
        "student_name": None,
        "roll_number": None,
        "course_name": None,
        "grade": None,
        "issue_date": None,
        "institution_name": None,
        "error": None
    }
    
    # Comprehensive regex patterns for data extraction
    patterns = {
        'student_name': [
            # Pattern 1: Look for names after common certificate phrases
            r"(?i)(?:This is to certify that|is hereby awarded to|of)\s+([A-Z][a-z]+(?:\s[A-Z][a-z'\.]+)+)",
            # Pattern 2: Look for names after "Name:" or similar labels
            r"(?i)(?:Name|Student Name|Candidate Name)\s*[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z'\.]+)+)",
            # Pattern 3: Generic three-part name pattern (First Middle Last)
            r"([A-Z][a-z]+\s[A-Z][a-z\.]+\s[A-Z][a-z]+)",
            # Pattern 4: Two-part name pattern (First Last)
            r"([A-Z][a-z]+\s[A-Z][a-z]+)",
            # Pattern 5: Look for names in quotes
            r'"([A-Z][a-z]+(?:\s[A-Z][a-z'\.]+)+)"'
        ],
        
        'roll_number': [
            # Pattern 1: Look for roll number with common keywords
            r"(?i)(?:Roll No|Enrollment No\.?|ID|Serial No|Student ID|Reg\.? No)\s*[:\-]?\s*([A-Z0-9\-]+)",
            # Pattern 2: Look for roll number with "Number" keyword
            r"(?i)(?:Roll Number|Enrollment Number|Registration Number)\s*[:\-]?\s*([A-Z0-9\-]+)",
            # Pattern 3: Generic long number pattern (5-12 digits)
            r"\b(\d{5,12})\b",
            # Pattern 4: Alphanumeric code pattern
            r"\b([A-Z]{2,4}\d{4,8})\b",
            # Pattern 5: Look for numbers with dashes or slashes
            r"\b(\d{2,4}[-/]\d{2,4}[-/]\d{2,4})\b"
        ],
        
        'course_name': [
            # Pattern 1: Look for degree/course names after common phrases
            r"(?i)(?:in|for|of)\s+([A-Z][A-Za-z\s]+(?:Bachelor|Master|Diploma|Certificate|Degree|Program|Course))",
            # Pattern 2: Look for course names with "in" keyword
            r"(?i)(?:Bachelor|Master|Diploma|Certificate|Degree)\s+of\s+([A-Z][A-Za-z\s]+)",
            # Pattern 3: Look for course names in quotes
            r'"([A-Z][A-Za-z\s]+(?:Bachelor|Master|Diploma|Certificate|Degree|Program|Course))"',
            # Pattern 4: Generic course name pattern
            r"([A-Z][A-Za-z\s]{10,50}(?:Bachelor|Master|Diploma|Certificate|Degree|Program|Course))",
            # Pattern 5: Look for course names with "in" at the beginning
            r"(?i)in\s+([A-Z][A-Za-z\s]+(?:Engineering|Technology|Science|Arts|Commerce|Management))"
        ],
        
        'grade': [
            # Pattern 1: Look for grades after common phrases
            r"(?i)(?:with|obtaining|securing)\s+([A-Z][a-z\s]+(?:Class|Grade|Division|Honors|Distinction))",
            # Pattern 2: Look for percentage grades
            r"(?i)(?:with|obtaining|securing)\s+(\d{1,3}\.?\d*%)",
            # Pattern 3: Look for letter grades
            r"(?i)(?:Grade|GPA)\s*[:\-]?\s*([A-F][+-]?)",
            # Pattern 4: Look for CGPA
            r"(?i)(?:CGPA|GPA)\s*[:\-]?\s*(\d\.\d{1,2})",
            # Pattern 5: Generic grade pattern
            r"([A-Z][a-z\s]+(?:First|Second|Third|Distinction|Merit|Pass))"
        ],
        
        'issue_date': [
            # Pattern 1: Look for dates in DD/MM/YYYY format
            r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b",
            # Pattern 2: Look for dates in YYYY-MM-DD format
            r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
            # Pattern 3: Look for dates with month names
            r"\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b",
            # Pattern 4: Look for dates after common phrases
            r"(?i)(?:dated|on|issued on)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            # Pattern 5: Look for dates in Month DD, YYYY format
            r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b"
        ],
        
        'institution_name': [
            # Pattern 1: Look for institution names after common phrases
            r"(?i)(?:from|by|at)\s+([A-Z][A-Za-z\s]+(?:University|College|Institute|School|Academy))",
            # Pattern 2: Look for institution names in quotes
            r'"([A-Z][A-Za-z\s]+(?:University|College|Institute|School|Academy))"',
            # Pattern 3: Look for institution names with "of" keyword
            r"([A-Z][A-Za-z\s]+(?:University|College|Institute|School|Academy)\s+of\s+[A-Z][A-Za-z\s]+)",
            # Pattern 4: Generic institution name pattern
            r"([A-Z][A-Za-z\s]{5,50}(?:University|College|Institute|School|Academy))",
            # Pattern 5: Look for institution names at the beginning of lines
            r"^([A-Z][A-Za-z\s]+(?:University|College|Institute|School|Academy))"
        ]
    }
    
    # Extract data using regex patterns
    for detail_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    extracted_value = match.group(1).strip()
                    # Clean up the extracted value
                    extracted_value = re.sub(r'\s+', ' ', extracted_value)  # Normalize whitespace
                    extracted_value = extracted_value.strip('.,:;')  # Remove trailing punctuation
                    details[detail_type] = extracted_value
                    break  # Use the first successful pattern
            except Exception as e:
                # Continue with next pattern if current one fails
                continue
    
    return details


def validate_extracted_data(details: dict) -> dict:
    """
    Validate and clean the extracted certificate data.
    
    This function performs additional validation and cleaning on the extracted
    data to ensure accuracy and consistency.
    
    Args:
        details (dict): Dictionary containing extracted certificate details
        
    Returns:
        dict: Validated and cleaned certificate details
    """
    validated_details = details.copy()
    
    # Validate student name
    if validated_details.get('student_name'):
        name = validated_details['student_name']
        # Remove common OCR artifacts
        name = re.sub(r'[^\w\s\.\']', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        if len(name) < 3 or len(name) > 100:
            validated_details['student_name'] = None
    
    # Validate roll number
    if validated_details.get('roll_number'):
        roll = validated_details['roll_number']
        # Clean roll number
        roll = re.sub(r'[^\w\-/]', '', roll)
        if len(roll) < 3 or len(roll) > 20:
            validated_details['roll_number'] = None
    
    # Validate course name
    if validated_details.get('course_name'):
        course = validated_details['course_name']
        # Clean course name
        course = re.sub(r'[^\w\s]', '', course)
        course = re.sub(r'\s+', ' ', course).strip()
        if len(course) < 5 or len(course) > 200:
            validated_details['course_name'] = None
    
    # Validate grade
    if validated_details.get('grade'):
        grade = validated_details['grade']
        # Clean grade
        grade = re.sub(r'[^\w\s\.%+-]', '', grade)
        grade = re.sub(r'\s+', ' ', grade).strip()
        if len(grade) < 1 or len(grade) > 50:
            validated_details['grade'] = None
    
    # Validate issue date
    if validated_details.get('issue_date'):
        date_str = validated_details['issue_date']
        # Basic date validation
        if not re.match(r'\d{1,4}[/-]\d{1,2}[/-]\d{1,4}', date_str):
            validated_details['issue_date'] = None
    
    # Validate institution name
    if validated_details.get('institution_name'):
        institution = validated_details['institution_name']
        # Clean institution name
        institution = re.sub(r'[^\w\s]', '', institution)
        institution = re.sub(r'\s+', ' ', institution).strip()
        if len(institution) < 5 or len(institution) > 200:
            validated_details['institution_name'] = None
    
    return validated_details
