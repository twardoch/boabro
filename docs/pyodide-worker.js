// pyodide-worker.js
importScripts('https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js');

// Debug logging function
function log(message) {
  self.postMessage({ type: 'log', data: message });
}

async function initializePyodide() {
  try {
    log("Loading Pyodide...");
    self.pyodide = await loadPyodide();
    log("Pyodide loaded, loading fonttools package...");
    await self.pyodide.loadPackage(['fonttools']);
    log("Fonttools package loaded, setting up Python environment...");
    
    // Setup font analysis functions
    await self.pyodide.runPython(`
      from fontTools.ttLib import TTFont
      import io
      import sys
      import traceback
      from io import StringIO
      
      def analyze_font(font_data):
          # Redirect stdout to capture output
          sys.stdout = StringIO()
          
          try:
              # Load the font from bytes
              font_io = io.BytesIO(font_data)
              font = TTFont(font_io)
              
              # Get UPM value
              upm = font["head"].unitsPerEm
              
              # Get name table entries
              name_table = font["name"]
              
              # Helper to get name
              def get_name(nameID):
                  entry = name_table.getName(nameID, 3, 1, 0x409) or name_table.getName(nameID, 1, 0, 0)
                  return entry.toUnicode() if entry else "(N/A)"
              
              # Print font information
              print(f"Font Information:\\n")
              print(f"Family Name: {get_name(1)}")
              print(f"Subfamily: {get_name(2)}")
              print(f"Full Name: {get_name(4)}")
              print(f"Version: {get_name(5)}")
              print(f"Units Per Em (UPM): {upm}")
              print(f"Number of Glyphs: {len(font.getGlyphOrder())}")
              
              print(f"\\nAvailable Tables:")
              for table in sorted(font.keys()):
                  print(f"- {table}")
              
              print(f"\\nName Table Entries:")
              for record in name_table.names:
                  try:
                      name_id = record.nameID
                      platform_id = record.platformID
                      string = record.toUnicode()
                      print(f"ID: {name_id}, Platform: {platform_id}, String: {string}")
                  except Exception as e:
                      print(f"ID: {record.nameID}, Platform: {record.platformID}, String: (could not decode: {str(e)})")
          
          except Exception as e:
              print(f"Error analyzing font: {str(e)}")
              print(f"\\nTraceback:\\n{traceback.format_exc()}")
          
          # Return the captured output
          return sys.stdout.getvalue()
      
      # Function to be called from JavaScript via pyodide
      def process_font(font_data_bytes):
          try:
              print(f"Processing font data ({len(font_data_bytes)} bytes)")
              return analyze_font(font_data_bytes)
          except Exception as e:
              return f"Error analyzing font: {str(e)}\\n\\nTraceback:\\n{traceback.format_exc()}"
              
      # For URL fetching, we'll use fetch from Python's side
      async def fetch_and_process_font(url):
          import pyodide.http
          
          try:
              print(f"Fetching font from URL: {url}")
              
              # Use custom headers to avoid CORS issues
              headers = {
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                  "Accept": "*/*",
                  "Accept-Language": "en-US,en;q=0.9",
                  "Referer": "https://example.com/",
                  "Origin": "https://example.com"
              }
              
              # List of CORS proxies to try
              cors_proxies = [
                  "https://corsproxy.io/?url=",
                  "https://api.allorigins.win/raw?url=",
                  "https://cors.eu.org/",
                  "https://xofix.4kb.dev/?url="
              ]
              
              font_data = None
              
              # If it's a GitHub URL, try to use a more direct approach first
              if "github.com" in url:
                  # Try to convert to raw.githubusercontent.com if not already
                  if "raw.githubusercontent.com" not in url:
                      # Convert github.com URL to raw.githubusercontent.com
                      raw_url = url.replace("github.com", "raw.githubusercontent.com")
                      raw_url = raw_url.replace("/blob/", "/")
                      print(f"Converted to raw URL: {raw_url}")
                      try:
                          response = await pyodide.http.pyfetch(raw_url, headers=headers)
                          if response.status == 200:
                              font_data = await response.bytes()
                              print(f"Successfully fetched {len(font_data)} bytes from raw URL")
                      except Exception as raw_error:
                          print(f"Raw URL request failed: {str(raw_error)}")
              
              # If we don't have font data yet, try CORS proxies
              if not font_data:
                  # Try each CORS proxy in sequence
                  for proxy in cors_proxies:
                      proxy_url = f"{proxy}{url}"
                      print(f"Trying CORS proxy: {proxy}")
                      try:
                          response = await pyodide.http.pyfetch(proxy_url, headers=headers)
                          if response.status == 200:
                              font_data = await response.bytes()
                              print(f"Successfully fetched {len(font_data)} bytes via proxy: {proxy}")
                              break
                          else:
                              print(f"Proxy {proxy} request failed with status: {response.status}")
                      except Exception as proxy_error:
                          print(f"Proxy {proxy} request failed: {str(proxy_error)}")
              
              # If we still don't have font data, try direct URL as fallback
              if not font_data:
                  print("Trying direct URL request")
                  try:
                      response = await pyodide.http.pyfetch(url, headers=headers)
                      if response.status == 200:
                          font_data = await response.bytes()
                          print(f"Successfully fetched {len(font_data)} bytes from direct URL")
                      else:
                          print(f"Direct request failed with status: {response.status}")
                  except Exception as direct_error:
                      print(f"Direct request failed: {str(direct_error)}")
                  
                  # Try with no-cors mode as a last resort
                  if not font_data:
                      print("Attempting with no-cors mode")
                      try:
                          response = await pyodide.http.pyfetch(url, headers=headers, mode="no-cors")
                          font_data = await response.bytes()
                          print(f"Successfully fetched {len(font_data)} bytes with no-cors mode")
                      except Exception as no_cors_error:
                          print(f"No-cors request failed: {str(no_cors_error)}")
              
              # If we have font data, analyze it
              if font_data:
                  return analyze_font(font_data)
              else:
                  return "Failed to fetch font from URL. CORS policy may be blocking the request. Try downloading the font and uploading it directly."
          except Exception as e:
              error_details = traceback.format_exc()
              print(f"Error processing font URL: {str(e)}")
              print(f"Error details: {error_details}")
              return f"Error processing font URL: {str(e)}\n\nTraceback:\n{error_details}"
    `);
    
    log("Python environment setup complete");
    self.postMessage({ type: 'ready' });
  } catch (error) {
    log(`Error initializing Pyodide: ${error.message}`);
    self.postMessage({ type: 'error', data: `Failed to initialize Pyodide: ${error.message}` });
  }
}

