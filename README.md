# Banking Supply Chain Attack Simulation
### About the Project
In recent months, we’ve seen more and more companies integrating AI chatbots into their websites to improve customer service. Often, these bots are provided by third-party vendors. While this is great for UX, it creates a massive security blind spot: if the vendor's code is compromised, the company's website is compromised too.

**I built this project to simulate that exact scenario. I wanted to see how a "trusted" third-party component—like a help-desk chatbot could be used as a vector for a supply chain attack.**

 ## Live Demo
You can check out the simulation here: [[Live Link Here](https://python-pickwiz.onrender.com)]

(Note: Use your own username/password to log in it's just a simulation)

## How it Works
I created a full-stack banking dashboard simulation to act as the "victim" site. The core of the project is the AI chatbot integration:

**The Vector:** I embedded a chatbot widget into the bank's dashboard.

**The Payload:** The bot is scripted to provide a "helpful" link to the user. In reality, this link contains a hidden JavaScript function.

**The Exfiltration:** When the user clicks the link, the script stealthily captures the user's session cookie and sends it directly to my logging server.

I paid attention to the small details to make this feel like a real-world scenario—from the professional banking UI to the actual cookie handling. I even set up a dedicated backend logger to verify that the "stolen" data is successfully received, which allowed me to document the entire attack flow.

## Screenshots

![Banking Dashboard: A professional interface that builds trust.](images/login.png)
![The Attack: Showing the malicious link inside the AI chat widget.](images/chatbox.png)

![Proof of Concept: The Network tab showing the cookie being exfiltrated to the /log endpoint.](images/inspect.png)
![](images/log.png)

## Mitigation & Defense
How do we protect ourselves from this kind of attack? Here are the key security practices:

- Content Security Policy (CSP): Implementing a strict CSP would prevent the browser from sending data to unauthorized domains, effectively blocking the exfiltration part of the attack.

- Subresource Integrity (SRI): When using external scripts (like a chatbot), we should use SRI hashes to ensure that the code hasn't been tampered with or modified by the vendor.

- Principle of Least Privilege: Restricting what scripts can access (e.g., setting the HttpOnly flag on cookies makes them inaccessible to JavaScript).

- Third-Party Risk Management (TPRM): Before integrating external services, security teams must audit the vendor’s security posture and ensure they maintain a secure supply chainal.


## Disclaimer
This project is for educational purposes only. All data, including the banking dashboard, user authentication, and the "stolen" cookies, are part of a controlled simulation environment. No real-world systems, users, or financial data are harmed or involved. The purpose of this project is to showcase how security vulnerabilities function in order to learn how to defend against them.

### Tools Used: ###

Frontend: HTML5, JavaScript

Backend (C2 Server): Flask (Python)

Deployment: Render
