# Security Analysis Report: Supply Chain Attack Simulation

## Overview ##

This project serves as a Proof of Concept (PoC) demonstrating a Supply Chain Attack. The simulation highlights how third-party dependencies—even those intended for minor UI improvements—can be weaponized to compromise sensitive user session data

##Attack Workflow##
1. Dependency Injection: A malicious script is injected into the web application, simulating a compromised third-party library that the application trusts.

2.Session Creation: When a user logs into the application, the browser generates a valid session_token cookie.

3.Data Exfiltration: The malicious script, running within the application's origin, automatically accesses document.cookie, extracts the session token, and exfiltrates it to an external Command & Control (C2) server.

4.Impact: The attacker receives the stolen session token, enabling them to perform Session Hijacking.

##Vulnerability Analysis##
###The core vulnerability is the excessive trust in third-party scripts.###

- Lack of Isolation: Scripts running in the browser share the same origin and have access to sensitive data such as cookies.

- Implicit Trust: Applications often load external scripts without verifying their integrity or restricting their capabilities.

##Mitigation & Prevention##
###To defend against such attacks, the following security controls should be implemented:###

- Content Security Policy (CSP): Implement a strict CSP to restrict where scripts can be loaded from and, more importantly, to prevent the exfiltration of data to unauthorized external domains (using connect-src).

- Subresource Integrity (SRI): Use SRI hashes to ensure that the browser only executes files that match a known, verified cryptographic hash.

- HttpOnly Cookies: Set the HttpOnly flag on sensitive cookies (like session tokens). This prevents document.cookie from accessing them via JavaScript, rendering this specific attack ineffective.

- Dependency Auditing: Regularly audit and update third-party libraries and avoid loading external scripts from untrusted or unverified sources.

###Tools Used:###

Frontend: HTML5, JavaScript

Backend (C2 Server): Flask (Python)

Deployment: Render
