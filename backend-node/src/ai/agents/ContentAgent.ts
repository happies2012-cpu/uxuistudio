import { AIService } from '../AIService';
import { AgentInput, AgentOutput, ContentOutput, PageStructure } from '../types';
import { CONTENT_AGENT_PROMPT, substituteVariables } from '../PromptTemplates';
import logger from '../../config/logger';

export class ContentAgent {
    constructor(private aiService: AIService) { }

    async execute(input: AgentInput, pages: PageStructure[]): Promise<AgentOutput> {
        try {
            logger.info('Content Agent: Starting content generation');

            const prompt = substituteVariables(CONTENT_AGENT_PROMPT, {
                businessName: input.businessName,
                businessType: input.businessType,
                pages: JSON.stringify(pages.map(p => ({ title: p.title, slug: p.slug })))
            });

            const response = await this.aiService.generateCompletion(
                prompt,
                'You are an expert content writer. Always respond with valid JSON only.'
            );

            const data = await this.aiService.parseJSONResponse<ContentOutput & { confidence: number }>(response);

            logger.info('Content Agent: Successfully generated content');

            return {
                success: true,
                confidence: data.confidence,
                data: {
                    pages: data.pages,
                    posts: data.posts || []
                }
            };

        } catch (error: any) {
            logger.error('Content Agent: Failed', error);
            return {
                success: false,
                confidence: 0,
                data: null,
                errors: [error.message]
            };
        }
    }
}
