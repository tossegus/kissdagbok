# Potty-training web service

## Setup
Change the `db_path` variable in flask_app.py to point to where your database should be located.
Run the following to start up a flask webpage on <ip>:5000:
`./mainfile.py <IP>`

The port isn't configurable since me myself don't have a need for it right now.

## My setup
I'm running this as a service on a RPI and access it either from my RPI with an external display, or using my phone (via wifi or VPN).
It works fairly well.

## Disclaimer
Everything is written in Swenglish with questionable design decisions (since I threw this together in a couple of downtime during potty training).

## Todos
- Add language options
- Add analysis tools (Calculate the most common time between toilet visits. List common times for potty etc.)
- Add daily stats (#hits/#total. Could be disheartening though).
- Lint the code
- Structure the database in a smarter way
- Change from entries -> named tuple perhaps.
