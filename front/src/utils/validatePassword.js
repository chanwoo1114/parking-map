export default function validatePassword(password1, password2) {
    if (password1 !== password2) {
        return "비밀번호가 일치하지 않습니다.";
    }
    if (password1.length < 8 || password1.length > 30) {
        return "비밀번호는 최소 8자리 이상 또는 30자리 이하이어야 합니다.";
    }
    if (!/[A-Za-z]/.test(password1)) {
        return "비밀번호에는 영문자가 포함되어야 합니다.";
    }
    if (!/[0-9]/.test(password1)) {
        return "비밀번호에는 숫자가 포함되어야 합니다.";
    }
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password1)) {
        return "비밀번호에는 특수문자가 포함되어야 합니다.";
    }
    if (/(.)\1\1/.test(password1)) {
        return "같은 문자를 3번 이상 반복할 수 없습니다.";
    }
    return null;
}