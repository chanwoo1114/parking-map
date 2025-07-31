// components/LoginForm.jsx
import React from 'react';
import PasswordInput from './PasswordInput.jsx';

export default function LoginForm({ email, setEmail, password, setPassword, onSubmit }) {
    return (
        <div className="w-full max-w-md px-8 flex flex-col">
            <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
                🚗 주차 공유 시스템
            </h1>

            <input
                type="email"
                placeholder="이메일"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full h-12 p-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 text-lg"
            />

            <PasswordInput
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="비밀번호"
                className="w-full h-12 p-4 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 text-lg"
            />

            <button
                onClick={onSubmit}
                className="w-full h-12 bg-blue-500 text-white rounded-lg hover:bg-blue-600 mb-4 font-medium text-lg"
            >
                로그인
            </button>
        </div>
    );
}
