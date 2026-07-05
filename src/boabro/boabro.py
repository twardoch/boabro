#!/usr/bin/env python3
# this_file: src/boabro/boabro.py
"""boabro: In-browser font analysis tools.

Fetch a font. Crack it open. Look inside.
All running locally in the browser via PyScript. No server required.

Created by Adam Twardoch.
"""

import io
import logging
import traceback
from typing import Any

from fontTools.ttLib import TTFont

# `js`, `pyodide`, and `to_js` only exist inside the PyScript/Pyodide runtime.
# Locally (tests, the CLI) they are absent, so we fall back to plain-Python stand-ins.
# `document` and `pyodide` stay `None` off-browser; the fetch code guards on that.
try:
    from js import Object, console as js_console, document
    from pyodide.ffi import to_js
    import pyodide.http
except ImportError:
    js_console = print  # browser console.log -> local print

    class DummyObject:
        """Minimal stand-in for the JS `Object` used only for `Object.fromEntries`."""

        @staticmethod
        def fromEntries(entries: Any) -> dict[str, Any]:  # noqa: N802
            return dict(entries)

    Object = DummyObject
    document = None
    pyodide = None
    to_js = None  # sentinel: header conversion is skipped when running locally

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Centralized logging for the font utilities.
util_logger = logging.getLogger("boabro.font_utils")
util_logger.setLevel(logging.INFO)  # Default; the host app may raise it.


def _log_util_debug(message: str) -> None:
    """Emit a debug line to the Python logger and, in PyScript, the browser console.

    Locally the message only surfaces when the logger is at DEBUG, so the CLI
    stays quiet. In PyScript the real `console.log` mirrors it to the devtools
    console, which is where the HTML examples want it.
    """
    util_logger.debug(message)
    if hasattr(
        js_console, "log"
    ):  # real browser console, not the local `print` stand-in
        js_console.log(f"[BoabroUtilDebug] {message}")


def _to_js_headers(headers_dict: dict[str, str]) -> Any:
    """Convert a header dict to the JS object `pyodide.http.pyfetch` expects.

    Inside PyScript `pyfetch` needs a real JS object, so we round-trip through
    `to_js` + `Object.fromEntries`. Locally `to_js` is `None`, so we hand back
    the plain dict untouched.
    """
    if to_js is None:
        return headers_dict
    return Object.fromEntries(to_js(headers_dict).entries())


