import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/auth';
import { saveTokens } from "../utils/token";
import RegisterModal from '../components/RegisterModal';
import PasswordInput from '../components/PasswordInput';
import SocialLoginButtons from "../components/SocialLoginButtons";

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const data = await loginUser({ email, password });
            saveTokens(data);
            navigate('/map');
        } catch (err) {
            alert(err.detail || '로그인 실패');
        }
    };

    return (
        <>
            <div className="flex flex-row w-screen h-screen overflow-hidden">

                <div className="flex-none w-[70%] bg-login h-screen" />

                <div className="flex-none w-[30%] bg-white h-screen flex items-center justify-center">
                    <div className="w-full max-w-sm px-8 flex flex-col">
                        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">🚗 주차 공유 시스템</h1>

                        <input
                            type="email"
                            placeholder="이메일"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                        />

                        <PasswordInput
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="비밀번호"
                        />

                        <button
                            className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 mb-4 font-medium"
                            onClick={handleLogin}
                        >
                            로그인
                        </button>

                        <div className="text-center text-sm text-gray-500 mt-8 mb-4 flex items-center justify-center">
                            <div className="flex-grow h-px bg-gray-200"></div>
                            <span className="px-4 text-gray-400">간편 로그인</span>
                            <div className="flex-grow h-px bg-gray-200"></div>
                        </div>

                        <div className="flex justify-center gap-4">
                          <button className="…"><img src="/kakao-icon.png"/></button>
                          <button className="…"><img src="/google-icon.png"/></button>
                          <button className="…"><img src="/naver-icon.png"/></button>
                        </div>

                        <SocialLoginButtons />

                        <div className="text-center text-sm text-gray-600 mt-6">
                            계정이 없으신가요?{' '}
                            <button
                                className="text-blue-600 hover:underline font-semibold px-0 py-0 bg-none border-none shadow-none"
                                style={{ background: 'none', border: 'none' }}
                                onClick={() => setShowModal(true)}
                                type="button"
                            >
                                회원가입
                            </button>
                        </div>

                    </div>
                </div>
            </div>
            {showModal && <RegisterModal onClose={() => setShowModal(false)} />}
        </>
    );
}
