import React from 'react';
import './App.css';
import BackendTest from './components/BackendTest';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Macro Tracking App - Frontend</h1>
        <p>Testing Backend Connection</p>
      </header>
      <main>
        <BackendTest />
      </main>
    </div>
  );
}

export default App;
