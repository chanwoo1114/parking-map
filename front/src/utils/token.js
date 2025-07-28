export function saveTokens({ access_token, refresh_token }) {
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
}

export function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

export function getAccessToken() {
    return localStorage.getItem('access_token');
}
