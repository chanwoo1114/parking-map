import { useState, useEffect, useMemo } from 'react';
import debounce from 'lodash.debounce';
import { checkEmailDuplicate } from '../../api/auth';

export default function emailValidation(email, delay = 500) {
    const [valid, setValid] = useState(null);
    const [error, setError] = useState('');

    const debouncedValidate = useMemo(
        () =>
            debounce(async (value) => {
                if (!value) {
                    setValid(null);
                    setError('');
                    return;
                }
                // 형식 검사
                if (!/\S+@\S+\.\S+/.test(value)) {
                    setValid(false);
                    setError('유효한 이메일을 입력하세요.');
                    return;
                }
                // 중복 검사
                try {
                    const { is_duplicate } = await checkEmailDuplicate(value);
                    if (is_duplicate) {
                        setValid(false);
                        setError('이미 사용중인 이메일입니다.');
                    } else {
                        setValid(true);
                        setError('');
                    }
                } catch {
                    setValid(false);
                    setError('이메일 중복 검사 실패');
                }
            }, delay),
        [delay]
    );

    useEffect(() => {
        setValid(null);
        setError('');
        debouncedValidate(email);
        return debouncedValidate.cancel;
    }, [email, debouncedValidate]);

    return { valid, error };
}
