// pages/LoginPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageLayout from '../components/login/PageLayout.jsx';
import LoginForm from '../components/login/LoginForm.jsx';
import SocialLoginButtons from '../components/login/SocialLoginButtons.jsx';
import RegisterModal from '../components/login/RegisterModal.jsx';
import useAuth from '../hooks/auth/useAuth';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleLogin = () => {
        login({ email, password })
            .then(() => navigate('/map'))
            .catch(err => {/* 에러 처리 */});
    };

    const left = <div className="bg-login h-full" />;
    const right = (
        <div className="bg-white h-full flex flex-col items-center justify-center">
            <LoginForm
                email={email}
                setEmail={setEmail}
                password={password}
                setPassword={setPassword}
                onSubmit={handleLogin}
            />
            <div className="divider">간편 로그인</div>
            <SocialLoginButtons />
            <div className="text-center mt-6">
                계정이 없으신가요?{' '}
                <button
                    className="text-blue-600 font-semibold"
                    onClick={() => setShowModal(true)}
                >
                    회원가입
                </button>
            </div>
        </div>
    );

    return (
        <>
            <PageLayout left={left} right={right} />
            {showModal && <RegisterModal onClose={() => setShowModal(false)} />}
        </>
    );
}
