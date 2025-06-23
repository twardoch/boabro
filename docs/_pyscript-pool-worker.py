# Python code for the Web Worker Pool (adapted from embedded script in pyodide-workerspool.html)
import sys
import io
import traceback
# from fontTools.ttLib import TTFont # No longer used directly
# import pyodide.http # No longer used directly
from js import self as js_self, postMessage, Object, URL # Need URL for filename extraction
from pyodide.ffi import to_js, create_proxy

# Import shared utilities from boabro.boabro
# This assumes that the main HTML page's <py-config> has set up paths correctly
# (e.g., paths = ["../../src"]) so that `import boabro.boabro` works.
from boabro.boabro import fetch_font_bytes_from_url, analyze_font_data

def log_debug_to_main(message):
    """Sends a log message to the main thread."""
    print(f"[PoolWorkerPy] {message}") # Worker's own console
    try:
        # Use a consistent 'log' type if the main thread is set up to handle it for debugging
        postMessage(to_js({"type": "log", "data": f"[PoolWorkerPy] {message}"}))
    except Exception as e:
        print(f"[PoolWorkerPy] Error sending log to main: {e}")


log_debug_to_main("Python pool worker script started and shared utilities imported.")

# The local analyze_font_for_pool can now directly use the shared analyze_font_data
# as the shared utility already returns a comprehensive dictionary.
# No significant adaptation of the dictionary structure is needed for this worker,
# as the main thread's PyodideWorkersPool class seems to handle the dictionary as is.

async def on_message_handler(event):
    message_data = event.data.to_py()

    task_id = message_data.get("id")
    task_type = message_data.get("type")

    log_debug_to_main(f"Worker received task ID {task_id}, type: {task_type}")

    if task_type == 'analyze':
        file_name_str = message_data.get("fileName", "uploaded_file")
        try:
            font_data_js_array = message_data.get("fontData") # JS ArrayBuffer/TypedArray
            font_bytes = bytes(font_data_js_array)

            log_debug_to_main(f"Task {task_id}: Analyzing file '{file_name_str}' ({len(font_bytes)} bytes)")
            analysis_result_dict = analyze_font_data(font_bytes, filename=file_name_str)

            postMessage(to_js({
                "type": "result",
                "id": task_id,
                "success": True,
                "data": result_data # Python dict, to_js will handle it
            }))
        except Exception as e:
            log_debug_to_main(f"Error processing file task {task_id} ({file_name}): {str(e)}")
            postMessage(to_js({
                "type": "result",
                "id": task_id,
                "success": False,
                "error": str(e),
                "fileName": file_name
            }))

    elif task_type == 'analyze_url':
        url = message.get("url")
        file_name_for_error = url # Use URL as filename in case of error
        try:
            font_data_bytes = await fetch_font_from_url_internal(url)

            # Extract filename from URL for successful fetch
            # This is a bit simplistic, real URLs can be complex.
            try {
                url_obj = URL.new(url)
                file_name = url_obj.pathname.split('/')[-1] or f"font-from-{url_obj.hostname}.ttf"
            } except Exception { // In case URL parsing fails (e.g. not a valid URL string for JS URL constructor)
                file_name = "font-from-url.ttf"
            }

            result_data = analyze_font_for_pool(font_data_bytes, file_name)
            postMessage(to_js({
                "type": "result",
                "id": task_id,
                "success": True,
                "data": result_data
            }))
        except Exception as e:
            log_debug_to_main(f"Error processing URL task {task_id} ({url}): {str(e)}")
            postMessage(to_js({
                "type": "result",
                "id": task_id,
                "success": False,
                "error": str(e),
                "fileName": file_name_for_error
            }))
    else:
        log_debug_to_main(f"Unknown message type received: {task_type}")

# Setup message listener for the worker
js_self.addEventListener('message', create_proxy(on_message_handler))

# Signal that the worker's Python environment is ready
log_debug_to_main("Python pool worker initialized and listener attached.")
postMessage(to_js({"type": "ready"}))
