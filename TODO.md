# TODO

### [x] http://127.0.0.1:8080/gradio.html

Works fully correctly!

### [x] http://127.0.0.1:8080/stlite.html

Works!

### [x] http://127.0.0.1:8080/_pyscript-fs.html

Ported to PyScript from `pyodide-fs.html`. Functionality includes file upload, URL processing, and saving/loading fonts from PyScript's virtual filesystem. File renamed to `_pyscript-fs.html`.
 

### [x] http://127.0.0.1:8080/_pyscript-tailwindcss.html

Ported to PyScript from `pyodide-tailwindcss.html`. Uses Tailwind CSS for styling. Python code for fetching and analysis is now in `<script type="py">`. File renamed to `_pyscript-tailwindcss.html`.

 

### [x] http://127.0.0.1:8080/_pyscript-worker.html

Ported to PyScript from `pyodide-worker.html` and `pyodide-worker.js`. The main page `_pyscript-worker.html` now uses a PyScript worker defined in `_pyscript-worker-script.py`. Communication uses standard Web Worker APIs, bridged by PyScript. Old `pyodide-worker.js` deleted.


### [x] http://127.0.0.1:8080/_pyscript-workerspool.html

Ported to PyScript from `pyodide-workerspool.html`. The main page `_pyscript-workerspool.html` now uses a pool of PyScript workers, defined in `<py-config>` and using `_pyscript-pool-worker.py`. The JavaScript `PyodideWorkersPool` class was adapted to manage these PyScript worker proxies, with a main-thread PyScript block to facilitate initialization.


### [x] http://127.0.0.1:8080/_pyscript-alpinejs.html

Refactored Alpine.js initialization to use `alpine:init` and correctly interact with PyScript functions after `py:ready`. Addressed console errors related to undefined properties. File renamed to `_pyscript-alpinejs.html`.

On load, console: 

