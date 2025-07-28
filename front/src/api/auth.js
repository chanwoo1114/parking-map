import { API_BASE_URL } from '../config';

export async function loginUser({ email, password }) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

export async function registerUser({ email, password1, password2, nickname, age, gender }) {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password1, password2, nickname, age, gender }),
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

export async function checkEmailDuplicate(email) {
    const res = await fetch(`${API_BASE_URL}/auth/check-email?email=${encodeURIComponent(email)}`);
    if (!res.ok) throw new Error('이메일 확인 실패');
    return res.json();
}

export async function checkNicknameDuplicate(nickname) {
    const res = await fetch(`${API_BASE_URL}/auth/check-nickname?nickname=${encodeURIComponent(nickname)}`);
    if (!res.ok) throw new Error('닉네임 확인 실패');
    return res.json();
}
