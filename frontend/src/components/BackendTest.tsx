import React, { useState } from 'react';
import authService from '../services/authService';

const BackendTest: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<string>('');
  const [sendGridStatus, setSendGridStatus] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const testHealthEndpoint = async () => {
    setLoading(true);
    try {
      const result = await authService.testConnection();
      setHealthStatus(`Backend is healthy: ${JSON.stringify(result)}`);
    } catch (error: any) {
      setHealthStatus(`Backend connection failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testSendGrid = async () => {
    setLoading(true);
    try {
      const result = await authService.testSendGrid();
      setSendGridStatus(`SendGrid test successful: ${JSON.stringify(result)}`);
    } catch (error: any) {
      setSendGridStatus(`SendGrid test failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Backend Connection Test</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={testHealthEndpoint}
          disabled={loading}
          style={{ 
            padding: '10px 20px', 
            marginRight: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Testing...' : 'Test Health Endpoint'}
        </button>
        
        <button 
          onClick={testSendGrid}
          disabled={loading}
          style={{ 
            padding: '10px 20px',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Testing...' : 'Test SendGrid'}
        </button>
      </div>

      {healthStatus && (
        <div style={{ 
          padding: '10px', 
          marginBottom: '10px',
          backgroundColor: healthStatus.includes('healthy') ? '#d4edda' : '#f8d7da',
          border: `1px solid ${healthStatus.includes('healthy') ? '#c3e6cb' : '#f5c6cb'}`,
          borderRadius: '5px'
        }}>
          <strong>Health Status:</strong> {healthStatus}
        </div>
      )}

      {sendGridStatus && (
        <div style={{ 
          padding: '10px',
          backgroundColor: sendGridStatus.includes('successful') ? '#d4edda' : '#f8d7da',
          border: `1px solid ${sendGridStatus.includes('successful') ? '#c3e6cb' : '#f5c6cb'}`,
          borderRadius: '5px'
        }}>
          <strong>SendGrid Status:</strong> {sendGridStatus}
        </div>
      )}

      <div style={{ marginTop: '20px', fontSize: '14px', color: '#666' }}>
        <p><strong>Instructions:</strong></p>
        <ul>
          <li>Make sure your FastAPI backend is running on http://localhost:8000</li>
          <li>Click "Test Health Endpoint" to verify backend connection</li>
          <li>Click "Test SendGrid" to verify email functionality</li>
        </ul>
      </div>
    </div>
  );
};

export default BackendTest; 