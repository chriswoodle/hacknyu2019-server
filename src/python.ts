import { exec } from 'child_process';
import * as path from 'path';
import * as debug from 'debug';

const log = debug('rideable:python-exec');

export function getNearestStaion(lat: string, lng: string, disability = 1, outputformat = 'json') {
    return new Promise((resolve, reject) => {
        const command = `python ${path.resolve(__dirname, '../scripts/getNearestStation.py')} ${lat} ${lng} ${disability} ${outputformat}`;
        exec(command, (error, stdout, stderr) => {
            if (error) {
                log(`exec error: ${error}`);
                return reject(error)
            }
            // console.log(`stdout: ${stdout}`);
            // console.log(`stderr: ${stderr}`);
            try {
                const result = JSON.parse(stdout);
                return resolve(result);
            } catch (error) {
                return reject(error);
            }
        });
    });
}

export function getBalance(rfid: string) {
    return new Promise((resolve, reject) => {
        const command = `python ${path.resolve(__dirname, '../scripts/getBalance.py')} ${rfid} json`;
        exec(command, (error, stdout, stderr) => {
            if (error) {
                log(`exec error: ${error}`);
                return reject(error)
            }
            // console.log(`stdout: ${stdout}`);
            // console.log(`stderr: ${stderr}`);
            try {
                const result = JSON.parse(stdout);
                return resolve(result);
            } catch (error) {
                return reject(error);
            }
        });
    });
}

export function shareRide(rfidFrom: string, rfidTo: string) {
    return new Promise((resolve, reject) => {
        const command = `python ${path.resolve(__dirname, '../scripts/sharePay.py')} ${rfidTo} ${rfidFrom}`;
        console.log(command)
        exec(command, (error, stdout, stderr) => {
            if (error) {
                log(`exec error: ${error}`);
                return reject(error)
            }
            console.log(`stdout: ${stdout}`);
            // console.log(`stderr: ${stderr}`);
            try {
                const result = JSON.parse(stdout);
                return resolve(result);
            } catch (error) {
                return reject(error);
            }
        });
    });
}