import { useState, useEffect } from 'react';

export default function useCurrentPosition(defaultCoords) {
    const [coords, setCoords] = useState(defaultCoords);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!navigator.geolocation) {
            setError('Geolocation not supported');
            setLoading(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                setCoords([position.coords.longitude, position.coords.latitude]);
                setLoading(false);
            },
            (err) => {
                console.warn('Geolocation error:', err.message);
                setError(err.message);
                setCoords(defaultCoords);
                setLoading(false);
            },
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    }, [defaultCoords]);

    return { coords, error, loading };
}