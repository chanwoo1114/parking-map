import { API_BASE_URL } from '../config';

// 이메일, 비밀번호 로그인
export async function loginUser({ email, password }) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

// 회원가입
export async function registerUser({ email, password1, password2, nickname, age, gender }) {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password1, password2, nickname, age, gender }),
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

// 이메일 중복체크
export async function checkEmailDuplicate(email) {
    const res = await fetch(`${API_BASE_URL}/auth/check-email?email=${encodeURIComponent(email)}`);
    if (!res.ok) throw new Error('이메일 확인 실패');
    return res.json();
}

// 닉네임 중복체크
export async function checkNicknameDuplicate(nickname) {
    const res = await fetch(`${API_BASE_URL}/auth/check-nickname?nickname=${encodeURIComponent(nickname)}`);
    if (!res.ok) throw new Error('닉네임 확인 실패');
    return res.json();
}

// 소셜로그인 URL 반환
export function getSocialLoginUrl(provider) {
    return `${API_BASE_URL}/auth/social/${provider}`;
}

// 소셜로그인 콜백 후 토큰 교환 -> JWT 반환
export async function socialCallback(provider, code) {
    const res = await fetch(
        `${API_BASE_URL}/auth/social/${provider}/callback?code=${encodeURIComponent(code)}`
    );
    console.log(res)
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw err;
    }
    return res.json();
}