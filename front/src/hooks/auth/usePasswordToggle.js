import { useState} from "react";

export default function usePasswordToggle() {
    const [showPassword, setShowPassword] = useState(false);
    const toggle = () => setShowPassword((v) => !v);
    return [showPassword, toggle];
}