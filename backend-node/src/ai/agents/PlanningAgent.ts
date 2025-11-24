import { AIService } from '../AIService';
import { AgentInput, AgentOutput, SiteArchitecture } from '../types';
import { PLANNING_AGENT_PROMPT, substituteVariables } from '../PromptTemplates';
import logger from '../../config/logger';

export class PlanningAgent {
    constructor(private aiService: AIService) { }

    async execute(input: AgentInput): Promise<AgentOutput> {
        try {
            logger.info('Planning Agent: Starting site architecture generation');

            const prompt = substituteVariables(PLANNING_AGENT_PROMPT, {
                businessName: input.businessName,
                businessType: input.businessType,
                description: input.description
            });

            const response = await this.aiService.generateCompletion(
                prompt,
                'You are a website planning expert. Always respond with valid JSON only.'
            );

            const data = await this.aiService.parseJSONResponse<SiteArchitecture & { confidence: number; assumptions?: string[] }>(response);

            // Validate confidence threshold
            if (data.confidence < 0.75) {
                logger.warn('Planning Agent: Low confidence', { confidence: data.confidence });
            }

            logger.info('Planning Agent: Successfully generated site architecture');

            return {
                success: true,
                confidence: data.confidence,
                data: {
                    pages: data.pages,
                    features: data.features,
                    navigation: data.navigation,
                    siteMap: data.siteMap
                },
                assumptions: data.assumptions
            };

        } catch (error: any) {
            logger.error('Planning Agent: Failed', error);
            return {
                success: false,
                confidence: 0,
                data: null,
                errors: [error.message]
            };
        }
    }
}
