import 'source-map-support/register'
import 'dotenv/config'

import { createWebServer } from './server';
import { connectDatabase } from './db';

connectDatabase()
.then(() => {
    return createWebServer();
}).then(() => {
    console.log('**ready**');
}).catch(error => {
    console.log(error);
});
