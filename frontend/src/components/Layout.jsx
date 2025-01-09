import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ChatBot from './ChatBot';

const Layout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { responseData } = location.state || {};
  const renderValue = (value) => {
    if (Array.isArray(value)) {
      return value.join(', ');
    }
    return value;
  };

  const handleDownloadJson = () => {
    const json = JSON.stringify(responseData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'responseData.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-3/4 p-6">
        <h1 className="text-4xl font-bold text-gray-800">Extracted SLA from Document</h1>

        {responseData ? (
          <div className="mt-6 p-4 border border-gray-300 rounded-md bg-white shadow-md">
            <div className="mt-2 text-lg text-gray-600">
              {Object.keys(responseData).map((key) => (
                <div key={key} className="mb-2">
                  <strong>{key}:</strong> {renderValue(responseData[key])}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="mt-6 text-lg">No SLA data found in the uploaded document.</p>
        )}
        <button
        className="mt-2 bg-orange-400 text-white py-2 px-4 rounded-lg shadow-md hover:bg-blue-600"
        onClick={() => navigate('/')}
        >Home
        </button>
        {responseData && (
            <button
            onClick={handleDownloadJson}
            className="mt-2 float-right bg-blue-500 text-white py-2 px-4 rounded-lg shadow-md hover:bg-blue-600"
            >
            Download as JSON
            </button>
        )}
      </div>

      <div className="w-1/4">
        <ChatBot />
      </div>
    </div>
  );
};

export default Layout;