async def fetch_font_bytes_from_url(url_str: str) -> bytes | None:  # noqa: C901, PLR0912, PLR0915
    """Fetches font data from a given URL.

    This function attempts to retrieve font file bytes using several strategies:
    1. If it's a GitHub URL, it tries to convert it to a raw content URL.
    2. It then iterates through a list of common CORS proxies.
    3. A direct fetch is attempted.
    4. Finally, a direct fetch with `mode="no-cors"` is tried as a last resort.

    Standard HTTP headers (User-Agent, Accept, Referer, Origin) are included in
    the requests to improve success rates. Relies on `pyodide.http.pyfetch`
    when running in a PyScript environment.

    Args:
        url_str: The URL string from which to fetch the font data.

    Returns:
        Optional[bytes]: The font data as bytes if successfully fetched,
                         otherwise None.
    """
    _log_util_debug(f"Fetching font from URL: {url_str}")
    if not url_str or not url_str.startswith(("http://", "https://")):
        util_logger.error(f"Invalid URL provided: {url_str}")
        return None

    try:
        # Determine headers. In PyScript, document.location might be available.
        # Default to generic referer/origin if not in a browser context with 'document'.
        referer = (
            document.location.href
            if document and hasattr(document, "location")
            else "https://example.com/"
        )
        origin = (
            document.location.origin
            if document and hasattr(document, "location")
            else "https://example.com/"
        )

        headers_dict = {
            "User-Agent": "Mozilla/5.0 (BoabroFontInspector/1.0)",
            "Accept": "*/*",
            "Referer": referer,
            "Origin": origin,
        }
        # In PyScript, headers must be a JS Object.
        headers_js = _to_js_headers(headers_dict)

        cors_proxies = [
            "https://corsproxy.io/?url=",
            "https://api.allorigins.win/raw?url=",
            "https://cors.eu.org/",
            "https://xofix.4kb.dev/?url=",
        ]

        font_data_bytes: bytes | None = None

        # Try GitHub raw URL conversion first
        if "github.com" in url_str and "raw.githubusercontent.com" not in url_str:
            raw_url = url_str.replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob/", "/")
            _log_util_debug(f"Attempting GitHub raw URL: {raw_url}")
            try:
                response = await pyodide.http.pyfetch(raw_url, headers=headers_js)
                if response.status == 200:
                    font_data_bytes = await response.bytes()
                    _log_util_debug(
                        f"Successfully fetched {len(font_data_bytes)} bytes from raw GitHub URL."
                    )
            except Exception as e:
                _log_util_debug(f"Raw GitHub URL request failed: {e!s}")

        # Try CORS proxies if raw GitHub failed or not a GitHub URL
        if not font_data_bytes:
            for proxy_base in cors_proxies:
                proxy_url = f"{proxy_base}{url_str}"
                _log_util_debug(f"Trying CORS proxy: {proxy_url}")
                try:
                    response = await pyodide.http.pyfetch(proxy_url, headers=headers_js)
                    if response.status == 200:
                        font_data_bytes = await response.bytes()
                        _log_util_debug(
                            f"Successfully fetched {len(font_data_bytes)} bytes via proxy: {proxy_base}"
                        )
                        break
                except Exception as e:
                    _log_util_debug(f"Proxy {proxy_base} request failed: {e!s}")

        # Try direct URL if proxies failed
        if not font_data_bytes:
            _log_util_debug(f"Trying direct URL request: {url_str}")
            try:
                response = await pyodide.http.pyfetch(url_str, headers=headers_js)
                if response.status == 200:
                    font_data_bytes = await response.bytes()
                    _log_util_debug(
                        f"Successfully fetched {len(font_data_bytes)} bytes from direct URL."
                    )
            except Exception as e:
                _log_util_debug(f"Direct URL request failed: {e!s}")

        # Try no-cors as a last resort
        if not font_data_bytes:
            _log_util_debug(f"Attempting with no-cors mode for: {url_str}")
            try:
                # For no-cors, headers might be restricted. Sending minimal.
                no_cors_headers_js = _to_js_headers({"Accept": "*/*"})
                response = await pyodide.http.pyfetch(
                    url_str, headers=no_cors_headers_js, mode="no-cors"
                )
                font_data_bytes = await response.bytes()
                if font_data_bytes and len(font_data_bytes) > 0:
                    _log_util_debug(
                        f"Fetched {len(font_data_bytes)} bytes with no-cors mode (quality unknown)."
                    )
                else:
                    _log_util_debug(f"No-cors mode did not yield data for {url_str}.")
                    font_data_bytes = None
            except Exception as e:
                _log_util_debug(f"No-cors request failed for {url_str}: {e!s}")
                font_data_bytes = None

        if not font_data_bytes:
            util_logger.warning(f"All fetch attempts failed for URL: {url_str}")
            return None

        return font_data_bytes

    except Exception as e:
        util_logger.error(
            f"Generic error in fetch_font_bytes_from_url for {url_str}: {e!s}\n{traceback.format_exc()}"
        )
        return None


