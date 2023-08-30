export type TriliumStatus = ({
    online: true;
    appVersion: string;
    dbVersion: number;
    syncVersion: number;
    buildDate: string;
    buildRevision: string;
    dataDirectory: string;
    clipperProtocolVersion: string;
    utcDateTime: string;
} | {
    online: false
}) & {
    url: string;
}