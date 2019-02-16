import * as express from 'express';
import * as http from 'http';
import * as bodyParser from 'body-parser';

import * as debug from 'debug';

const log = debug('rideable:http');

const PORT = process.env.PORT || 3000;

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
            next();
        });

        app.get('/', (req, res) => {
            return res.send('hello world!');
        });
    });

}