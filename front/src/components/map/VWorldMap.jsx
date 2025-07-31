import React, { useEffect, useRef } from 'react';

const defaultOptions = {
    basemapType: window.vw.ol3.BasemapType.GRAPHIC,
    controlDensity: window.vw.ol3.DensityType.EMPTY,
    interactionDensity: window.vw.ol3.DensityType.FULL,
    controlsAutoArrange: true,
    homePosition: window.vw.ol3.CameraPosition,
    initPosition: window.vw.ol3.CameraPosition,
};

export default function VWorldMap({ center, zoom = 13 }) {
    const mapRef = useRef(null);

    useEffect(() => {
        if (!window.vw?.ol3?.Map) {
            console.error('VWorld API가 준비되지 않았습니다.');
            return;
        }
        const map = new window.vw.ol3.Map(mapRef.current, defaultOptions);
        map.getView().setCenter(center);
        map.getView().setZoom(zoom);
    }, [center, zoom]);

    return (
        <div
            ref={mapRef}
            id="mapVO"
            style={{ width: '100%', height: '100vh' }}
        />
    );
}
