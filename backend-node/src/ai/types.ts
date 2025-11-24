export interface AgentInput {
    businessName: string;
    businessType: string;
    description: string;
    industry?: string;
    targetAudience?: string;
}

export interface AgentOutput {
    success: boolean;
    confidence: number;
    data: any;
    assumptions?: string[];
    errors?: string[];
}

export interface SiteArchitecture {
    pages: PageStructure[];
    features: string[];
    navigation: NavigationItem[];
    siteMap: string[];
}

export interface PageStructure {
    title: string;
    slug: string;
    template: string;
    sections: string[];
    priority: number;
}

export interface NavigationItem {
    label: string;
    url: string;
    children?: NavigationItem[];
}

export interface DesignConfig {
    theme: string;
    colorPalette: {
        primary: string;
        secondary: string;
        accent: string;
        background: string;
        text: string;
    };
    typography: {
        headingFont: string;
        bodyFont: string;
    };
    style: 'modern' | 'classic' | 'bold' | 'minimal';
}

export interface PluginConfig {
    slug: string;
    name: string;
    required: boolean;
    settings?: Record<string, any>;
}

export interface ContentOutput {
    pages: PageContent[];
    posts: PostContent[];
}

export interface PageContent {
    title: string;
    slug: string;
    content: string;
    seoTitle: string;
    seoDescription: string;
    focusKeyword: string;
}

export interface PostContent {
    title: string;
    slug: string;
    content: string;
    excerpt: string;
    categories: string[];
    tags: string[];
}

export interface DeploymentPlan {
    steps: DeploymentStep[];
    estimatedTime: number;
    prerequisites: string[];
}

export interface DeploymentStep {
    name: string;
    description: string;
    order: number;
    critical: boolean;
}

export interface AIProviderConfig {
    provider: 'anthropic' | 'openai';
    apiKey: string;
    model: string;
    maxTokens: number;
    temperature: number;
}
