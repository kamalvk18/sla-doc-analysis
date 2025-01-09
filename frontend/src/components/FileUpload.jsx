import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const FileUpload = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      await handleUpload(selectedFile);
    }
  };

  const handleUpload = async (selectedFile) => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/v1/get_sla_insights_json/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        navigate('/result', {
          state: { responseData: response.data },
        });
      } else {
        alert("Error uploading file");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">Extract SLA from Document</h1>

        <p className="text-lg mb-6">Extract Service Level Agreements from documents with incredible accuracy</p>

        <input
          type="file"
          className="hidden"
          onChange={handleFileChange}
          ref={fileInputRef}
        />

        <button
          className="bg-red-500 text-white py-3 px-6 text-lg rounded-lg hover:bg-red-700 transform transition duration-200 hover:scale-105"
          onClick={() => fileInputRef.current.click()}
        >
          {loading ? "Uploading..." : "Upload Document File"}
        </button>
      </div>
    </div>
  );
};

export default FileUpload;
