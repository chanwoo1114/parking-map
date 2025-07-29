import React from 'react';
import { API_BASE_URL } from '../config';

export default function SocialLoginButtons() {
    const handleLogin = (provider) => {
        window.location.href = `${API_BASE_URL}/auth/social/${provider}`;
    };

    return (
        <div className="flex gap-4">
            <button
                onClick={() => handleLogin('kakao')}
                className="px-4 py-2 bg-yellow-400 rounded text-black"
            >
                카카오 로그인
            </button>
            <button
                onClick={() => handleLogin('naver')}
                className="px-4 py-2 bg-green-500 rounded text-white"
            >
                네이버 로그인
            </button>
            <button
                onClick={() => handleLogin('google')}
                className="px-4 py-2 bg-blue-600 rounded text-white"
            >
                구글 로그인
            </button>
        </div>
    );
}
