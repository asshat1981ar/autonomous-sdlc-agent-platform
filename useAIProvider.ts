import { useState, useEffect, useCallback } from 'react';
import { AIProvider, AIProviderFactory, AIGenerationConfig, AIResponse } from '../services/aiProviderInterface';

interface UseAIProviderReturn {
    currentProvider: AIProvider | null;
    currentProviderName: string | null;
    availableProviders: string[];
    allProviders: string[];
    isLoading: boolean;
    error: string | null;
    switchProvider: (providerName: string) => Promise<boolean>;
    generateContent: (config: AIGenerationConfig) => Promise<AIResponse>;
    testProvider: (providerName: string) => Promise<boolean>;
    refreshProviders: () => void;
}

export const useAIProvider = (initialProvider?: string): UseAIProviderReturn => {
    const [currentProvider, setCurrentProvider] = useState<AIProvider | null>(null);
    const [currentProviderName, setCurrentProviderName] = useState<string | null>(null);
    const [availableProviders, setAvailableProviders] = useState<string[]>([]);
    const [allProviders, setAllProviders] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Initialize providers and set default
    useEffect(() => {
        initializeProviders();
    }, []);

    // Set initial provider
    useEffect(() => {
        if (initialProvider && availableProviders.includes(initialProvider)) {
            switchProvider(initialProvider);
        } else if (availableProviders.length > 0 && !currentProvider) {
            const defaultProvider = AIProviderFactory.getDefaultProvider();
            if (defaultProvider) {
                setCurrentProvider(defaultProvider);
                setCurrentProviderName(defaultProvider.name);
            }
        }
    }, [initialProvider, availableProviders, currentProvider]);

    const initializeProviders = useCallback(() => {
        try {
            AIProviderFactory.initialize();
            
            // Wait a bit for async imports to complete
            setTimeout(() => {
                const available = AIProviderFactory.getAvailableProviders();
                const all = AIProviderFactory.getAllProviders();
                
                setAvailableProviders(available);
                setAllProviders(all);
                
                // Set default provider if none is set
                if (!currentProvider && available.length > 0) {
                    const defaultProvider = AIProviderFactory.getDefaultProvider();
                    if (defaultProvider) {
                        setCurrentProvider(defaultProvider);
                        setCurrentProviderName(defaultProvider.name);
                    }
                }
            }, 100);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to initialize AI providers');
        }
    }, [currentProvider]);

    const switchProvider = useCallback(async (providerName: string): Promise<boolean> => {
        setIsLoading(true);
        setError(null);
        
        try {
            const provider = await AIProviderFactory.switchProvider(providerName);
            if (provider) {
                setCurrentProvider(provider);
                setCurrentProviderName(providerName);
                return true;
            }
            return false;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to switch provider';
            setError(errorMessage);
            return false;
        } finally {
            setIsLoading(false);
        }
    }, []);

    const generateContent = useCallback(async (config: AIGenerationConfig): Promise<AIResponse> => {
        if (!currentProvider) {
            throw new Error('No AI provider selected');
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await currentProvider.generateContent(config);
            return response;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to generate content';
            setError(errorMessage);
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, [currentProvider]);

    const testProvider = useCallback(async (providerName: string): Promise<boolean> => {
        try {
            const provider = AIProviderFactory.getProvider(providerName);
            if (!provider || !provider.isConfigured()) {
                return false;
            }

            // Test with a simple prompt
            const testConfig: AIGenerationConfig = {
                prompt: 'Hello, please respond with "Test successful" to confirm you are working.',
                temperature: 0.1,
                maxTokens: 50
            };

            const response = await provider.generateContent(testConfig);
            return response.text.toLowerCase().includes('test successful') || 
                   response.text.toLowerCase().includes('hello') ||
                   response.text.trim().length > 0;
        } catch (err) {
            console.error(`Provider test failed for ${providerName}:`, err);
            return false;
        }
    }, []);

    const refreshProviders = useCallback(() => {
        initializeProviders();
    }, [initializeProviders]);

    return {
        currentProvider,
        currentProviderName,
        availableProviders,
        allProviders,
        isLoading,
        error,
        switchProvider,
        generateContent,
        testProvider,
        refreshProviders
    };
};

// Hook for specific provider capabilities
export const useProviderCapabilities = (providerName?: string) => {
    const [capabilities, setCapabilities] = useState<string[]>([]);

    useEffect(() => {
        if (providerName) {
            const caps = AIProviderFactory.getProviderCapabilities(providerName);
            setCapabilities(caps);
        } else {
            setCapabilities([]);
        }
    }, [providerName]);

    return capabilities;
};

// Hook for provider-specific methods (like Blackbox code generation)
export const useProviderMethods = (providerName?: string) => {
    const [provider, setProvider] = useState<any>(null);

    useEffect(() => {
        if (providerName) {
            const p = AIProviderFactory.getProvider(providerName);
            setProvider(p);
        } else {
            setProvider(null);
        }
    }, [providerName]);

    const generateCode = useCallback(async (language: string, description: string, context?: string): Promise<string> => {
        if (provider && 'generateCode' in provider) {
            return await provider.generateCode(language, description, context);
        }
        throw new Error('Code generation not supported by current provider');
    }, [provider]);

    const explainCode = useCallback(async (code: string, language?: string): Promise<string> => {
        if (provider && 'explainCode' in provider) {
            return await provider.explainCode(code, language);
        }
        throw new Error('Code explanation not supported by current provider');
    }, [provider]);

    const analyzeCodeQuality = useCallback(async (code: string, language: string): Promise<string> => {
        if (provider && 'analyzeCodeQuality' in provider) {
            return await provider.analyzeCodeQuality(code, language);
        }
        throw new Error('Code quality analysis not supported by current provider');
    }, [provider]);

    const generateTests = useCallback(async (code: string, language: string, testFramework?: string): Promise<string> => {
        if (provider && 'generateTests' in provider) {
            return await provider.generateTests(code, language, testFramework);
        }
        throw new Error('Test generation not supported by current provider');
    }, [provider]);

    const optimizeCode = useCallback(async (code: string, language: string, goals?: string[]): Promise<string> => {
        if (provider && 'optimizeCode' in provider) {
            return await provider.optimizeCode(code, language, goals);
        }
        throw new Error('Code optimization not supported by current provider');
    }, [provider]);

    const debugCode = useCallback(async (code: string, error: string, language: string): Promise<string> => {
        if (provider && 'debugCode' in provider) {
            return await provider.debugCode(code, error, language);
        }
        throw new Error('Code debugging not supported by current provider');
    }, [provider]);

    return {
        generateCode,
        explainCode,
        analyzeCodeQuality,
        generateTests,
        optimizeCode,
        debugCode,
        hasCodeGeneration: provider && 'generateCode' in provider,
        hasCodeAnalysis: provider && 'analyzeCodeQuality' in provider,
        hasTestGeneration: provider && 'generateTests' in provider
    };
};

