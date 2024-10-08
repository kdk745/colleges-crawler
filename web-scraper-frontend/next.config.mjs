// next.config.mjs

export default {
    trailingSlash: true,
    async rewrites() {
        return [{
            source: '/api/:path*',
            destination: process.env.API_URL || 'http://localhost:8000/api/:path*', // Proxy to FastAPI backend
        }, ];
    },
    env: {
        API_URL: process.env.API_URL, // Ensure API_URL is available on the client
    },
};