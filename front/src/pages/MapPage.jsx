// src/pages/MapPage.jsx
import React from 'react';
import useCurrentPosition from '../hooks/useCurrentPosition';
import VWorldMap from '../components/map/VWorldMap';

export default function MapPage() {
    const defaultCenter = [127.1052131, 37.3595316];
    const { coords, loading } = useCurrentPosition(defaultCenter);

    if (loading) {
        return <div>위치 정보를 불러오는 중…</div>;
    }

    return <VWorldMap center={coords} />;
}
