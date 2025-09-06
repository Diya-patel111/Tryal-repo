"""
Certificate management routes module for AcademiaVeritas project.

This module provides secure certificate management endpoints for educational institutions
and public certificate verification functionality with file upload support.
"""

import os
import jwt
import functools
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.database import get_db_connection
from utils.hashing import generate_certificate_hash

# Load SECRET_KEY from environment variables for JWT signing
SECRET_KEY = os.getenv('SECRET_KEY')

# Define allowed file extensions for certificate uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Initialize the certificate management blueprint
cert_bp = Blueprint('certificate', __name__)


def token_required(f):
    """
    Custom JWT decorator for route protection.
    
    This decorator validates JWT tokens from the Authorization header and extracts
    the institution_id for use in protected routes. It ensures that only authenticated
    institutions can access secure endpoints.
    
    Args:
        f: The route function to be decorated
        
    Returns:
        Decorated function that validates JWT tokens before execution
        
    Raises:
        401 Unauthorized: If token is missing, invalid, or expired
    """
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check for Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "error": "Authorization header is missing"
            }), 401
        
        # Validate Bearer token format
        try:
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                return jsonify({
                    "error": "Invalid authorization type. Use 'Bearer <token>'"
                }), 401
        except ValueError:
            return jsonify({
                "error": "Invalid authorization header format. Use 'Bearer <token>'"
            }), 401
        
        # Validate SECRET_KEY availability
        if not SECRET_KEY:
            print("Error: SECRET_KEY environment variable is not set")
            return jsonify({
                "error": "Server configuration error"
            }), 500
        
        try:
            # Decode and validate the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_institution_id = payload.get('institution_id')
            
            if not current_institution_id:
                return jsonify({
                    "error": "Invalid token payload"
                }), 401
            
            # Pass the institution_id to the decorated function
            return f(current_institution_id, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                "error": "Token has expired"
            }), 401
            
        except jwt.InvalidTokenError:
            return jsonify({
                "error": "Invalid token"
            }), 401
            
        except Exception as e:
            print(f"Unexpected error during token validation: {e}")
            return jsonify({
                "error": "Token validation failed"
            }), 401
    
    return decorated


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): The name of the uploaded file
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@cert_bp.route('/api/certificate/add', methods=['POST'])
@token_required
def add_certificate(current_institution_id):
    """
    Add a new certificate record to the database.
    
    This endpoint allows authenticated institutions to add new certificate records
    to the system. It validates input data, generates integrity hashes, and stores
    the certificate information in the database.
    
    Expected JSON Input:
        {
            "student_name": "Jane Doe",
            "roll_number": "R-98765",
            "course_name": "Bachelor of Information Technology",
            "grade": "First Class",
            "issue_date": "2025-10-15"
        }
    
    Returns:
        JSON response with success message and 201 status code on success,
        or error message with appropriate status code on failure.
    """
    try:
        # Extract and validate input data from JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        student_name = data.get('student_name')
        roll_number = data.get('roll_number')
        course_name = data.get('course_name')
        grade = data.get('grade')
        issue_date = data.get('issue_date')
        
        # Validate that all required fields are present
        if not all([student_name, roll_number, course_name, grade, issue_date]):
            return jsonify({
                "error": "Missing required fields. Please provide student_name, roll_number, course_name, grade, and issue_date."
            }), 400
        
        # Validate date format (basic validation)
        try:
            # Convert string date to date object for validation
            from datetime import datetime
            datetime.strptime(issue_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "error": "Invalid date format. Please use YYYY-MM-DD format."
            }), 400
        
        # Generate certificate hash for data integrity
        certificate_hash = generate_certificate_hash(
            student_name, roll_number, course_name, issue_date
        )
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Check if certificate with this hash already exists
            cursor.execute(
                "SELECT id FROM certificates WHERE certificate_hash = %s",
                (certificate_hash,)
            )
            
            if cursor.fetchone():
                return jsonify({
                    "error": "Certificate with these details already exists"
                }), 409
            
            # Store certificate hash on blockchain
            from services.blockchain_service import store_certificate_on_blockchain
            
            blockchain_result = store_certificate_on_blockchain(certificate_hash, current_institution_id)
            blockchain_tx_hash = blockchain_result.get('tx_hash') if blockchain_result.get('success') else None
            
            # Insert new certificate into database
            cursor.execute(
                """INSERT INTO certificates 
                   (institution_id, student_name, roll_number, course_name, grade, issue_date, certificate_hash, blockchain_tx_hash) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (current_institution_id, student_name, roll_number, course_name, grade, issue_date, certificate_hash, blockchain_tx_hash)
            )
            
            # Commit the transaction
            connection.commit()
            
            response_data = {
                "message": "Certificate added successfully",
                "certificate_hash": certificate_hash,
                "blockchain_tx_hash": blockchain_tx_hash
            }
            
            if not blockchain_result.get('success'):
                response_data["blockchain_warning"] = "Certificate stored in database but blockchain storage failed"
            
            return jsonify(response_data), 201
            
        except Exception as e:
            # Rollback transaction on error
            connection.rollback()
            print(f"Database error during certificate addition: {e}")
            return jsonify({
                "error": "Database error occurred during certificate addition"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except Exception as e:
        print(f"Unexpected error during certificate addition: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


@cert_bp.route('/api/verify', methods=['POST'])
def verify_certificate():
    """
    Verify a certificate by uploading an image file.
    
    This public endpoint allows anyone to upload a certificate image for verification.
    It validates the file type, saves it temporarily, and processes it for verification.
    
    Expected Input:
        Multipart form data with a file field containing the certificate image
        
    Returns:
        JSON response with verification status and file information.
    """
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided. Please upload a certificate image."
            }), 400
        
        file = request.files['file']
        
        # Check if file is actually selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected. Please choose a certificate image."
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Sanitize filename for security
        filename = secure_filename(file.filename)
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Generate unique filename to prevent conflicts
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        try:
            # Save the uploaded file temporarily
            file.save(file_path)
            
            # Import OCR service for certificate processing
            from services.ocr_service import parse_details_from_image, validate_extracted_data
            from services.blockchain_service import verify_certificate_on_blockchain
            from utils.hashing import generate_certificate_hash
            
            # Extract details from the uploaded certificate
            extracted_details = parse_details_from_image(file_path)
            
            # Validate extracted data
            validated_details = validate_extracted_data(extracted_details)
            
            # Check if extraction was successful
            if validated_details.get('error'):
                return jsonify({
                    "error": f"Certificate processing failed: {validated_details['error']}"
                }), 400
            
            # Check if we have the minimum required data
            required_fields = ['student_name', 'roll_number', 'course_name', 'issue_date']
            missing_fields = [field for field in required_fields if not validated_details.get(field)]
            
            if missing_fields:
                return jsonify({
                    "error": f"Could not extract required information: {', '.join(missing_fields)}. Please ensure the certificate is clear and readable."
                }), 400
            
            # Generate certificate hash for verification
            certificate_hash = generate_certificate_hash(
                validated_details['student_name'],
                validated_details['roll_number'],
                validated_details['course_name'],
                validated_details['issue_date']
            )
            
            # Query database for matching certificate
            connection = get_db_connection()
            if not connection:
                return jsonify({
                    "error": "Database connection failed"
                }), 500
            
            try:
                cursor = connection.cursor()
                
                # Search for certificate in database
                cursor.execute(
                    """SELECT c.*, i.name as institution_name 
                       FROM certificates c 
                       JOIN institutions i ON c.institution_id = i.id 
                       WHERE c.certificate_hash = %s""",
                    (certificate_hash,)
                )
                
                certificate_record = cursor.fetchone()
                
                if certificate_record:
                    # Certificate found in database
                    result_data = {
                        "student_name": certificate_record[2],
                        "roll_number": certificate_record[3],
                        "course_name": certificate_record[4],
                        "grade": certificate_record[5],
                        "issue_date": certificate_record[6].isoformat() if certificate_record[6] else None,
                        "institution_name": certificate_record[9],  # institution name
                        "certificate_hash": certificate_record[7],
                        "blockchain_tx_hash": certificate_record[8]
                    }
                    
                    # Verify on blockchain if transaction hash exists
                    if certificate_record[8]:
                        blockchain_result = verify_certificate_on_blockchain(certificate_record[8])
                        result_data["blockchain_verified"] = blockchain_result.get('verified', False)
                    else:
                        result_data["blockchain_verified"] = False
                    
                    return jsonify(result_data), 200
                else:
                    # Certificate not found in database
                    return jsonify({
                        "error": "Certificate not found in our database. This certificate may not be issued by a registered institution or may be fraudulent."
                    }), 404
                    
            except Exception as e:
                print(f"Database error during verification: {e}")
                return jsonify({
                    "error": "Database error occurred during verification"
                }), 500
            finally:
                if connection:
                    connection.close()
            
        except Exception as e:
            print(f"Error processing uploaded file: {e}")
            return jsonify({
                "error": "Error processing uploaded file"
            }), 500
            
        finally:
            # Clean up: delete the temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temporary file: {e}")
                
    except Exception as e:
        print(f"Unexpected error during certificate verification: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


@cert_bp.route('/api/certificate/list', methods=['GET'])
@token_required
def list_certificates(current_institution_id):
    """
    List all certificates issued by the authenticated institution.
    
    This endpoint allows authenticated institutions to retrieve a list of all
    certificates they have issued, with optional pagination support.
    
    Query Parameters:
        page (int): Page number for pagination (default: 1)
        limit (int): Number of certificates per page (default: 10)
        
    Returns:
        JSON response with list of certificates and pagination information.
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Validate pagination parameters
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({
                "error": "Invalid pagination parameters. Page must be >= 1, limit must be between 1 and 100."
            }), 400
        
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Get total count of certificates for this institution
            cursor.execute(
                "SELECT COUNT(*) FROM certificates WHERE institution_id = %s",
                (current_institution_id,)
            )
            total_count = cursor.fetchone()[0]
            
            # Get paginated certificates
            cursor.execute(
                """SELECT id, student_name, roll_number, course_name, grade, issue_date, 
                          certificate_hash, blockchain_tx_hash, created_at
                   FROM certificates 
                   WHERE institution_id = %s 
                   ORDER BY created_at DESC 
                   LIMIT %s OFFSET %s""",
                (current_institution_id, limit, offset)
            )
            
            certificates = cursor.fetchall()
            
            # Convert to list of dictionaries
            certificate_list = []
            for cert in certificates:
                certificate_list.append({
                    "id": cert[0],
                    "student_name": cert[1],
                    "roll_number": cert[2],
                    "course_name": cert[3],
                    "grade": cert[4],
                    "issue_date": cert[5].isoformat() if cert[5] else None,
                    "certificate_hash": cert[6],
                    "blockchain_tx_hash": cert[7],
                    "created_at": cert[8].isoformat() if cert[8] else None
                })
            
            # Calculate pagination info
            total_pages = (total_count + limit - 1) // limit
            has_next = page < total_pages
            has_prev = page > 1
            
            return jsonify({
                "certificates": certificate_list,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_count": total_count,
                    "limit": limit,
                    "has_next": has_next,
                    "has_prev": has_prev
                }
            }), 200
            
        except Exception as e:
            print(f"Database error during certificate listing: {e}")
            return jsonify({
                "error": "Database error occurred during certificate listing"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except Exception as e:
        print(f"Unexpected error during certificate listing: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500
