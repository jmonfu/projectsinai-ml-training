declare module "*.json" {
    const value: {
        subjects: Array<{ id: string; name: string }>;
        complexity: Array<{ id: string; name: string }>;
    };
    export default value;
} 