self.onmessage = async (event) => {
  const { type, code, data, url } = event.data;
  
  try {
    if (type === 'run') {
      // Redirect stdout
      self.pyodide.runPython(`
        import sys
        from io import StringIO
        sys.stdout = StringIO()
      `);
      
      // Run the code
      self.pyodide.runPython(code);
      
      // Get the output
      const stdout = self.pyodide.runPython("sys.stdout.getvalue()");
      self.postMessage({ type: 'output', data: stdout });
    }
    else if (type === 'analyze_font_file') {
      log("Received font file data for analysis");
      // Process uploaded font file
      const fontBytes = new Uint8Array(data);
      log(`Processing ${fontBytes.length} bytes of font data`);
      const result = await self.pyodide.runPythonAsync(`process_font(${fontBytes})`);
      self.postMessage({ type: 'output', data: result });
    }
    else if (type === 'analyze_font_url') {
      log(`Received URL for analysis: ${url}`);
      // Process font from URL
      // Escape any quotes in the URL to prevent injection
      const safeUrl = url.replace(/"/g, '\\"');
      const result = await self.pyodide.runPythonAsync(`await fetch_and_process_font("${safeUrl}")`);
      self.postMessage({ type: 'output', data: result });
    }
  } catch (error) {
    log(`Error in worker: ${error.message}`);
    self.postMessage({ type: 'error', data: error.message });
  }
};

// Start initialization
log("Worker script loaded, initializing Pyodide...");
initializePyodide();
