import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const dashboardService = {
    login: async (username: string, password: string) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        const response = await axios.post(`${API_BASE}/auth/login`, formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        return response.data;
    },
    getGraphData: async (token: string) => {
        const response = await axios.get(`${API_BASE}/investigation/graph`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return response.data;
    },
    getStats: async () => {
        const response = await axios.get(`${API_BASE}/stats`);
        return response.data;
    },
    uploadDataset: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(`${API_BASE}/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },
    getHistory: async () => {
        const response = await axios.get(`${API_BASE}/history`);
        return response.data;
    },
    getBlockchainLogs: async () => {
        const response = await axios.get(`${API_BASE}/blockchain/logs`);
        return response.data;
    },
    getInvestigationData: async () => {
        const response = await axios.get(`${API_BASE}/investigation/flagged-accounts?sort=desc`);
        return response.data;
    },
    revealIdentity: async (accountHash: string, token: string) => {
        const response = await axios.get(`${API_BASE}/investigation/reveal/${accountHash}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return response.data;
    },
    getRecentDetections: async () => {
        const response = await axios.get(`${API_BASE}/investigation/flagged-accounts?limit=5&sort=desc`);
        return response.data;
    },
    reset: async () => {
        const response = await axios.post(`${API_BASE}/reset`);
        return response.data;
    }
};
