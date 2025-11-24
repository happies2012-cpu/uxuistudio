import { AIService } from '../AIService';
import { AgentInput, AgentOutput, DesignConfig } from '../types';
import { DESIGN_AGENT_PROMPT, substituteVariables } from '../PromptTemplates';
import logger from '../../config/logger';

export class DesignAgent {
    constructor(private aiService: AIService) { }

    async execute(input: AgentInput): Promise<AgentOutput> {
        try {
            logger.info('Design Agent: Starting design configuration');

            const prompt = substituteVariables(DESIGN_AGENT_PROMPT, {
                businessName: input.businessName,
                businessType: input.businessType,
                industry: input.industry || input.businessType
            });

            const response = await this.aiService.generateCompletion(
                prompt,
                'You are a web design expert. Always respond with valid JSON only.'
            );

            const data = await this.aiService.parseJSONResponse<DesignConfig & { confidence: number }>(response);

            logger.info('Design Agent: Successfully generated design config');

            return {
                success: true,
                confidence: data.confidence,
                data: {
                    theme: data.theme,
                    colorPalette: data.colorPalette,
                    typography: data.typography,
                    style: data.style
                }
            };

        } catch (error: any) {
            logger.error('Design Agent: Failed', error);
            return {
                success: false,
                confidence: 0,
                data: null,
                errors: [error.message]
            };
        }
    }
}
