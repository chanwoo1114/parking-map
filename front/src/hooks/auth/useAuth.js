import { useNavigate } from 'react-router-dom';
import { loginUser, socialCallback } from '../../api/auth';
import { saveTokens } from '../../utils/token';

export default function useAuth() {
    const navigate = useNavigate();

    async function login({ email, password }) {
        const data = await loginUser({ email, password });
        saveTokens(data);
        navigate('/map');
    }

    async function handleSocial(provider, code) {
        const data = await socialCallback(provider, code);
        saveTokens(data);
        navigate('/map');
    }

    return { login, handleSocial };
}
