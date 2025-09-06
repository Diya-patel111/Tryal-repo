import React, { useState } from 'react';
import Navbar from './components/Navbar';
import VerificationDemo from './components/VerificationDemo';
import InstitutionPortal from './components/InstitutionPortal';

function App() {
  const [activeView, setActiveView] = useState('verifier'); // 'verifier' or 'portal'

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar activeView={activeView} setActiveView={setActiveView} />
      <main className="pt-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {activeView === 'verifier' ? <VerificationDemo /> : <InstitutionPortal />}
      </main>
    </div>
  );
}

export default App;
