import { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
      <div className="flex w-full h-screen">
        {/* 왼쪽: 70% 이미지 영역 */}
        <div className="basis-[70%] bg-login h-full" />

        {/* 오른쪽: 30% 로그인 영역 */}
        <div className="basis-[30%] bg-white flex items-center justify-center">
          <div className="w-full max-w-sm p-8 flex flex-col">
            <h1 className="text-2xl font-bold text-center mb-6">🚗 주차 공유 시스템</h1>

            <input
                type="email"
                placeholder="이메일"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2 mb-4 border rounded"
            />
            <input
                type="password"
                placeholder="비밀번호"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-2 mb-6 border rounded"
            />

            <button className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 mb-4">
              로그인
            </button>
            <button className="w-full bg-gray-600 text-white py-2 rounded hover:bg-gray-700 mb-6">
              회원가입
            </button>

            <div className="text-center text-sm text-gray-500 mb-2">
              또는 소셜 계정으로 로그인
            </div>

            <div className="flex flex-col gap-2">
              <button className="bg-yellow-400 py-2 rounded hover:brightness-110">
                카카오 로그인
              </button>
              <button className="bg-white border py-2 rounded hover:bg-gray-100">
                구글 로그인
              </button>
            </div>
          </div>
        </div>
      </div>
  );
}
