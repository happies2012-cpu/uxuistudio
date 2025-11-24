import axios, { AxiosInstance } from 'axios';
import { WPAuth, WPPost, WPPage, WPMedia } from './types';
import { WPError, WPAuthError, WPNetworkError } from './errors';
import logger from '../../config/logger';

export class WordPressAPIClient {
    private client: AxiosInstance;

    constructor(private config: WPAuth) {
        const baseURL = config.url.endsWith('/') ? config.url : `${config.url}/`;

        this.client = axios.create({
            baseURL: `${baseURL}wp-json/wp/v2/`,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Add Auth Header
        if (config.applicationPassword) {
            const token = Buffer.from(`${config.username}:${config.applicationPassword}`).toString('base64');
            this.client.defaults.headers.common['Authorization'] = `Basic ${token}`;
        } else if (config.token) {
            this.client.defaults.headers.common['Authorization'] = `Bearer ${config.token}`;
        }

        // Interceptors for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response) {
                    if (error.response.status === 401) {
                        throw new WPAuthError();
                    }
                    throw new WPError(
                        error.response.data?.message || 'WordPress API Error',
                        error.response.status,
                        error.response.data?.code
                    );
                } else if (error.request) {
                    throw new WPNetworkError(error.message);
                }
                throw error;
            }
        );
    }

    async validateConnection(): Promise<boolean> {
        try {
            await this.client.get('users/me');
            return true;
        } catch (error) {
            logger.error('WP Connection Validation Failed', error);
            return false;
        }
    }

    // --- Posts ---
    async createPost(post: WPPost): Promise<WPPost> {
        const { data } = await this.client.post('posts', post);
        return data;
    }

    async updatePost(id: number, post: Partial<WPPost>): Promise<WPPost> {
        const { data } = await this.client.post(`posts/${id}`, post);
        return data;
    }

    async deletePost(id: number): Promise<void> {
        await this.client.delete(`posts/${id}?force=true`);
    }

    // --- Pages ---
    async createPage(page: WPPage): Promise<WPPage> {
        const { data } = await this.client.post('pages', page);
        return data;
    }

    // --- Media ---
    async uploadMedia(fileBuffer: Buffer, fileName: string, mimeType: string): Promise<WPMedia> {
        const { data } = await this.client.post('media', fileBuffer, {
            headers: {
                'Content-Type': mimeType,
                'Content-Disposition': `attachment; filename="${fileName}"`,
            },
        });
        return data;
    }

    // --- Settings ---
    async updateSettings(settings: Record<string, any>): Promise<any> {
        const { data } = await this.client.post('settings', settings);
        return data;
    }
}
