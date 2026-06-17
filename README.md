Supply Chain Attack Simulation
This project demonstrates a Supply Chain Attack, where an attacker compromises a website by poisoning a third-party dependency. In this scenario, I simulated how an external script can be used to steal session data from an unsuspecting user.

The Process
Attacker Infrastructure: I set up a "listener" endpoint on my server. Its job is to secretly collect and display any information that is sent to it, acting as the attacker's central data collection point.

[https://github.com/alisip-3/Python_PickWiz/blob/main/1.server_log.png]

The Victim Site: I modified a webpage to include an external script (a fake accessibility tool). This mimics real-world scenarios where websites trust external code that might be malicious.

[Insert Screenshot: The HTML of the banking site]

User Simulation: To prove the attack works, I simulated a real user session by manually setting a bank_session cookie. This represents the sensitive data the attacker wants to steal.

[Insert Screenshot: The cookie set in the console]

Data Exfiltration: Once the page loads, the malicious script automatically runs in the background. It extracts the sensitive cookie and sends it to the listener endpoint I created in step 1.

[Insert Screenshot: The Network tab showing the data being sent]

Results: The data is successfully received and recorded in the server logs, confirming that the "stolen" information has been exfiltrated from the user's browser.

[Insert Screenshot: The log in Render showing the stolen cookie]
