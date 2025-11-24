import Anthropic from '@anthropic-ai/sdk';
import { AIProviderConfig } from './types';
import logger from '../config/logger';

export class AIService {
    private anthropic: Anthropic | null = null;
    private config: AIProviderConfig;

    constructor(config: AIProviderConfig) {
        this.config = config;

        if (config.provider === 'anthropic' && config.apiKey) {
            this.anthropic = new Anthropic({ apiKey: config.apiKey });
        }
    }

    async generateCompletion(prompt: string, systemPrompt?: string): Promise<string> {
        try {
            if (this.config.provider === 'anthropic' && this.anthropic) {
                return await this.generateWithAnthropic(prompt, systemPrompt);
            }

            // Fallback to mock if no provider configured
            logger.warn('No AI provider configured, using mock response');
            return this.mockResponse(prompt);
        } catch (error: any) {
            logger.error('AI generation failed', error);
            throw new Error(`AI generation failed: ${error.message}`);
        }
    }

    private async generateWithAnthropic(prompt: string, systemPrompt?: string): Promise<string> {
        const message = await this.anthropic!.messages.create({
            model: this.config.model || 'claude-3-5-sonnet-20241022',
            max_tokens: this.config.maxTokens || 2000,
            temperature: this.config.temperature || 0.7,
            system: systemPrompt,
            messages: [
                {
                    role: 'user',
                    content: prompt
                }
            ]
        });

        const content = message.content[0];
        if (content.type === 'text') {
            return content.text;
        }

        throw new Error('Unexpected response format from Anthropic');
    }

    private mockResponse(prompt: string): string {
        // Mock response for development/testing
        if (prompt.includes('planning')) {
            return JSON.stringify({
                pages: [
                    { title: 'Home', slug: 'home', template: 'homepage', sections: ['hero', 'services', 'cta'], priority: 1 },
                    { title: 'About', slug: 'about', template: 'standard', sections: ['story', 'team'], priority: 2 },
                    { title: 'Services', slug: 'services', template: 'services', sections: ['list', 'pricing'], priority: 3 },
                    { title: 'Contact', slug: 'contact', template: 'contact', sections: ['form', 'map'], priority: 4 }
                ],
                features: ['Contact Form', 'SEO', 'Mobile Responsive'],
                navigation: [
                    { label: 'Home', url: '/' },
                    { label: 'About', url: '/about' },
                    { label: 'Services', url: '/services' },
                    { label: 'Contact', url: '/contact' }
                ],
                siteMap: ['/', '/about', '/services', '/contact'],
                confidence: 0.85,
                assumptions: ['Standard business website structure']
            });
        }

        return JSON.stringify({ confidence: 0.8, data: 'Mock response' });
    }

    async parseJSONResponse<T>(response: string): Promise<T> {
        try {
            // Extract JSON from markdown code blocks if present
            const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/) ||
                response.match(/```\n([\s\S]*?)\n```/);

            const jsonString = jsonMatch ? jsonMatch[1] : response;
            return JSON.parse(jsonString.trim());
        } catch (error) {
            logger.error('Failed to parse JSON response', { response, error });
            throw new Error('Invalid JSON response from AI');
        }
    }
}
