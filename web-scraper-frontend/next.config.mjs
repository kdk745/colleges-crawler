// next.config.mjs

export default {
    async rewrites() {
        return [{
            source: '/api/:path*',
            destination: process.env.API_URL || 'http://localhost:8000/api/:path*', // Proxy to FastAPI backend
        }, ];
    },
};