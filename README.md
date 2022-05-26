# DNS Resolver
## Overview 
This is a DNS resolver python script that takes a domain name as input and resolves this query by first contacting the root server, then the top-level domain, all the way until the authoritative name server.
## Libraries Needed
dnspython --> "pip install dnspython"
## How to Execute 
```
Step 1: Open your favorite IDE (preferrably PyCharm). 
Step 2: Navigate to and execute the main class: main.py.
Step 3: When prompted, enter the name of the domain in which you would like to query.
```
## Output
```
Question Section - Shows the domain which is being queried.
Answer Section - Displays the IP address or the CNAME of the DNS query.
Query time - Displays the time it took to run the query.
When - Displays the time and date the query took place.
```