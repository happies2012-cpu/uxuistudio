export interface WPAuth {
    url: string;
    username: string;
    applicationPassword?: string;
    token?: string;
}

export interface WPPost {
    id?: number;
    date?: string;
    slug?: string;
    status?: 'publish' | 'future' | 'draft' | 'pending' | 'private';
    title: { rendered?: string; raw?: string } | string;
    content: { rendered?: string; raw?: string } | string;
    excerpt?: { rendered?: string; raw?: string } | string;
    author?: number;
    featured_media?: number;
    categories?: number[];
    tags?: number[];
}

export interface WPPage extends WPPost {
    parent?: number;
    menu_order?: number;
    template?: string;
}

export interface WPMedia {
    id?: number;
    source_url: string;
    mime_type: string;
    alt_text?: string;
    caption?: { rendered: string };
}

export interface SSHConfig {
    host: string;
    port?: number;
    username: string;
    privateKey?: string;
    password?: string;
    path: string; // WordPress installation path
}

export interface DeploymentStep {
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    message?: string;
}
