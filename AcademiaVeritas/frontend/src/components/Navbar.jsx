import React from 'react';

const Navbar = ({ activeView, setActiveView }) => {
  const navButtonStyles = "px-4 py-2 rounded-md text-sm font-medium transition-colors";
  const activeStyles = "bg-blue-600 text-white";
  const inactiveStyles = "text-gray-600 hover:bg-gray-200";

  return (
    <nav className="bg-white shadow-md w-full fixed top-0 left-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section */}
          <div className="flex-shrink-0 flex items-center">
            {/* SVG for a simple shield icon */}
            <svg className="h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 20.944a12.02 12.02 0 0018 0 12.02 12.02 0 00-3.382-9.984z" />
            </svg>
            <span className="ml-3 text-xl font-bold text-gray-800">AcademiaVeritas</span>
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setActiveView('verifier')}
              className={`${navButtonStyles} ${activeView === 'verifier' ? activeStyles : inactiveStyles}`}
            >
              Verify Certificate
            </button>
            <button
              onClick={() => setActiveView('portal')}
              className={`${navButtonStyles} ${activeView === 'portal' ? activeStyles : inactiveStyles}`}
            >
              Institution Portal
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