```
cdn.min.js:1 Alpine Expression Error: fontAnalyzer is not defined

Expression: "fontAnalyzer"

 div.container.py-4
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
R @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: processing is not defined

Expression: "processing"

 input#font-file.form-control
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: hasFile is not defined

Expression: "hasFile"

 div.form-text
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: fileName is not defined

Expression: "fileName"

 span
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: processing is not defined

Expression: "processing"

 input#font-url.form-control
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: fontUrl is not defined

Expression: "fontUrl"

 input#font-url.form-control
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
c @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: hasFile is not defined

Expression: "(!hasFile && !fontUrl) || processing"

 button.btn.btn-primary
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: processing is not defined

Expression: "processing"

 span.spinner-border.spinner-border-sm.me-2
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: processing is not defined

Expression: "processing ? 'Analyzing...' : 'Analyze Font'"

 span
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: error is not defined

Expression: "error"

 div.alert.alert-danger
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: error is not defined

Expression: "error"

 div.alert.alert-danger
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: result is not defined

Expression: "result"

 div.card
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:1 Alpine Expression Error: result is not defined

Expression: "result"

 <div x-html=​"result">​undefined​</div>​
re @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
Promise.catch
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: fontAnalyzer is not defined
    at [Alpine] fontAnalyzer (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at R (cdn.min.js:5:143)
    at Function.<anonymous> (cdn.min.js:5:34273)
    at r (cdn.min.js:5:2323)
    at n (cdn.min.js:5:2353)
    at fr (cdn.min.js:5:2363)
    at S (cdn.min.js:5:5131)
    at cdn.min.js:5:4561
[Alpine] fontAnalyzer @ VM177:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
R @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: processing is not defined
    at [Alpine] processing (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33747
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at vn (cdn.min.js:5:33741)
    at r (cdn.min.js:5:2323)
[Alpine] processing @ VM178:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: hasFile is not defined
    at [Alpine] hasFile (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:35180
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:35174)
    at r (cdn.min.js:5:2323)
[Alpine] hasFile @ VM180:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: fileName is not defined
    at [Alpine] fileName (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33251
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:33244)
    at r (cdn.min.js:5:2323)
[Alpine] fileName @ VM181:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: processing is not defined
    at [Alpine] processing (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33747
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at vn (cdn.min.js:5:33741)
    at r (cdn.min.js:5:2323)
[Alpine] processing @ VM178:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: fontUrl is not defined
    at [Alpine] fontUrl (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at c (cdn.min.js:5:30780)
    at cdn.min.js:5:31752
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:31739)
[Alpine] fontUrl @ VM182:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
c @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: hasFile is not defined
    at [Alpine] (!hasFile && !fontUrl) || processing (eval at <anonymous> (https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js:5:665), <anonymous>:3:34)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33747
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at vn (cdn.min.js:5:33741)
    at r (cdn.min.js:5:2323)
[Alpine] (!hasFile && !fontUrl) || processing @ VM184:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
vn @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: processing is not defined
    at [Alpine] processing (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:35180
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:35174)
    at r (cdn.min.js:5:2323)
[Alpine] processing @ VM178:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: processing is not defined
    at [Alpine] processing ? 'Analyzing...' : 'Analyze Font' (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33251
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:33244)
    at r (cdn.min.js:5:2323)
[Alpine] processing ? 'Analyzing...' : 'Analyze Font' @ VM186:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: error is not defined
    at [Alpine] error (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:35180
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:35174)
    at r (cdn.min.js:5:2323)
[Alpine] error @ VM187:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: error is not defined
    at [Alpine] error (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33251
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:33244)
    at r (cdn.min.js:5:2323)
[Alpine] error @ VM187:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: result is not defined
    at [Alpine] result (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:35180
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:35174)
    at r (cdn.min.js:5:2323)
[Alpine] result @ VM188:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
cdn.min.js:5 Uncaught ReferenceError: result is not defined
    at [Alpine] result (eval at <anonymous> (cdn.min.js:5:665), <anonymous>:3:32)
    at cdn.min.js:5:1068
    at or (cdn.min.js:1:4957)
    at cdn.min.js:5:33363
    at r (cdn.min.js:5:18580)
    at Object.rn [as effect] (cdn.min.js:5:18368)
    at N (cdn.min.js:1:398)
    at cdn.min.js:1:511
    at Function.<anonymous> (cdn.min.js:5:33356)
    at r (cdn.min.js:5:2323)
[Alpine] result @ VM188:3
(anonymous) @ cdn.min.js:5
or @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
rn @ cdn.min.js:5
N @ cdn.min.js:1
(anonymous) @ cdn.min.js:1
(anonymous) @ cdn.min.js:5
r @ cdn.min.js:5
n @ cdn.min.js:5
fr @ cdn.min.js:5
S @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
gr @ cdn.min.js:5
(anonymous) @ cdn.min.js:5
pyscript-alpinejs.html:348 Fallback initialization for Alpine.js data
core.js:142 Deprecated: use <script type="py"> for an always safe content parsing:
 
from fontTools.ttLib import TTFont
import io
import js
import pyodide.http

async def fetch_font_from_url(url):
    try:
        print(f"Fetching font from URL: {url}")
        
        # Add custom headers to help with CORS issues
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        # List of CORS proxies to try
        cors_proxies = [
            "https://corsproxy.io/?url=",
            "https://api.allorigins.win/raw?url=",
            "https://cors.eu.org/",
            "https://xofix.4kb.dev/?url=",
            "https://corsproxy.org/?",
            "https://cors-proxy.htmldriven.com/?url="
        ]
        
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
                        return await response.bytes()
                except Exception as raw_error:
                    print(f"Raw URL request failed: {str(raw_error)}")
        
        # Try each CORS proxy in sequence
        for proxy in cors_proxies:
            proxy_url = f"{proxy}{url}"
            print(f"Trying CORS proxy: {proxy}")
            try:
                response = await pyodide.http.pyfetch(proxy_url, headers=headers)
                if response.status == 200:
                    font_bytes = await response.bytes()
                    print(f"Successfully fetched {len(font_bytes)} bytes via proxy: {proxy}")
                    return font_bytes
                else:
                    print(f"Proxy {proxy} request failed with status: {response.status}")
            except Exception as proxy_error:
                print(f"Proxy {proxy} request failed: {str(proxy_error)}")
        
        # Try direct URL as fallback
        print("Trying direct URL request")
        response = await pyodide.http.pyfetch(url, headers=headers)
        if response.status == 200:
            return await response.bytes()
        else:
            print(f"Direct request failed with status: {response.status}")
            
            # Try with no-cors mode as a last resort
            print("Attempting with no-cors mode")
            try:
                response = await pyodide.http.pyfetch(url, headers=headers, mode="no-cors")
                return await response.bytes()
            except Exception as no_cors_error:
                print(f"No-cors request failed: {str(no_cors_error)}")
        
        # If we got here, all attempts failed
        print("All fetch attempts failed")
        return None
    except Exception as e:
        print(f"Error fetching font: {str(e)}")
        return None

def analyze_font(font_data):
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
    
    # Create a list to store the name table data
    name_data = []
    
    for record in name_table.names:
        try:
            name_id = record.nameID
            platform_id = record.platformID
            string = record.toUnicode()
            name_data.append({"Name ID": name_id, "Platform ID": platform_id, "String": string})
        except:
            name_data.append({"Name ID": record.nameID, "Platform ID": record.platformID, "String": "(could not decode)"})
    
    # Format the output as HTML
    output = f"""
<h5>Font Information</h5>
<p><strong>Family Name:</strong> {get_name(1)}</p>
<p><strong>Subfamily:</strong> {get_name(2)}</p>
<p><strong>Full Name:</strong> {get_name(4)}</p>
<p class="mb-4"><strong>Units Per Em (UPM):</strong> {upm}</p>
<p class="mb-4"><strong>Number of Glyphs:</strong> {len(font.getGlyphOrder())}</p>

<h5>Name Table Entries</h5>
<div class="table-responsive">
  
"""
    
    # Add table rows
    for entry in name_data:
        output += f"""
      """
    
    output += """
    <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Name ID</th>
        <th>Platform ID</th>
        <th>String</th>
      </tr>
    </thead>
    <tbody><tr>
        <td>{entry['Name ID']}</td>
        <td>{entry['Platform ID']}</td>
        <td>{entry['String']}</td>
      </tr></tbody>
  </table>
</div>
"""
    return output

# Function to be called from JavaScript for uploaded files
def process_font(font_data_js):
    try:
        # Convert JS Uint8Array to Python bytes
        font_data = bytes(font_data_js.to_py())
        result = analyze_font(font_data)
        return result
    except Exception as e:
        print(f"Error analyzing font: {str(e)}")
        return f'<div class="alert alert-danger">Error analyzing font: {str(e)}</div>'

# Function to be called from JavaScript for URLs
async def process_font_url(url):
    try:
        print(f"Processing font URL: {url}")
        font_data = await fetch_font_from_url(url)
        if font_data:
            result = analyze_font(font_data)
            return result
        else:
            return '<div class="alert alert-danger">Error fetching font from URL. Check the console for details.</div>'
    except Exception as e:
        print(f"Error processing font URL: {str(e)}")
        return f'<div class="alert alert-danger">Error processing font URL: {str(e)}</div>'

# Signal that Python is ready
js.console.log("Python code loaded and ready")
  
c @ core.js:142
connectedCallback @ core.js:347
await in connectedCallback
(anonymous) @ core.js:325
Promise.then
(anonymous) @ core.js:188
pyscript-alpinejs.html:335 PyScript is ready, initializing Alpine.js data
pyscript-alpinejs.html:356 Secondary fallback initialization for Alpine.js data
pyodide.asm.js:10 Python code loaded and ready

```


