// Notes: 
// https://cloud.google.com/appengine/docs/flexible/nodejs/using-cloud-sql
// https://medium.com/@austinhale/building-a-node-api-with-express-and-google-cloud-sql-9bda260b040f

import * as mysql from 'mysql';

import * as debug from 'debug';

const log = debug('rideable:db');

const host = process.env.SQL_HOST;
if (!host) throw new Error('missing process.env.SQL_HOST!');

const user = process.env.SQL_USER;
if (!user) throw new Error('missing process.env.SQL_USER!');

const password = process.env.SQL_PASSWORD;
if (!password) throw new Error('missing process.env.SQL_PASSWORD!');

const database = process.env.SQL_DATABASE;
if (!database) throw new Error('missing process.env.SQL_DATABASE!');

const config: any = {
  host, user, database, password
};

if (process.env.INSTANCE_CONNECTION_NAME && process.env.NODE_ENV === 'production') {
  config.socketPath = `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`;
}

let instance: mysql.Connection;

export function connectDatabase() {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(config);
    connection.connect((error) => {
      if (error) {
        console.error('Error connecting: ' + error.stack);
        return reject(error);
      }
      log('Connected as thread id: ' + connection.threadId);
      instance = connection;
      return resolve(connection);
    });
  });
}

