import React from 'react';
import { getSocialLoginUrl } from '../../api/auth.js';
import kakaoIcon from '../../assets/kakao-icon.png';
import googleIcon from '../../assets/google-icon.png';

const providers = [
    {
        name: 'kakao',
        img: kakaoIcon,
        alt: '카카오로 로그인',
    },
    {
        name: 'google',
        img: googleIcon,
        alt: '구글로 로그인',
    },
];

export default function SocialLoginButtons() {
    return (
        <div className="flex justify-center gap-4 mt-4">
            {providers.map(({ name, img, alt }) => (
                <a
                    key={name}
                    href={getSocialLoginUrl(name)}
                    aria-label={alt}
                    className="w-12 h-12 flex items-center justify-center rounded-full hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-blue-500"
                >
                    <img src={img} alt={alt} className="w-6 h-6" />
                </a>
            ))}
        </div>
    );
}