### [x] http://127.0.0.1:8080/_pyscript-htmx.html

Refactored PyScript readiness check and JS-Python interaction. HTMX usage is minimal (indicator only). Renamed to `_pyscript-htmx.html`. Multiple "Starting font analysis" logs should be resolved.

console: 

```
pyscript-htmx.html:434 DOM loaded, waiting for PyScript
core.js:142 Deprecated: use <script type="py"> for an always safe content parsing:
 
from fontTools.ttLib import TTFont
import io
import js
import json
import pyodide.http
import sys
import traceback

# Set up logging to JavaScript console
def log_to_js(message):
    js.console.log(f"[Python] {message}")
    debug_div = js.document.getElementById("debug-info")
    if debug_div:
        debug_div.innerHTML += f"<div>[Python] {message}</div>"

async def fetch_font_from_url(url):
    try:
        log_to_js(f"Fetching font from URL: {url}")
        
        # Use a more robust URL fetching approach with custom headers
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

        
        # If it's a GitHub URL, try to use a more direct approach first
        if "github.com" in url and "raw" in url:
            # Try to convert to raw.githubusercontent.com if not already
            if "raw.githubusercontent.com" not in url:
                # Convert github.com URL to raw.githubusercontent.com
                raw_url = url.replace("github.com", "raw.githubusercontent.com")
                raw_url = raw_url.replace("/blob/", "/")
                log_to_js(f"Converted to raw URL: {raw_url}")
                try:
                    response = await pyodide.http.pyfetch(raw_url, headers=headers)
                    if response.status == 200:
                        font_bytes = await response.bytes()
                        log_to_js(f"Successfully fetched {len(font_bytes)} bytes from raw URL")
                        return font_bytes
                except Exception as raw_error:
                    log_to_js(f"Raw URL request failed: {str(raw_error)}")
        
        # Try each CORS proxy in sequence
        for proxy in cors_proxies:
            proxy_url = f"{proxy}{url}"
            log_to_js(f"Trying CORS proxy: {proxy_url}")
            try:
                response = await pyodide.http.pyfetch(proxy_url, headers=headers)
                if response.status == 200:
                    font_bytes = await response.bytes()
                    log_to_js(f"Successfully fetched {len(font_bytes)} bytes using proxy: {proxy}")
                    return font_bytes
                else:
                    log_to_js(f"Proxy {proxy} request failed with status {response.status}")
            except Exception as proxy_error:
                log_to_js(f"Proxy {proxy} request failed: {str(proxy_error)}")
        
        # Try direct URL as fallback
        log_to_js("Trying direct URL request")
        try:
            response = await pyodide.http.pyfetch(url, headers=headers)
            if response.status == 200:
                font_bytes = await response.bytes()
                log_to_js(f"Successfully fetched {len(font_bytes)} bytes from direct URL")
                return font_bytes
            else:
                log_to_js(f"Direct request failed with status {response.status}")
                
                # Try with no-cors mode as a last resort
                log_to_js("Attempting with no-cors mode")
                try:
                    response = await pyodide.http.pyfetch(url, headers=headers, mode="no-cors")
                    font_bytes = await response.bytes()
                    log_to_js(f"Successfully fetched {len(font_bytes)} bytes with no-cors mode")
                    return font_bytes
                except Exception as no_cors_error:
                    log_to_js(f"No-cors request failed: {str(no_cors_error)}")
        except Exception as direct_error:
            log_to_js(f"Direct request failed: {str(direct_error)}")
        
        # If we got here, all attempts failed
        log_to_js("All fetch attempts failed")
        raise Exception("Failed to fetch font. CORS policy may be blocking the request. Try downloading the font and uploading it directly.")
            
    except Exception as e:
        error_details = traceback.format_exc()
        log_to_js(f"Error fetching font: {str(e)}")
        log_to_js(f"Error details: {error_details}")
        return None

def analyze_font(font_data):
    try:
        log_to_js(f"Analyzing font data ({len(font_data)} bytes)")
        
        # Load the font from bytes
        font_io = io.BytesIO(font_data)
        font = TTFont(font_io)
        
        # Get UPM value
        upm = font["head"].unitsPerEm
        log_to_js(f"Font UPM: {upm}")
        
        # Get name table entries
        name_table = font["name"]
        
        # Helper to get name
        def get_name(nameID):
 
c @ core.js:142
connectedCallback @ core.js:347
await in connectedCallback
(anonymous) @ core.js:325
Promise.then
(anonymous) @ core.js:188
pyscript-htmx.html:434 Starting font analysis
pyodide.asm.js:10 Python code loaded and ready
pyscript-htmx.html:434 Starting font analysis
pyscript-htmx.html:434 Starting font analysis

```

