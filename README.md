# Security Analysis Report: Supply Chain Attack Simulation

### Overview ###

This project serves as a Proof of Concept (PoC) demonstrating a Supply Chain Attack. The simulation highlights how third-party dependencies—even those intended for minor UI improvements can be weaponized to compromise sensitive user session data

## Live Demo
You can test the simulation here:
[Click here to access the Simulated Bank Login](https://python-pickwiz.onrender.com/secure-zone)
*(Note: This is a security demonstration. The cookie theft is purely for educational purposes and captured in the logs.)*

## Attack Workflow ##

1. Setting up the C2 Server
I created a Python server (using Flask) that acts as my "Command & Control" (C2) server. The server listens for incoming requests at a specific endpoint (/log) and logs any data received from the browser.

![Figure 1: The backend server code, waiting to receive and log incoming](https://github.com/alisip-3/Cookie-Exfiltration-PoC/blob/main/1.server.png)

2. Malicious Code Injection
I embedded a small snippet of JavaScript into the login page. This script mimics a trusted external library, but it is triggered as soon as the user logs in.

![Figure 2: The malicious script in the HTML, waiting for the user to submit the login form.](https://github.com/alisip-3/Cookie-Exfiltration-PoC/blob/main/2.%20fetch.png)

3. Data Exfiltration
Once the user logs in, the browser generates a session cookie (session_token). The malicious script accesses document.cookie, extracts the token, and sends it to my server via an asynchronous fetch request.

![Figure 3: The browser's Network Tab showing the sensitive cookie being exfiltrated to my server.](https://github.com/alisip-3/Cookie-Exfiltration-PoC/blob/main/3.cookie.png)

4. Successful Capture
My server receives the request, extracts the cookie, and prints it to the logs. With this token, an attacker could impersonate the user without needing a password.

![Figure 4: The stolen session token appearing in my server logs, confirming the successful attack.](https://github.com/alisip-3/Cookie-Exfiltration-PoC/blob/main/4.log.png)

## Vulnerability Analysis ##
### The core vulnerability is the excessive trust in third-party scripts. ###

- Lack of Isolation: Scripts running in the browser share the same origin and have access to sensitive data such as cookies.

- Implicit Trust: Applications often load external scripts without verifying their integrity or restricting their capabilities.

## Mitigation & Prevention ##
### To defend against such attacks, the following security controls should be implemented: ###

- Content Security Policy (CSP): Implement a strict CSP to restrict where scripts can be loaded from and, more importantly, to prevent the exfiltration of data to unauthorized external domains (using connect-src).

- Subresource Integrity (SRI): Use SRI hashes to ensure that the browser only executes files that match a known, verified cryptographic hash.

- HttpOnly Cookies: Set the HttpOnly flag on sensitive cookies (like session tokens). This prevents document.cookie from accessing them via JavaScript, rendering this specific attack ineffective.

- Dependency Auditing: Regularly audit and update third-party libraries and avoid loading external scripts from untrusted or unverified sources.

### Tools Used: ###

Frontend: HTML5, JavaScript

Backend (C2 Server): Flask (Python)

Deployment: Render
