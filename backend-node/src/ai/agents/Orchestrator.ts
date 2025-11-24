import { EventEmitter } from 'events';
import { AIService } from '../AIService';
import { PlanningAgent } from './PlanningAgent';
import { ContentAgent } from './ContentAgent';
import { DesignAgent } from './DesignAgent';
import { AgentInput } from '../types';
import logger from '../../config/logger';

export interface OrchestrationResult {
    success: boolean;
    siteArchitecture?: any;
    content?: any;
    design?: any;
    overallConfidence: number;
    errors: string[];
}

export class Orchestrator extends EventEmitter {
    private planningAgent: PlanningAgent;
    private contentAgent: ContentAgent;
    private designAgent: DesignAgent;

    constructor(private aiService: AIService) {
        super();
        this.planningAgent = new PlanningAgent(aiService);
        this.contentAgent = new ContentAgent(aiService);
        this.designAgent = new DesignAgent(aiService);
    }

    async orchestrate(input: AgentInput): Promise<OrchestrationResult> {
        const errors: string[] = [];
        let overallConfidence = 0;
        const confidences: number[] = [];

        try {
            // Step 1: Planning Agent
            this.emit('progress', { step: 'planning', progress: 10, message: 'Analyzing business and creating site architecture...' });
            const planningResult = await this.planningAgent.execute(input);

            if (!planningResult.success) {
                errors.push(...(planningResult.errors || ['Planning failed']));
                return { success: false, overallConfidence: 0, errors };
            }

            confidences.push(planningResult.confidence);
            logger.info('Orchestrator: Planning complete', { confidence: planningResult.confidence });

            // Step 2: Design Agent (parallel with content)
            this.emit('progress', { step: 'design', progress: 30, message: 'Selecting theme and design system...' });
            const designResult = await this.designAgent.execute(input);

            if (!designResult.success) {
                errors.push(...(designResult.errors || ['Design selection failed']));
            } else {
                confidences.push(designResult.confidence);
            }

            // Step 3: Content Agent
            this.emit('progress', { step: 'content', progress: 50, message: 'Generating page content and SEO metadata...' });
            const contentResult = await this.contentAgent.execute(input, planningResult.data.pages);

            if (!contentResult.success) {
                errors.push(...(contentResult.errors || ['Content generation failed']));
            } else {
                confidences.push(contentResult.confidence);
            }

            // Calculate overall confidence
            overallConfidence = confidences.reduce((a, b) => a + b, 0) / confidences.length;

            this.emit('progress', { step: 'complete', progress: 100, message: 'Site generation complete!' });

            logger.info('Orchestrator: Complete', { overallConfidence, errors });

            return {
                success: errors.length === 0,
                siteArchitecture: planningResult.data,
                content: contentResult.success ? contentResult.data : null,
                design: designResult.success ? designResult.data : null,
                overallConfidence,
                errors
            };

        } catch (error: any) {
            logger.error('Orchestrator: Fatal error', error);
            return {
                success: false,
                overallConfidence: 0,
                errors: [error.message]
            };
        }
    }
}
