import { EventEmitter } from 'events';
import { WordPressAPIClient } from './api-client';
import { SSHClient } from './ssh-client';
import { SSHConfig, WPAuth } from './types';
import logger from '../../config/logger';
import prisma from '../../config/prisma';

export class WordPressService extends EventEmitter {
    private sshClient: SSHClient;
    private apiClient: WordPressAPIClient | null = null;

    constructor(private sshConfig: SSHConfig, private wpAuth?: WPAuth) {
        super();
        this.sshClient = new SSHClient(sshConfig);
        if (wpAuth) {
            this.apiClient = new WordPressAPIClient(wpAuth);
        }
    }

    async deploySite(siteId: string, deploymentData: any) {
        logger.info(`Starting deployment for site ${siteId}`);
        this.emit('progress', { step: 'init', message: 'Initializing deployment...' });

        try {
            // 1. Install Core
            this.emit('progress', { step: 'core_install', message: 'Installing WordPress Core...' });
            await this.sshClient.wpCoreInstall(
                deploymentData.url,
                deploymentData.title,
                deploymentData.adminUser,
                deploymentData.adminPass,
                deploymentData.adminEmail
            );

            // 2. Install Theme
            if (deploymentData.theme) {
                this.emit('progress', { step: 'theme_install', message: `Installing theme: ${deploymentData.theme}` });
                await this.sshClient.wpThemeInstall(deploymentData.theme);
            }

            // 3. Install Plugins
            if (deploymentData.plugins && deploymentData.plugins.length > 0) {
                this.emit('progress', { step: 'plugins_install', message: 'Installing plugins...' });
                for (const plugin of deploymentData.plugins) {
                    await this.sshClient.wpPluginInstall(plugin);
                }
            }

            // 4. Create Initial Content (via REST API if available, else CLI)
            // We need to initialize the API client now that WP is installed
            if (!this.apiClient) {
                // In a real scenario, we'd need to get the application password here
                // For now, we assume we can use the admin credentials or SSH
            }

            // Update DB status
            await prisma.site.update({
                where: { id: siteId },
                data: { status: 'DEPLOYED' }
            });

            this.emit('progress', { step: 'completed', message: 'Deployment successful!' });
            logger.info(`Deployment completed for site ${siteId}`);

        } catch (error: any) {
            logger.error(`Deployment failed for site ${siteId}`, error);
            this.emit('progress', { step: 'failed', message: error.message });

            await prisma.site.update({
                where: { id: siteId },
                data: { status: 'FAILED' }
            });

            throw error;
        }
    }
}
