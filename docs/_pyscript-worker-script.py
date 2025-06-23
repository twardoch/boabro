# Python code for the Web Worker (originally in pyodide-worker.js)
import sys
import io
import traceback
# from fontTools.ttLib import TTFont # No longer directly used here
# import pyodide.http # No longer directly used here
from js import self as js_self, postMessage, Uint8Array, Object # Added Object for headers
from pyodide.ffi import to_js, create_proxy

# Import shared utilities
from boabro.boabro import fetch_font_bytes_from_url, analyze_font_data


# Debug logging function for the worker
def log_to_main(message_type, data):
    postMessage(to_js({"type": message_type, "data": data}))

def log_debug(message):
    log_to_main('log', f"[PyWorker] {message}")

log_debug("Python worker script started.")

def _format_analysis_to_text_for_worker(analysis_data: dict) -> str:
    """
    Helper to format the structured analysis data from analyze_font_data
    into the text string format this worker posts to the main thread.
    """
    if not analysis_data:
        return "No analysis data to format."

    output_parts = [
        f"Font Information for: {analysis_data.get('fileName', 'N/A')}",
        f"Family Name: {analysis_data.get('familyName', 'N/A')}",
        f"Subfamily: {analysis_data.get('subfamily', 'N/A')}",
        f"Full Name: {analysis_data.get('fullName', 'N/A')}",
        f"Version: {analysis_data.get('version', 'N/A')}",
        f"Units Per Em (UPM): {analysis_data.get('upm', 'N/A')}",
        f"Number of Glyphs: {analysis_data.get('numGlyphs', 'N/A')}",
        f"\nAvailable Tables:"
    ]
    output_parts.extend(f"- {table}" for table in analysis_data.get('tables', []))

    output_parts.append(f"\nName Table Entries:")
    for record in analysis_data.get('nameTableRecords', []):
        output_parts.append(f"ID: {record.get('nameID', 'N/A')}, Platform: {record.get('platformID', 'N/A')}, String: {record.get('string', 'N/A')}")

    return "\n".join(output_parts)

def analyze_font_from_bytes_for_worker(font_data_bytes, filename="font_from_bytes"):
    """Analyzes font data (bytes) and returns a formatted text string."""
    log_debug(f"Analyzing font data for '{filename}' ({len(font_data_bytes)} bytes) using shared utility.")
    try:
        analysis_data = analyze_font_data(font_data_bytes, filename=filename)
        return _format_analysis_to_text_for_worker(analysis_data)
    except Exception as e:
        log_debug(f"Error in analyze_font_from_bytes_for_worker for '{filename}': {str(e)}\n{traceback.format_exc()}")
        return f"Error analyzing font '{filename}': {str(e)}\n\nTraceback:\n{traceback.format_exc()}"

async def fetch_and_analyze_font_url(url_str: str):
    """Fetches a font from URL, analyzes it, and returns a formatted text string."""
    log_debug(f"Fetching and analyzing URL: {url_str}")
    try:
        font_bytes = await fetch_font_bytes_from_url(url_str) # from boabro.boabro
        if font_bytes:
            filename = url_str.split('/')[-1] if url_str else "font_from_url"
            return analyze_font_from_bytes_for_worker(font_bytes, filename=filename)
        else:
            err_msg = f"Failed to fetch font from URL: {url_str} (shared utility returned None)"
            log_debug(err_msg)
            return err_msg
    except Exception as e:
        log_debug(f"Error in fetch_and_analyze_font_url for {url_str}: {str(e)}\n{traceback.format_exc()}")
        return f"Error processing font URL '{url_str}': {str(e)}\n\nTraceback:\n{traceback.format_exc()}"

async def on_message_handler(event):
    message = event.data.to_py() # Convert JS object to Python dict if not already
    type = message.get("type")

    log_debug(f"Received message of type: {type}")

    if type == 'analyze_font_file':
        try:
            # Data from main thread is ArrayBuffer, convert to bytes
            font_data_js_array = message.get("data") # This is an ArrayBuffer
            font_data_bytes = bytes(font_data_js_array) # Convert ArrayBuffer to Python bytes

            # Extract filename if sent, otherwise use a default.
            # The main thread (JS) currently doesn't send filename for file uploads with arrayBuffer.
            filename = message.get("filename", "uploaded_file_from_worker.dat")

            result = analyze_font_from_bytes_for_worker(font_data_bytes, filename=filename)
            log_to_main('output', result)
        except Exception as e:
            log_debug(f"Error processing file: {str(e)}\n{traceback.format_exc()}")
            log_to_main('error', f"Error processing font file: {str(e)}")

    elif type == 'analyze_font_url':
        try:
            url = message.get("url")
            result = await fetch_and_analyze_font_url(url)
            log_to_main('output', result)
        except Exception as e:
            log_debug(f"Error processing URL: {str(e)}\n{traceback.format_exc()}")
            log_to_main('error', f"Error processing font URL: {str(e)}")
    else:
        log_debug(f"Unknown message type: {type}")

# PyScript specific: Set up the message listener for the worker
from pyodide.ffi import create_proxy, to_js
js_self.addEventListener('message', create_proxy(on_message_handler))

# Signal that the worker is ready with its Python environment
log_to_main('ready', 'PyScript worker is initialized and ready.')
log_debug("Python worker initialization complete. Listener attached.")

# Keep the worker alive (PyScript might terminate it if the main script ends)
# This is usually not needed if there's an active event listener.
# import time
# while True:
# time.sleep(1)
# log_debug("Worker still alive...")
# This loop is problematic as it blocks. Event listener should be enough.
