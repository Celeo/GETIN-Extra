# GETIN-Extra

Additional web apps for the GETIN EVE alliance.

Feature areas:
* Wiki
* Fits

The wiki functions like a simple but easy-to-use wiki. The fits is a subset of that functionality, specifically for posting ship fittings and descriptions about them.

## Stack

This app uses Python ([Flask](http://flask.pocoo.org/)) for the server, with several extensions, and JavaScript ([Vue.js](https://vuejs.org/)) for the client.

## Setting up

1. Clone the repo
2. Create a virtualenv in the server directory and install the prereqs (`cd server && virtualenv env && source env/bin/activate && pip install -r requirements.txt`)
3. Install JS dependencies in the client directory (`cd client && yarn` or `cd client && npm i`)
4. Setup an app on the EVE Developers website at https://developers.eveonline.com
5. Create a config file (`cp server/config.example.cfg server/config.cfg`) and populate it with a secret key and the EVE Devs app info.
6. Run the dev server with `cd server && ./flask_debug.sh`
7. Run the dev client (in another terminal/screen/whatever) with `cd client && yarn dev` or `cd client && npm run dev`

## Deploying

1. Build production client files (`cd client && yarn build` or `cd client && npm run build`)
2. Copy those client files to the server
3. Copy the server files to the server
4. Create the same virtualenv on the server as you did on your dev machine
5. Setup a reverse proxy (like [Nginx](https://www.nginx.com/)) to serve the client files
6. Run the server with `cd server && ./gunicorn_run.sh`
