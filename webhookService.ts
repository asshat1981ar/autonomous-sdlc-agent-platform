// Webhook service for event-driven communication
export interface WebhookEvent {
    id: string;
    type: string;
    timestamp: string;
    data: any;
    source: string;
}

export interface WebhookSubscription {
    id: string;
    url: string;
    events: string[];
    active: boolean;
    secret?: string;
    headers?: Record<string, string>;
}

export type WebhookEventType = 
    | 'project.created'
    | 'project.updated'
    | 'ideation.completed'
    | 'plan.generated'
    | 'code.generated'
    | 'code.updated'
    | 'test.passed'
    | 'test.failed'
    | 'build.started'
    | 'build.completed'
    | 'build.failed'
    | 'deployment.started'
    | 'deployment.completed'
    | 'deployment.failed'
    | 'error.occurred';

class WebhookService {
    private subscriptions: Map<string, WebhookSubscription> = new Map();
    private eventQueue: WebhookEvent[] = [];
    private isProcessing = false;

    // Subscribe to webhook events
    subscribe(subscription: Omit<WebhookSubscription, 'id'>): string {
        const id = crypto.randomUUID();
        const fullSubscription: WebhookSubscription = {
            id,
            ...subscription,
            active: true
        };
        
        this.subscriptions.set(id, fullSubscription);
        return id;
    }

    // Unsubscribe from webhook events
    unsubscribe(subscriptionId: string): boolean {
        return this.subscriptions.delete(subscriptionId);
    }

    // Get all active subscriptions
    getSubscriptions(): WebhookSubscription[] {
        return Array.from(this.subscriptions.values()).filter(sub => sub.active);
    }

    // Emit an event to all relevant subscribers
    async emit(eventType: WebhookEventType, data: any, source = 'sdlc-agent'): Promise<void> {
        const event: WebhookEvent = {
            id: crypto.randomUUID(),
            type: eventType,
            timestamp: new Date().toISOString(),
            data,
            source
        };

        this.eventQueue.push(event);
        
        if (!this.isProcessing) {
            this.processQueue();
        }
    }

    // Process the event queue
    private async processQueue(): Promise<void> {
        this.isProcessing = true;

        while (this.eventQueue.length > 0) {
            const event = this.eventQueue.shift();
            if (!event) continue;

            const relevantSubscriptions = Array.from(this.subscriptions.values())
                .filter(sub => sub.active && sub.events.includes(event.type));

            await Promise.allSettled(
                relevantSubscriptions.map(subscription => 
                    this.deliverEvent(event, subscription)
                )
            );
        }

        this.isProcessing = false;
    }

    // Deliver event to a specific subscription
    private async deliverEvent(event: WebhookEvent, subscription: WebhookSubscription): Promise<void> {
        try {
            const headers: Record<string, string> = {
                'Content-Type': 'application/json',
                'X-Webhook-Event': event.type,
                'X-Webhook-ID': event.id,
                'X-Webhook-Timestamp': event.timestamp,
                ...subscription.headers
            };

            // Add signature if secret is provided
            if (subscription.secret) {
                const signature = await this.generateSignature(JSON.stringify(event), subscription.secret);
                headers['X-Webhook-Signature'] = signature;
            }

            const response = await fetch(subscription.url, {
                method: 'POST',
                headers,
                body: JSON.stringify(event)
            });

            if (!response.ok) {
                console.error(`Webhook delivery failed for ${subscription.id}: ${response.status} ${response.statusText}`);
            }
        } catch (error) {
            console.error(`Webhook delivery error for ${subscription.id}:`, error);
        }
    }

    // Generate HMAC signature for webhook security
    private async generateSignature(payload: string, secret: string): Promise<string> {
        const encoder = new TextEncoder();
        const key = await crypto.subtle.importKey(
            'raw',
            encoder.encode(secret),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );
        
        const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(payload));
        const hashArray = Array.from(new Uint8Array(signature));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return `sha256=${hashHex}`;
    }

    // Validate webhook signature
    async validateSignature(payload: string, signature: string, secret: string): Promise<boolean> {
        const expectedSignature = await this.generateSignature(payload, secret);
        return signature === expectedSignature;
    }

    // Get event history (for debugging/monitoring)
    getEventHistory(limit = 100): WebhookEvent[] {
        // In a real implementation, this would come from persistent storage
        return this.eventQueue.slice(-limit);
    }
}

// Export singleton instance
export const webhookService = new WebhookService();

// Helper function to emit events with type safety
export const emitWebhookEvent = (eventType: WebhookEventType, data: any, source?: string) => {
    return webhookService.emit(eventType, data, source);
};