### [x] http://127.0.0.1:8080/_pyscript-indexeddb.html

Added safeguards and logging for PyScript initialization. The error "ReferenceError: pyscript is not defined" should be resolved by ensuring code accessing `pyscript.interpreter` only runs after `py:ready` and confirms availability. Renamed to `_pyscript-indexeddb.html`.

### [x] http://127.0.0.1:8080/_pyscript-lit.html

Refactored Lit component to correctly handle PyScript readiness using an `isPyScriptReady` property and updated Python function calls. Added logging for better debugging. Renamed to `_pyscript-lit.html`. The "Processing... and nothing happens" issue should be resolved or provide clearer errors.

FIXME: On click I get

```
Font Analyzer
Upload a TTF or OTF font file to analyze its properties, or provide a URL.

Font File:
No file chosen
Font URL:
https://github.com/google/fonts/raw/refs/heads/main/ofl/abrilfatface/AbrilFatface-Regular.ttf
If both file and URL are provided, the file will be used.
Processing...
```

and nothign happens. 

### [x] http://127.0.0.1:8080/_pyscript-preact-signals.html

Refactored to ensure Preact component logic only calls PyScript functions after `py:ready` event. Added a global flag `isPyScriptReady` and checks within the component's methods. Corrected PyScript interpreter access. Renamed to `_pyscript-preact-signals.html`. The "pyscript is not defined" error on click should be resolved.

