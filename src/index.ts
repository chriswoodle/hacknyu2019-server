import 'source-map-support/register'
import * as express from 'express';
import * as http from 'http';
import * as bodyParser from 'body-parser';

const PORT = process.env.PORT || 3000;

console.log(`Starting server on port: ${PORT}`);

const app = express();

// Explicitly create the http server to reuse for websocket if needed
const server = http.createServer(app);
server.listen(PORT, () => {
    console.log('**ready**');
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
    console.log(`${req.method}: ${req.path}`);
    next();
});

app.get('/', (req, res) => {
    return res.send('hello world!');
});