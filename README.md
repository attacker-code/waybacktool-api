Sure, here's how you could update your README.md file to reflect these changes:

---

# Wayback-Tool
A tool to fetch and verify the existence of endpoints from the Wayback Machine API. This tool has been updated to support Python 3.

### Features
* Pull URLs from Wayback Machine
* Check those URLs and provide URL, status code, response length, content-type, and redirect URL 
* Multithreaded
* Load and output to/from file
* Accepts stdin as input
* Optimizations made around old domains and timeouts

### Updates
With the transition to Python 3, there have been a few changes:

* The `print` statement now requires parentheses. So, instead of `print r.text.strip()`, use `print(r.text.strip())`.
* The `urlparse` module has been renamed to `urllib.parse`. So, if you're using Python 3, replace `import urlparse` with `from urllib.parse import urlparse`.

Here's the updated line in your code:

```python
from urllib.parse import urlparse
```

### Usage:
Fetch URLs:
```bash
$ python waybacktool.py pull --host example.com  
http://example.com/example.html  
https://example.com/testing.js  
https://example.com/test.css  
```

Check URLs:
```bash
$ python waybacktool.py pull --host example.com | python waybacktool.py check 
http://example.com/example.html, 200, 1024, text/html
https://example.com/testing.js, 301, 58, text/plain; charset=utf-8, https://example.com/testing1234.js
https://example.com/test.css, 403, 103, text/html
```

The design allows you to apply `grep` transformations to the output of the fetch URLs. For instance, the following is a valid usage:
```bash
$ python waybacktool.py pull --host example.com | grep html | python waybacktool.py check 
http://example.com/example.html, 200, 1024, text/html
```

Enjoy using this tool!