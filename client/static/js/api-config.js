// API base: set window.SIR_KOTHAY_API_BASE before this script to override (e.g. production).
// Default local backend: http://127.0.0.1:8000
(function () {
    var host = typeof window !== 'undefined' ? window.location.hostname : '';
    var isLocal =
        host === 'localhost' ||
        host === '127.0.0.1' ||
        host === '' ||
        host === '[::1]';
    var defaultBase = isLocal ? 'http://127.0.0.1:8000' : window.location.origin;
    var raw =
        (typeof window !== 'undefined' && window.SIR_KOTHAY_API_BASE) ||
        defaultBase;
    window.SIR_KOTHAY_API_BASE = String(raw).replace(/\/$/, '');
})();

var API_BASE_URL = window.SIR_KOTHAY_API_BASE;

/** GitHub owner/repo for contributor widgets (About page, footer). */
var GITHUB_REPO = 'UIU-Developers-Hub/Sir-Kothay';

function sirKothayContributorsApiUrl() {
    return 'https://api.github.com/repos/' + GITHUB_REPO + '/contributors';
}

window.sirKothayContributorsApiUrl = sirKothayContributorsApiUrl;

// API Endpoints
var API_ENDPOINTS = {
    LOGIN: API_BASE_URL + '/api/auth/users/login/',
    REGISTER: API_BASE_URL + '/api/auth/users/register/',
    CURRENT_USER: API_BASE_URL + '/api/auth/users/me/',
    CHANGE_PASSWORD: API_BASE_URL + '/api/auth/users/change_password/',
    USER_DETAILS: API_BASE_URL + '/api/dashboard/user-details/my_details/',
    UPDATE_USER_DETAILS: API_BASE_URL + '/api/dashboard/user-details/update_my_details/',
    MY_QRCODE: API_BASE_URL + '/api/qrcode/qrcodes/my_qrcode/',
    GENERATE_QR: API_BASE_URL + '/api/qrcode/qrcodes/generate/',
    MESSAGES: API_BASE_URL + '/api/broadcast/messages/my_messages/',
    ACTIVE_MESSAGE: API_BASE_URL + '/api/broadcast/messages/active_message/',
    CREATE_MESSAGE: API_BASE_URL + '/api/broadcast/messages/',
};

function getAuthToken() {
    return localStorage.getItem('access_token');
}

async function apiRequest(url, options) {
    options = options || {};
    var token = getAuthToken();
    var defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    if (token) {
        defaultOptions.headers.Authorization = 'Bearer ' + token;
    }
    var mergedOptions = Object.assign({}, defaultOptions, options);
    mergedOptions.headers = Object.assign(
        {},
        defaultOptions.headers,
        (options && options.headers) || {}
    );
    try {
        return await fetch(url, mergedOptions);
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        API_BASE_URL: API_BASE_URL,
        API_ENDPOINTS: API_ENDPOINTS,
        getAuthToken: getAuthToken,
        apiRequest: apiRequest,
        sirKothayContributorsApiUrl: sirKothayContributorsApiUrl,
    };
}