FIXME On click I get

```
Font Inspector
Upload Font File
Select a TTF or OTF font file to analyze its properties, or provide a URL.

Font File:No file chosen
Font URL:
https://github.com/google/fonts/raw/refs/heads/main/ofl/abrilfatface/AbrilFatface-Regular.ttf
If both file and URL are provided, the file will be used.
Error
Error: pyscript is not defined
```

### [x] http://127.0.0.1:8080/pyscript-puepy-bootstrap.html

Works fully correctly!

### [x] http://127.0.0.1:8080/pyscript-puepy-bulma.html

Implemented Bulma tabs in the PuePy component to separate "Font File" upload and "Font URL" input fields. This involved adding a state variable for the active tab and conditionally rendering the input sections. (No rename needed as it was a FIXME for an existing file).

### [x] http://127.0.0.1:8080/pyscript-puepy-frankenui.html

Works fully correctly!

### [x] http://127.0.0.1:8080/pyscript-puepy-uikit.html

Works fully correctly!

### [!] http://127.0.0.1:8080/pyscript-solidjs.html

FIXME: Initial investigation of console errors:
- `SyntaxError: Unexpected token 'export'` in `solid.js` (UMD build)
- `ReferenceError: Babel is not defined`
Attempted to fix Babel load order. The `Unexpected token 'export'` in Solid.js UMD suggests a more fundamental issue with its loading or compatibility in this environment. In-browser JSX compilation for Solid without `babel-preset-solid` is also complex.
**Recommendation:** Defer deep fix or consider removal per "don't overdo" guideline. This example may require a more modern setup (e.g., pre-compilation or using Solid with `htm`). Marking with `[!` for further review/decision.

blank page, Console

```
solid.js:1665 Uncaught SyntaxError: Unexpected token 'export'
pyscript-solidjs.html:11 Uncaught ReferenceError: Babel is not defined
    at pyscript-solidjs.html:11:5
```

Question: Does it make sense at all? Can we make it work? Or is this some hallucinated shit? Delete the file if you think it's not worth the effort. 

### [!] http://127.0.0.1:8080/pyscript-svelte.html

FIXME: Initial investigation of console error:
- `TypeError: Svelte is not a constructor`
The current code attempts to use Svelte by loading `svelte.min.js` and then overwriting `window.Svelte` with a custom shim that doesn't correctly represent Svelte's component system or compilation. This approach is fundamentally flawed for using Svelte components, which typically require a compilation step.
**Recommendation:** Defer deep fix or consider removal per "don't overdo" guideline. This example requires a significant architectural change to correctly use Svelte (e.g., pre-compilation or an in-browser Svelte compiler). Marking with `[!` for further review/decision.

blank page, console: 

```
pyscript-svelte.html:411 Error creating Svelte app: TypeError: Svelte is not a constructor
    at HTMLDocument.<anonymous> (pyscript-svelte.html:406:19)
    at O (utils.js:44:12)
    at HTMLElement.connectedCallback (core.js:354:29)
(anonymous) @ pyscript-svelte.html:411
```

Question: Does it make sense at all? Can we make it work? Or is this some hallucinated shit? Delete the file if you think it's not worth the effort. 

### [x] http://127.0.0.1:8080/_pyscript-vuejs.html

