import usePasswordToggle from '../hooks/auth/usePasswordToggle.js';

export default function PasswordInput({value, onChange, placeholder = "비밀번호", ...props}) {
    const [showPassword, toggleShow] = usePasswordToggle();

    return (
        <div className="relative mb-4">
            <input
                type={showPassword ? "text" : "password"}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 pr-12"
                autoComplete="current-password"
                {...props}
            />
            <button
                type="button"
                onClick={toggleShow}
                className="absolute right-3 top-1/2 -translate-y-1/2 bg-white hover:text-gray-700"
                tabIndex={-1}
                aria-label={showPassword ? "비밀번호 숨기기" : "비밀번호 표시"}
            >
                {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none"
                         viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                              d="M15 12a3 3 0 11-6 0 3 3 0 016 0zm6 0c0 4-6 7-9 7s-9-3-9-7 6-7 9-7 9 3 9 7z" />
                    </svg>
                ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none"
                         viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                              d="M13.875 18.825A10.05 10.05 0 0112 19c-3 0-7.5-2.25-9-7a11.72 11.72 0 012.344-3.56M4.271 4.271l15.458 15.458M9.88 9.88a3 3 0 104.24 4.24" />
                    </svg>
                )}
            </button>
        </div>
    );
}
