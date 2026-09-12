// src/services/api.js
import axios from 'axios';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const AUTH_TOKEN_KEY = 'authToken';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const register = (payload) => api.post('/auth/register', payload);
export const login = (payload) => api.post('/auth/login', payload);
export const getMe = () => api.get('/auth/me');

export function apiErrorMessage(error, fallback = 'The server could not complete your request.') {
    const detail = error?.response?.data?.detail;
    if (typeof detail === 'string' && detail.trim()) return detail;
    if (Array.isArray(detail)) {
        const messages = detail
            .map((item) => (typeof item === 'string' ? item : item?.msg || item?.message))
            .filter(Boolean);
        if (messages.length) return messages.join(' ');
    }
    if (error?.code === 'ERR_NETWORK' || error?.message === 'Network Error') {
        return 'Cannot reach the server. Please check that the backend is running.';
    }
    if (typeof error?.message === 'string' && error.message.trim()) return error.message;
    return fallback;
}

const isAuthCredentialRequest = (url = '') =>
    url.includes('/auth/login') || url.includes('/auth/register');

export const getFamilyMembers = () => api.get('/family/');
export const createFamilyMember = (payload) => api.post('/family/', payload);
export const updateFamilyMember = (familyMemberId, payload) => api.put(`/family/${familyMemberId}`, payload);
export const deleteFamilyMember = (familyMemberId) => api.delete(`/family/${familyMemberId}`);

export const getMemories = () => api.get('/memories/');
export const getMemory = (memoryId) => api.get(`/memories/${memoryId}`);
export const createMemory = (payload) => api.post('/memories/', payload);
export const updateMemory = (memoryId, payload) => api.put(`/memories/${memoryId}`, payload);
export const deleteMemory = (memoryId) => api.delete(`/memories/${memoryId}`);

// Request interceptor to add token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(AUTH_TOKEN_KEY);
        if (token) {
            if (typeof config.headers?.set === 'function') {
                config.headers.set('Authorization', `Bearer ${token}`);
            } else {
                config.headers = config.headers || {};
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && !isAuthCredentialRequest(error.config?.url)) {
            let role = 'patient';
            try {
                role = JSON.parse(localStorage.getItem('userData') || 'null')?.role || role;
            } catch {
                /* keep default role */
            }
            localStorage.removeItem(AUTH_TOKEN_KEY);
            localStorage.removeItem('userData');
            window.dispatchEvent(new CustomEvent('xathi-auth-expired', { detail: { role } }));
        }
        return Promise.reject(error);
    }
);

export default api;