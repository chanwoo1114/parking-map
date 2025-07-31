// OAuthCallback.jsx
import { useState, useEffect } from 'react';
import { useSearchParams, useParams } from 'react-router-dom';
import useAuth from '../hooks/auth/useAuth';

export default function OAuthCallback() {
    const [called, setCalled] = useState(false);
    const [qs] = useSearchParams();
    const { provider } = useParams();
    const code = qs.get('code');
    const { handleSocial } = useAuth();

    useEffect(() => {
        if (provider && code && !called) {
            setCalled(true);
            handleSocial(provider, code)
                .catch(err => console.error(err));
        }
    }, [provider, code, called]);

    return <div>로그인 처리 중…</div>;
}
