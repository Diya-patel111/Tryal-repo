# 🚀 How to Run AcademiaVeritas Project

This guide will show you how to run your complete AcademiaVeritas project and see the output.

## 📋 Prerequisites Check

✅ **Python 3.13.7** - Installed  
✅ **Node.js v22.19.0** - Installed  
❌ **Docker** - Not installed (optional)

## 🎯 Quick Start Guide

### **Method 1: Manual Setup (Recommended for now)**

Since Docker is not installed, we'll run the project manually. Here's the step-by-step process:

#### Step 1: Set up the Backend

1. **Navigate to backend directory:**
   ```bash
   cd Tryal-repo/AcademiaVeritas/backend
   ```

2. **Create environment file:**
   Create a file named `.env` in the backend directory with this content:
   ```env
   DATABASE_URL=postgresql://admin:admin@localhost:5432/academia_veritas
   SECRET_KEY=academia-veritas-secret-key-2024
   INFURA_API_KEY=demo-key
   CONTRACT_ADDRESS=demo-address
   WALLET_PRIVATE_KEY=demo-key
   WALLET_ADDRESS=demo-address
   MAX_CONTENT_LENGTH=16777216
   UPLOAD_FOLDER=uploads
   ALLOWED_EXTENSIONS=png,jpg,jpeg,pdf
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   - Install PostgreSQL if not already installed
   - Create database: `academia_veritas`
   - Create user: `admin` with password: `admin`

5. **Run the backend:**
   ```bash
   python app.py
   ```

#### Step 2: Set up the Frontend

1. **Navigate to frontend directory:**
   ```bash
   cd Tryal-repo/AcademiaVeritas/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Run the frontend:**
   ```bash
   npm run dev
   ```

#### Step 3: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

---

## 🐳 Method 2: Docker Setup (If you install Docker)

If you want to install Docker later, here's how to use it:

### Install Docker Desktop

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Install and restart your computer
3. Open Docker Desktop

### Run with Docker

1. **Create the .env file** (same as above)
2. **Run the project:**
   ```bash
   cd Tryal-repo/AcademiaVeritas
   docker-compose up --build
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:8080
   - **Backend API**: http://localhost:5001

---

## 🎮 What You'll See

### Frontend Interface
- **Home Page**: Welcome to AcademiaVeritas
- **Institution Portal**: Login/Register for institutions
- **Verification Demo**: Upload certificate images for verification
- **Modern UI**: Built with React and Tailwind CSS

### Backend API Endpoints
- **POST /api/auth/register**: Institution registration
- **POST /api/auth/login**: Institution login
- **POST /api/certificate/add**: Add new certificate
- **POST /api/verify**: Verify certificate
- **GET /api/certificate/list**: List certificates

### Key Features You Can Test

1. **Institution Registration**
   - Register a new educational institution
   - Get JWT token for authentication

2. **Certificate Management**
   - Add new certificates with student details
   - Generate SHA-256 hashes for verification
   - Store certificates in database

3. **Certificate Verification**
   - Upload certificate images
   - OCR extraction of certificate details
   - Two-factor verification (Database + Blockchain)
   - Real-time verification results

4. **Blockchain Integration**
   - Certificate hashes stored on Ethereum
   - Immutable verification records
   - Tamper-proof certificate validation

---

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in .env
   - Verify database exists

2. **Port Already in Use**
   - Change ports in configuration
   - Kill processes using the ports

3. **Module Import Errors**
   - Install missing dependencies
   - Check Python/Node.js versions

4. **Frontend Not Loading**
   - Check if backend is running
   - Verify API endpoints
   - Check browser console for errors

### Debug Commands

```bash
# Check if ports are in use
netstat -an | findstr :5000
netstat -an | findstr :5173

# Check Python packages
pip list

# Check Node.js packages
npm list

# Check database connection
psql -U admin -d academia_veritas -h localhost
```

---

## 📱 Demo Scenarios

### Scenario 1: Institution Registration
1. Open http://localhost:5173
2. Click "Institution Portal"
3. Register with institution details
4. Login with credentials
5. Access institution dashboard

### Scenario 2: Certificate Verification
1. Go to "Verification Demo"
2. Upload a certificate image
3. Watch OCR extraction process
4. See verification results
5. Check blockchain verification status

### Scenario 3: Full Workflow
1. Register as institution
2. Add multiple certificates
3. Test verification with different certificates
4. View certificate list
5. Test blockchain integration

---

## 🎉 Success Indicators

You'll know the project is working when you see:

✅ **Backend**: "Running on http://localhost:5000"  
✅ **Frontend**: "Local: http://localhost:5173"  
✅ **Database**: Connection successful  
✅ **API**: Endpoints responding  
✅ **UI**: Modern interface loading  
✅ **OCR**: Image processing working  
✅ **Blockchain**: Hash verification working  

---

## 🚀 Next Steps

Once everything is running:

1. **Test all features** thoroughly
2. **Customize the UI** for your presentation
3. **Add sample data** for demonstration
4. **Prepare your pitch** highlighting the blockchain integration
5. **Document any issues** you encounter

Your AcademiaVeritas project is now ready to showcase the power of blockchain-verified academic certificates! 🎓✨
