import * as express from 'express';
import * as http from 'http';
import * as bodyParser from 'body-parser';

import * as debug from 'debug';

const log = debug('rideable:http');

const PORT = process.env.PORT || 3000;

import { getNearestStaion, getBalance, shareRide } from './python';

export function createWebServer() {
    return new Promise((resolve, reject) => {

        log(`Starting server on port: ${PORT}`);

        const app = express();

        // Explicitly create the http server to reuse for websocket if needed
        const server = http.createServer(app);
        server.listen(PORT, () => {
            log(`HTTP server ready.`);
            return resolve();
        });

        // CORS
        app.use((req, res, next) => {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            next();
        });

        // Allow (parse) JSON body requests
        app.use(bodyParser.json());

        // Debug each request
        app.use((req, res, next) => {
            log(`${req.method}: ${req.path}`);
            // log(req.body);
            next();
        });

        // Routes here
        app.get('/', (req, res) => {
            return res.send('hello world!');
        });

        // Accept origin and destination lat/lng and find nearest subway station
        app.post('/findStations', (req, res) => {
            const origin = req.body.origin;
            const destination = req.body.destination;
            const disability = req.body.disability || 0;
            log(origin);
            log(destination);

            const response: any = {};

            Promise.resolve()
                .then(() => getNearestStaion(origin.lat, origin.lng, disability))
                .then(result => {
                    response.origin = result;
                })
                .then(() => getNearestStaion(destination.lat, destination.lng, disability))
                .then(result => {
                    response.destination = result;
                })
                .then(() => {
                    return res.send(response);
                })
        });

        app.post('/reportOutage', (req, res) => {
            const type = req.body.type;
            const location = req.body.location;
            console.log(type, location)
            res.send('ok');
        });

        app.post('/checkBalance', (req, res) => {
            const rfid = req.body.rfid;
            console.log(rfid)
            getBalance(rfid).then(result => {
                console.log(result)
                res.send(result);
            })
        });

        app.post('/shareRide', (req, res) => {
            const rfidFrom = req.body.rfidFrom;
            const rfidTo = req.body.rfidTo;

            console.log(rfidFrom, rfidTo)
            shareRide(rfidFrom, rfidTo).then(result => {
                console.log(result)
                res.send(result);
            })
        });
    });

}