import { useState, useEffect, useMemo } from 'react';
import debounce from 'lodash.debounce';
import { checkNicknameDuplicate } from '../../api/auth';

export default function NicknameValidation(nickname, delay = 500) {
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
                try {
                    const { is_duplicate } = await checkNicknameDuplicate(value);
                    if (is_duplicate) {
                        setValid(false);
                        setError('이미 사용 중인 닉네임입니다.');
                    } else {
                        setValid(true);
                        setError('');
                    }
                } catch {
                    setValid(false);
                    setError('닉네임 중복 검사 실패');
                }
            }, delay),
        [delay]
    );

    useEffect(() => {
        setValid(null);
        setError('');
        debouncedValidate(nickname);
        return debouncedValidate.cancel;
    }, [nickname, debouncedValidate]);

    return { valid, error };
}