The Python code generating HTML for the table had an unterminated string literal error due to quote handling. This was fixed by ensuring HTML attributes use single quotes within the triple-quoted Python f-string. Renamed to `_pyscript-vuejs.html`.

FIXME, after loading the page I get: 

```
PyScript with Vue.js
Font Analyzer
Upload a TTF or OTF font file to analyze its properties, or provide a URL.

Font File:
No file chosen
Font URL:
https://github.com/google/fonts/raw/refs/heads/main/ofl/abrilfatface/AbrilFatface-Regular.ttf
If both file and URL are provided, the file will be used.
Analyze Font
Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async
    await CodeRunner(
          ^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 285, in __init__
    self.ast = next(self._gen)
               ^^^^^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 149, in _parse_and_compile_gen
    mod = compile(source, filename, mode, flags | ast.PyCF_ONLY_AST)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 121
    output += "<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
                                                                                               ^
SyntaxError: unterminated string literal (detected at line 121)
```

console

```
vue.global.js:12288 You are running a development build of Vue.
Make sure to use the production build (*.prod.js) when deploying for production.
core.js:142 Deprecated: use <script type="py"> for an always safe content parsing:
 
from fontTools.ttLib import TTFont
import io
import js
import pyodide.http

async def fetch_font_from_url(url):
    try:
        # Add custom headers to help with CORS issues
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        # List of CORS proxies to try
        cors_proxies = [
            "https://corsproxy.io/?url=",
            "https://api.allorigins.win/raw?url=",
            "https://cors.eu.org/",
            "https://xofix.4kb.dev/?url="
        ]

        
        # If it's a GitHub URL, try to use a more direct approach first
        if "github.com" in url and "raw" in url:
            # Try to convert to raw.githubusercontent.com if not already
            if "raw.githubusercontent.com" not in url:
                # Convert github.com URL to raw.githubusercontent.com
                raw_url = url.replace("github.com", "raw.githubusercontent.com")
                raw_url = raw_url.replace("/blob/", "/")
                print(f"Converted to raw URL: {raw_url}")
                try:
                    response = await pyodide.http.pyfetch(raw_url, headers=headers)
                    if response.status == 200:
                        return await response.bytes()
                except Exception as raw_error:
                    print(f"Raw URL request failed: {str(raw_error)}")
        
        # Try each CORS proxy in sequence
        for proxy in cors_proxies:
            proxy_url = f"{proxy}{url}"
            print(f"Trying CORS proxy: {proxy}")
            try:
                response = await pyodide.http.pyfetch(proxy_url, headers=headers)
                if response.status == 200:
                    return await response.bytes()
                else:
                    print(f"Proxy {proxy} request failed with status: {response.status}")
            except Exception as proxy_error:
                print(f"Proxy {proxy} request failed: {str(proxy_error)}")
        
        # Try direct URL as fallback
        print("Trying direct URL request")
        response = await pyodide.http.pyfetch(url, headers=headers)
        if response.status == 200:
            return await response.bytes()
        else:
            print(f"Direct request failed with status: {response.status}")
            
            # Try with no-cors mode as a last resort
            print("Attempting with no-cors mode")
            try:
                response = await pyodide.http.pyfetch(url, headers=headers, mode="no-cors")
                return await response.bytes()
            except Exception as no_cors_error:
                print(f"No-cors request failed: {str(no_cors_error)}")
        
        # If we got here, all attempts failed
        print("All fetch attempts failed")
        return None
    except Exception as e:
        print(f"Error fetching font: {str(e)}")
        return None

def analyze_font(font_data):
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
    
    # Create a list to store the name table data
    name_data = []
    
    for record in name_table.names:
        try:
            name_id = record.nameID
            platform_id = record.platformID
            string = record.toUnicode()
            name_data.append({"Name ID": name_id, "Platform ID": platform_id, "String": string})
        except:
            name_data.append({"Name ID": record.nameID, "Platform ID": record.platformID, "String": "(could not decode)"})
    
    # Format the output as HTML
    output = f"""
<h3>Font Information</h3>
<p><strong>Family Name:</strong> {get_name(1)}</p>
<p><strong>Subfamily:</strong> {get_name(2)}</p>
<p><strong>Full Name:</strong> {get_name(4)}</p>
<p><strong>Units Per Em (UPM):</strong> {upm}</p>
<p><strong>Number of Glyphs:</strong> {len(font.getGlyphOrder())}</p>

<h3>Name Table Entries</h3>

"""
    
    # Add table rows
    for entry in name_data:
        output += f"""
  """
    
    output += "<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
  <tbody><tr>
    <th>Name ID</th>
    <th>Platform ID</th>
    <th>String</th>
  </tr><tr>
    <td>{entry['Name ID']}</td>
    <td>{entry['Platform ID']}</td>
    <td>{entry['String']}</td>
  </tr></tbody></table>"
    return output

# Function to be called from JavaScript for uploaded files
def process_font(font_data_js):
    try:
        # Convert JS Uint8Array to Python bytes
        font_data = bytes(font_data_js.to_py())
        result = analyze_font(font_data)
        return result
    except Exception as e:
        return f"<p class="error">Error analyzing font: {str(e)}</p>"

# Function to be called from JavaScript for URLs
async def process_font_url(url):
    try:
        font_data = await fetch_font_from_url(url)
        if font_data:
            result = analyze_font(font_data)
            return result
        else:
            return "<p class="error">Error fetching font from URL</p>"
    except Exception as e:
        return f"<p class="error">Error processing font URL: {str(e)}</p>"
  
c @ core.js:142
connectedCallback @ core.js:347
await in connectedCallback
(anonymous) @ core.js:325
Promise.then
(anonymous) @ core.js:188
error.js:20 PythonError: Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async
    await CodeRunner(
          ^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 285, in __init__
    self.ast = next(self._gen)
               ^^^^^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 149, in _parse_and_compile_gen
    mod = compile(source, filename, mode, flags | ast.PyCF_ONLY_AST)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 121
    output += "<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
                                                                                               ^
SyntaxError: unterminated string literal (detected at line 121) (at pyodide.asm.js:10:10009)

    at new_error (pyodide.asm.js:10:10009)
    at pyodide.asm.wasm:0x16e384
    at pyodide.asm.wasm:0x17855f
    at pyodide.asm.wasm:0x328642
    at pyodide.asm.wasm:0x1c44db
    at pyodide.asm.wasm:0x2ca38d
    at pyodide.asm.wasm:0x20c2d8
    at pyodide.asm.wasm:0x1c4bc2
    at pyodide.asm.wasm:0x1c4ed1
    at pyodide.asm.wasm:0x1c4f4f
    at pyodide.asm.wasm:0x2a0d61
    at pyodide.asm.wasm:0x2a72bf
    at pyodide.asm.wasm:0x1c508f
    at pyodide.asm.wasm:0x1c4cf8
    at pyodide.asm.wasm:0x177bbf
    at callPyObjectKwargs (pyodide.asm.js:10:62939)
    at Module.callPyObjectMaybePromising (pyodide.asm.js:10:64121)
    at wrapper (pyodide.asm.js:10:27499)
    at onGlobalMessage (pyodide.asm.js:10:101572)
d @ error.js:20
ke @ _python.js:67
await in ke
(anonymous) @ pyodide.js:19
N.e.<computed> @ utils.js:79
await in N.e.<computed>
(anonymous) @ hooks.js:54
await in (anonymous)
runAsync @ utils.js:60
connectedCallback @ core.js:358
await in connectedCallback
(anonymous) @ core.js:325
Promise.then
(anonymous) @ core.js:188

```

### [x] http://127.0.0.1:8080/_pyscript-webcomponents.html

Refactored the web component to correctly re-attach event listeners in its `render` method and ensured PyScript interpreter is accessed safely. Added logging. This should address the "spins forever" issue. Renamed to `_pyscript-webcomponents.html`.

FIXME: after I click the button I get: 

```
Upload Font File
Select a TTF or OTF font file to analyze its properties, or provide a URL.

Font File:
No file chosen
Font URL:
https://github.com/google/fonts/raw/refs/heads/main/ofl/abrilfatface/AbrilFatface-Regular.ttf
If both file and URL are provided, the file will be used.
Processing...
```

and "Analyzing font file..." spins forever. 

### THEN CHECK AGAIN
