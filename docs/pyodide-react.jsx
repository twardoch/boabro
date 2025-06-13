// App.jsx
import React, { useState, useEffect } from 'react';
import { loadPyodide } from 'pyodide';

function App() {
  const [pyodide, setPyodide] = useState(null);
  const [output, setOutput] = useState('Loading Python...');
  const [code, setCode] = useState('print("Hello from Python!")');

  useEffect(() => {
    async function initPyodide() {
      try {
        const pyodideInstance = await loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/'
        });
        setPyodide(pyodideInstance);
        setOutput('Python loaded successfully!');
      } catch (error) {
        setOutput(`Failed to load Python: ${error.message}`);
      }
    }
    initPyodide();
  }, []);

  const runCode = async () => {
    if (!pyodide) return;
    
    try {
      // Redirect stdout to capture print statements
      pyodide.runPython(`
        import sys
        from io import StringIO
        sys.stdout = StringIO()
      `);
      
      // Run the user code
      pyodide.runPython(code);
      
      // Get the captured output
      const stdout = pyodide.runPython("sys.stdout.getvalue()");
      setOutput(stdout || 'Code executed successfully (no output)');
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <h1>Python in React</h1>
      <textarea
        rows="10"
        cols="50"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <div>
        <button onClick={runCode} disabled={!pyodide}>
          Run Python
        </button>
      </div>
      <pre>{output}</pre>
    </div>
  );
}

export default App;
