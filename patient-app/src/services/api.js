// src/services/api.js
import axios from 'axios';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const AUTH_TOKEN_KEY = 'authToken';
const TOKEN_KEYS = ['authToken', 'access_token', 'token'];

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
    },
});

function normalizeToken(raw) {
    if (!raw || typeof raw !== 'string') return null;
    let token = raw.trim();
    if (
        (token.startsWith('"') && token.endsWith('"')) ||
        (token.startsWith("'") && token.endsWith("'"))
    ) {
        token = token.slice(1, -1).trim();
    }
    while (/^bearer\s+/i.test(token)) {
        token = token.replace(/^bearer\s+/i, '').trim();
    }
    return token || null;
}

function tokenFromUserData() {
    try {
        const user = JSON.parse(localStorage.getItem('userData') || sessionStorage.getItem('userData') || 'null');
        return normalizeToken(user?.access_token || user?.token || user?.authToken);
    } catch {
        return null;
    }
}

export function readAuthToken() {
    for (const store of [localStorage, sessionStorage]) {
        for (const key of TOKEN_KEYS) {
            const token = normalizeToken(store.getItem(key));
            if (token) return token;
        }
    }
    return tokenFromUserData();
}

export function setAuthToken(token) {
    const normalized = normalizeToken(token);
    if (!normalized) return null;
    localStorage.setItem(AUTH_TOKEN_KEY, normalized);
    api.defaults.headers.common.Authorization = `Bearer ${normalized}`;
    return normalized;
}

export function clearAuthToken() {
    TOKEN_KEYS.forEach((key) => {
        localStorage.removeItem(key);
        sessionStorage.removeItem(key);
    });
    delete api.defaults.headers.common.Authorization;
}

const existing = readAuthToken();
if (existing) setAuthToken(existing);

export const register = (payload) => api.post('/auth/register', payload);
export const login = (payload) => api.post('/auth/login', payload);
export const getMe = () => api.get('/auth/me');
export const getPatientProfile = () => api.get('/patient/profile');
export const updatePatientProfile = (payload) => api.put('/patients/profile', payload);

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

export const getReminders = () => api.get('/reminders/');
export const getReminder = (reminderId) => api.get(`/reminders/${reminderId}`);
export const createReminder = (payload) => api.post('/reminders/', payload);
export const updateReminder = (reminderId, payload) => api.put(`/reminders/${reminderId}`, payload);
export const deleteReminder = (reminderId) => api.delete(`/reminders/${reminderId}`);
export const recordReminderEvent = (payload) => api.post('/reminders/event', payload);
export const getReminderHistory = () => api.get('/reminders/history');
export const getReminderAdherence = () => api.get('/reminders/adherence');

export const getPatientAlerts = () => api.get('/alerts/patient');
export const createAlert = (payload) => api.post('/alerts/', payload);
export const resolveAlert = (alertId) => api.put(`/alerts/${alertId}/resolve`);

export const getNotifications = () => api.get('/notifications/');
export const getUnreadNotifications = () => api.get('/notifications/unread');
export const markNotificationRead = (notificationId) => api.put(`/notifications/${notificationId}/read`);
export const markAllNotificationsRead = () => api.put('/notifications/read-all');

export const saveLocation = (payload) => api.post('/location/', payload);
export const getVoiceRecordings = () => api.get('/voice-recordings/');
export const createVoiceRecording = (payload) => api.post('/voice-recordings/', payload);
export const getVoiceRecording = (recordingId) => api.get(`/voice-recordings/${recordingId}`);

export const uploadAudio = (file, extra = {}) => {
    const form = new FormData();
    form.append('file', file);
    Object.entries(extra).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') form.append(key, value);
    });
    return api.post('/audio/upload', form);
};
export const processAIVoice = (payload) =>
    api.post('/ai-voice/process', payload);

export const getGames = () => api.get('/games/');
export const startGame = (payload) => api.post('/games/start', payload);
export const submitGameResult = (payload) => api.post('/games/result', payload);
export const getGamePerformance = (patientId) => api.get(`/games/performance/${patientId}`);

api.interceptors.request.use(
    (config) => {
        const token = readAuthToken();
        if (token) {
            const headerValue = `Bearer ${token}`;
            if (typeof config.headers?.set === 'function') {
                config.headers.set('Authorization', headerValue, true);
            } else {
                config.headers = config.headers || {};
                config.headers.Authorization = headerValue;
            }
        }
        if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
            if (typeof config.headers?.set === 'function') {
                config.headers.set('Content-Type', false);
            } else if (config.headers) {
                delete config.headers['Content-Type'];
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

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
            clearAuthToken();
            localStorage.removeItem('userData');
            sessionStorage.removeItem('userData');
            window.dispatchEvent(new CustomEvent('xathi-auth-expired', { detail: { role } }));
        }
        return Promise.reject(error);
    }
);

export default api;
