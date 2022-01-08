
After Golismero project got dead there is no more any up to date open-source tool that can collect links with parametrs and web-forms and then test them, so i decided to write one by my own. At the first step this tool does collect all the entry-points for the target website and then tryes to find open redirect vulnerability.  

Why this project is better than other open-redirect scanners? It does recursevely crawl all the links from the target website and finds potential vulnerable web-forms by itself instead of using CommonCrawl or getting links list from user input. In the future i will probably add more modules to fuzz for SQL Injections and XSS.

### Instalation  

`~$ git clone https://github.com/d34db33f-1007/fuzz300.git`  
`~$ pip3 install -r requirements.txt`  

### Usage  

`~$ python3.8 fuzz300.py https://example.com` 

After running you will also find newly created files with interesting links and all website entry-points.

### Tips

• Try using the same parameter twice: `?next=whitelisted.com&next=google.com`  
• If periods filtered, use an IPv4 address in decimal notation http://www.geektools.com/geektools-cgi/ipconv.cgi  
• Try a double-URL and triple-URL encoded version of payloads  
• Try redirecting to an IP address (instead of a domain) using different notations: IPv6, IPv4 in decimal, hex or octal  
• For XSS, try replacing `alert(1)` with `prompt(1)` & `confirm(1)`  
• If extension checked, try `?image_url={payload}/.jpg`  
• Try `target.com/?redirect_url=.uk` (or [any_param]=.uk). If it redirects to target.com.uk, then it’s vulnerable! target.com.uk and target.com are different domains.  
• Use `/U+e280` RIGHT-TO-LEFT OVERRIDE: `https://whitelisted.com@%E2%80%AE@moc.elgoog`  
------ The unicode character `U+202E` changes all subsequent text to be right-to-left  
------ E.g.: https://hackerone.com/reports/299403  

### Exploitation

• Phishing  
• Chaining open redirect with  
-- • SSRF  
-- • OAuth token disclosure  
-- • XSS  
-- • CRLF injection  


### Open redirect writeups

• [Hackerone report 158434](https://hackerone.com/reports/158434): Open Redirect & XSS on Shopify, $1,000  
• [Hackerone report 101962](https://hackerone.com/reports/101962): Open Redirect on Shopify, $500  
• [Hackerone report 55546](https://hackerone.com/reports/55546): Open Redirect on Shopify, $500  
• [Hackerone report 55525](https://hackerone.com/reports/55525): Open Redirect on Shopify, $500  
• [Hackerone report 169759](https://hackerone.com/reports/169759): Open Redirect on Shopify, $500  
• [Hackerone report 160047](https://hackerone.com/reports/160047): Open Redirect on Shopify, $500  
• [Hackerone report 103772](https://hackerone.com/reports/103772): Open Redirect on Shopify, $500  
• [Hackerone report 159522](https://hackerone.com/reports/159522): Open Redirect on Shopify, $500  
