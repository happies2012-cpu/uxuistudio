export class WPError extends Error {
    constructor(public message: string, public statusCode?: number, public code?: string) {
        super(message);
        this.name = 'WPError';
    }
}

export class WPAuthError extends WPError {
    constructor(message = 'WordPress Authentication Failed') {
        super(message, 401, 'WP_AUTH_FAILED');
    }
}

export class WPNetworkError extends WPError {
    constructor(message: string) {
        super(message, 503, 'WP_NETWORK_ERROR');
    }
}

export class SSHError extends Error {
    constructor(public message: string, public command?: string) {
        super(message);
        this.name = 'SSHError';
    }
}
