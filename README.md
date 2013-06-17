opentaba-address-db
===================

Setting up a development environment
------------------------------------
Clone the repository locally, then run:
    $ pip install -r requirements.txt

Make sure you have a local mongoDB server running, and run:
    $ python create_db.py --force
To create the DB initially.

To run the webserver, execute:
    $ python app.py
    
The API
-------

### Locating a Gush by Address ###
Execute a GET request to `/locate/<addr>` where `<addr>` is the address you want to look up.
The response is a JSON object, and it looks like:
    {"lat": <latitude>, "lon": <longitude>, "gush_id": <gushid>}
    
