import { useState } from 'react';
import { registerUser } from '../api/auth';
import EmailValidation from '../hooks/auth/EmailValidation';
import NicknameValidation from '../hooks/auth/NicknameValidation';
import validatePassword from '../utils/validatePassword';
import PasswordInput from './PasswordInput';

export default function RegisterModal({ onClose, onRegisterSuccess }) {
    const [email, setEmail] = useState('');
    const { valid: emailValid, error: emailError } = EmailValidation(email);
    const [pw1, setPw1] = useState('');
    const [pw2, setPw2] = useState('');
    const [nickname, setNickname] = useState('');
    const { valid: nicknameValid, error: nicknameError } = NicknameValidation(nickname);
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('male');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async () => {
        setError('');
        // 필수 필드 체크
        if (!email || !pw1 || !pw2 || !nickname || !age) {
            setError('모든 필드를 입력하세요.');
            return;
        }
        // 이메일 검증
        if (emailValid !== true) {
            setError(emailError || '이메일을 확인해주세요.');
            return;
        }
        // 닉네임 검증
        if (nicknameValid !== true) {
            setError(nicknameError || '닉네임을 확인해주세요.');
            return;
        }
        // 비밀번호 유효성
        const pwError = validatePassword(pw1, pw2);
        if (pwError) {
            setError(pwError);
            return;
        }

        setLoading(true);
        try {
            await registerUser({
                email,
                password1: pw1,
                password2: pw2,
                nickname,
                age: Number(age),
                gender,
            });
            alert('회원가입 성공! 로그인 해주세요.');
            onClose();
            if (onRegisterSuccess) onRegisterSuccess();
        } catch (err) {
            setError(err.detail || '회원가입 실패');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center">
            <div className="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl relative">
                <button
                    className="absolute top-4 right-4 text-2xl text-gray-400 hover:text-gray-700"
                    onClick={onClose}
                    disabled={loading}
                >×</button>
                <h2 className="text-2xl font-bold text-center mb-8 text-gray-700">회원가입</h2>

                <div className="flex flex-col gap-3">
                    {/* 이메일 입력 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">이메일</label>
                        <input
                            type="email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            placeholder="이메일"
                            className="w-full px-4 py-3 border rounded-lg"
                            disabled={loading}
                        />
                        {emailValid === false && (
                            <div className="text-red-500 text-sm mt-1">{emailError}</div>
                        )}
                        {emailValid === true && (
                            <div className="text-green-600 text-sm mt-1">사용 가능한 이메일입니다.</div>
                        )}
                    </div>

                    {/* 비밀번호 입력 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">비밀번호</label>
                        <PasswordInput
                            value={pw1}
                            onChange={e => setPw1(e.target.value)}
                            placeholder="비밀번호"
                            disabled={loading}
                        />
                    </div>

                    {/* 비밀번호 확인 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">비밀번호 확인</label>
                        <PasswordInput
                            value={pw2}
                            onChange={e => setPw2(e.target.value)}
                            placeholder="비밀번호 확인"
                            disabled={loading}
                        />
                    </div>

                    {/* 닉네임 입력 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">닉네임</label>
                        <input
                            type="text"
                            value={nickname}
                            onChange={e => setNickname(e.target.value)}
                            placeholder="닉네임"
                            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                            disabled={loading}
                        />
                        {nicknameValid === false && (
                            <div className="text-red-500 text-sm mt-1">{nicknameError}</div>
                        )}
                        {nicknameValid === true && (
                            <div className="text-green-600 text-sm mt-1">사용 가능한 닉네임입니다.</div>
                        )}
                    </div>

                    {/* 나이 입력 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">나이</label>
                        <input
                            type="number"
                            value={age}
                            onChange={e => setAge(e.target.value)}
                            placeholder="나이"
                            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                            disabled={loading}
                        />
                    </div>

                    {/* 성별 선택 */}
                    <div>
                        <label className="text-gray-600 text-sm mb-1 block">성별</label>
                        <div className="flex gap-4 mt-1">
                            <label className="flex items-center">
                                <input
                                    type="radio"
                                    name="gender"
                                    value="male"
                                    checked={gender === 'male'}
                                    onChange={() => setGender('male')}
                                    className="mr-2"
                                    disabled={loading}
                                /> 남성
                            </label>
                            <label className="flex items-center">
                                <input
                                    type="radio"
                                    name="gender"
                                    value="female"
                                    checked={gender === 'female'}
                                    onChange={() => setGender('female')}
                                    className="mr-2"
                                    disabled={loading}
                                /> 여성
                            </label>
                        </div>
                    </div>
                </div>

                {/* 폼 에러 */}
                {error && <div className="text-red-500 mt-4 mb-2 text-center">{error}</div>}

                {/* 제출 버튼 */}
                <button
                    className="w-full mt-6 bg-gradient-to-r from-blue-500 to-blue-700 text-white py-3 rounded-lg font-bold text-lg shadow-lg hover:from-blue-600 hover:to-blue-800"
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? "가입 중..." : "회원가입"}
                </button>
            </div>
        </div>
    );
}