import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import api from '../apiService'; // Import our new API service

// --- Sub-components for displaying results ---
const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-8">
    <svg className="animate-spin h-10 w-10 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  </div>
);

const SuccessResult = ({ data }) => (
  <div className="text-center p-6 bg-green-50 border-2 border-green-200 rounded-lg">
    <svg className="w-16 h-16 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <h2 className="mt-4 text-2xl font-bold text-green-800">Certificate Verified Successfully!</h2>
    <div className="mt-4 text-left bg-white p-4 rounded-md shadow-sm">
      <p><strong>Student:</strong> {data.student_name || 'N/A'}</p>
      <p><strong>Roll Number:</strong> {data.roll_number || 'N/A'}</p>
      <p><strong>Course:</strong> {data.course_name || 'N/A'}</p>
      <p><strong>Grade:</strong> {data.grade || 'N/A'}</p>
      <p><strong>Issue Date:</strong> {data.issue_date || 'N/A'}</p>
      <p><strong>Institution:</strong> {data.institution_name || 'N/A'}</p>
      <div className="mt-3 flex items-center gap-2">
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          data.blockchain_verified 
            ? 'bg-green-100 text-green-800' 
            : 'bg-yellow-100 text-yellow-800'
        }`}>
          {data.blockchain_verified ? '✓ Blockchain Verified' : '⚠ Blockchain Pending'}
        </span>
      </div>
      {data.blockchain_tx_hash && (
        <a href={`https://sepolia.etherscan.io/tx/${data.blockchain_tx_hash}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline mt-2 inline-block">View on Blockchain</a>
      )}
    </div>
  </div>
);

const ErrorResult = ({ message }) => (
   <div className="text-center p-6 bg-red-50 border-2 border-red-200 rounded-lg">
    <svg className="w-16 h-16 mx-auto text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <h2 className="mt-4 text-2xl font-bold text-red-800">Verification Failed</h2>
    <p className="mt-2 text-red-600">{message}</p>
  </div>
);


// --- Main Component ---
const VerificationDemo = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleVerify = async (acceptedFile) => {
    setFile(acceptedFile);
    setIsLoading(true);
    setResult(null);
    setError('');
    try {
      const response = await api.verifyCertificate(acceptedFile);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      handleVerify(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop, 
    multiple: false,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf']
    }
  });

  return (
    <div className="bg-white p-4 sm:p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
      <div className="text-center mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Certificate Authenticity Validator</h1>
        <p className="mt-2 text-sm sm:text-base text-gray-600">Upload a certificate file (PNG, JPG, PDF) to instantly verify its authenticity.</p>
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : result ? (
         <SuccessResult data={result} />
      ) : error ? (
        <ErrorResult message={error} />
      ) : (
        <div {...getRootProps()} className={`p-8 sm:p-12 border-2 border-dashed rounded-lg cursor-pointer text-center transition-colors ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}>
          <input {...getInputProps()} />
          <svg className="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-4-4V6a4 4 0 014-4h10a4 4 0 014 4v6a4 4 0 01-4 4H7z" /></svg>
          {isDragActive ?
            <p className="mt-4 text-blue-600 font-semibold">Drop the file here...</p> :
            <p className="mt-4 text-gray-500">Drag & drop your file here, or click to select a file</p>
          }
          <p className="mt-2 text-sm text-gray-400">Supports: PNG, JPG, JPEG, PDF</p>
        </div>
      )}
      {(result || error) && (
         <button onClick={() => { setFile(null); setResult(null); setError(''); }} className="mt-6 w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
           Verify Another Document
         </button>
      )}
    </div>
  );
};

export default VerificationDemo;
