import { Client } from 'ssh2';
import { SSHConfig } from './types';
import { SSHError } from './errors';
import logger from '../../config/logger';

export class SSHClient {
    private conn: Client;

    constructor(private config: SSHConfig) {
        this.conn = new Client();
    }

    private connect(): Promise<void> {
        return new Promise((resolve, reject) => {
            this.conn
                .on('ready', resolve)
                .on('error', reject)
                .connect({
                    host: this.config.host,
                    port: this.config.port || 22,
                    username: this.config.username,
                    privateKey: this.config.privateKey,
                    password: this.config.password,
                });
        });
    }

    private disconnect() {
        this.conn.end();
    }

    async executeCommand(command: string): Promise<string> {
        try {
            await this.connect();

            return new Promise((resolve, reject) => {
                // Execute command in the WP directory
                const fullCommand = `cd ${this.config.path} && ${command}`;
                logger.info(`Executing SSH: ${fullCommand}`);

                this.conn.exec(fullCommand, (err, stream) => {
                    if (err) {
                        this.disconnect();
                        return reject(new SSHError(err.message, command));
                    }

                    let output = '';
                    let errorOutput = '';

                    stream
                        .on('close', (code: number, signal: any) => {
                            this.disconnect();
                            if (code !== 0) {
                                reject(new SSHError(`Command failed with code ${code}: ${errorOutput}`, command));
                            } else {
                                resolve(output.trim());
                            }
                        })
                        .on('data', (data: any) => {
                            output += data;
                        })
                        .stderr.on('data', (data: any) => {
                            errorOutput += data;
                        });
                });
            });
        } catch (error: any) {
            this.disconnect();
            throw new SSHError(error.message, command);
        }
    }

    // --- WP-CLI Wrappers ---

    async wpCoreInstall(url: string, title: string, adminUser: string, adminPass: string, adminEmail: string) {
        return this.executeCommand(
            `wp core install --url="${url}" --title="${title}" --admin_user="${adminUser}" --admin_password="${adminPass}" --admin_email="${adminEmail}"`
        );
    }

    async wpPluginInstall(plugin: string, activate = true) {
        return this.executeCommand(`wp plugin install ${plugin} ${activate ? '--activate' : ''}`);
    }

    async wpThemeInstall(theme: string, activate = true) {
        return this.executeCommand(`wp theme install ${theme} ${activate ? '--activate' : ''}`);
    }

    async wpUserCreate(user: string, email: string, role = 'subscriber') {
        return this.executeCommand(`wp user create ${user} ${email} --role=${role} --porcelain`);
    }
}