def analyze_font_data(
    font_bytes: bytes, filename: str | None = "font"
) -> dict[str, Any]:
    """Analyzes font data using fontTools and returns a structured dictionary.

    Args:
        font_bytes: The raw byte content of the font file.
        filename: Optional name of the font file, used for context and in the
                  output dictionary. Defaults to "font".

    Returns:
        A dictionary containing various pieces of font information.
        Key structure includes:
        - `fileName` (str): The provided or default filename.
        - `familyName` (str): Font family name (NameID 1).
        - `subfamily` (str): Font subfamily (NameID 2).
        - `uniqueID` (str): Unique font identifier (NameID 3).
        - `fullName` (str): Full font name (NameID 4).
        - `version` (str): Version string (NameID 5).
        - `psName` (str): PostScript name (NameID 6).
        - `trademark` (str): Trademark (NameID 7).
        - `manufacturer` (str): Manufacturer (NameID 8).
        - `designer` (str): Designer (NameID 9).
        - `description` (str): Description (NameID 10).
        - `vendorURL` (str): Vendor URL (NameID 11).
        - `designerURL` (str): Designer URL (NameID 12).
        - `license` (str): License description (NameID 13).
        - `licenseURL` (str): License URL (NameID 14).
        - `typographicFamily` (str): Typographic Family name (NameID 16).
        - `typographicSubfamily` (str): Typographic Subfamily name (NameID 17).
        - `compatibleFullName` (str): Compatible Full Name (NameID 18).
        - `sampleText` (str): Sample text (NameID 19).
        - `postScriptCIDFindfontName` (str): PostScript CID findfont name (NameID 20).
        - `wwsFamilyName` (str): WWS Family Name (NameID 21).
        - `wwsSubfamilyName` (str): WWS Subfamily Name (NameID 22).
        - `lightBackgroundPalette` (str): Light Background Palette (NameID 23).
        - `darkBackgroundPalette` (str): Dark Background Palette (NameID 24).
        - `variationsPostScriptNamePrefix` (str): Variations PostScript Name Prefix (NameID 25).
        - `upm` (int): Units Per Em, from the 'head' table.
        - `numGlyphs` (int): Total number of glyphs in the font.
        - `tables` (List[str]): A sorted list of table tags present in the font.
        - `nameTableRecords` (List[Dict[str, Any]]): A list of all name records,
          where each record is a dictionary with keys: `nameID` (int),
          `platformID` (int), `platEncID` (int), `langID` (int), `string` (str).

        The dictionary might also contain detailed dumps of other tables like
        'head', 'hhea', 'OS/2', 'glyf', 'CFF ' if `fontTools` provides them,
        though these are not explicitly enumerated in this docstring for brevity.
        Consult `fontTools` documentation for details on those table structures.

    Raises:
        Exception: Any exception raised by `fontTools.ttLib.TTFont` during parsing
                   or if other unexpected errors occur during analysis.
                   The caller is responsible for handling these.
    """
    _log_util_debug(f"Analyzing font data for: {filename} ({len(font_bytes)} bytes)")
    try:
        font_io = io.BytesIO(font_bytes)
        font = TTFont(font_io)

        name_table = font["name"]

        def get_name(name_id: int) -> str:
            # Prefer the Windows/Unicode/English record (3,1,0x409); fall back to
            # the Macintosh/Roman record (1,0,0) that older fonts still carry.
            entry = name_table.getName(name_id, 3, 1, 0x409) or name_table.getName(
                name_id, 1, 0, 0
            )
            return entry.toUnicode() if entry else "(N/A)"

        name_records: list[dict[str, Any]] = []
        for record in name_table.names:
            try:
                name_records.append(
                    {
                        "nameID": record.nameID,
                        "platformID": record.platformID,
                        "platEncID": record.platEncID,
                        "langID": record.langID,
                        "string": record.toUnicode(),
                    }
                )
            except Exception:
                name_records.append(
                    {
                        "nameID": record.nameID,
                        "platformID": record.platformID,
                        "platEncID": record.platEncID,
                        "langID": record.langID,
                        "string": "(could not decode)",
                    }
                )

        result = {
            "fileName": filename,
            "familyName": get_name(1),
            "subfamily": get_name(2),
            "uniqueID": get_name(3),
            "fullName": get_name(4),
            "version": get_name(5),
            "psName": get_name(6),
            "trademark": get_name(7),
            "manufacturer": get_name(8),
            "designer": get_name(9),
            "description": get_name(10),
            "vendorURL": get_name(11),
            "designerURL": get_name(12),
            "license": get_name(13),
            "licenseURL": get_name(14),
            "typographicFamily": get_name(16),
            "typographicSubfamily": get_name(17),
            "compatibleFullName": get_name(18),
            "sampleText": get_name(19),
            "postScriptCIDFindfontName": get_name(20),
            "wwsFamilyName": get_name(21),
            "wwsSubfamilyName": get_name(22),
            "lightBackgroundPalette": get_name(23),
            "darkBackgroundPalette": get_name(24),
            "variationsPostScriptNamePrefix": get_name(25),
            "upm": font["head"].unitsPerEm,
            "numGlyphs": len(font.getGlyphOrder()),
            "tables": sorted(font.keys()),
            "nameTableRecords": name_records,
        }
        _log_util_debug(f"Analysis successful for {filename}.")
        return result
    except Exception as e:
        util_logger.error(
            f"Error analyzing font {filename}: {e!s}\n{traceback.format_exc()}"
        )
        raise  # Let the caller decide how to surface the failure.
