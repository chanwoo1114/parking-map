import { useEffect } from 'react';

export default function MapPage() {
    useEffect(() => {
        if (window.vw?.ol3?.Map) {
            const options = {
                basemapType: window.vw.ol3.BasemapType.GRAPHIC,
                controlDensity: window.vw.ol3.DensityType.EMPTY,
                interactionDensity: window.vw.ol3.DensityType.FULL,
                controlsAutoArrange: true,
                homePosition: window.vw.ol3.CameraPosition,
                initPosition: window.vw.ol3.CameraPosition,
            };

            const map = new window.vw.ol3.Map('mapVO', options);

            map.getView().setCenter([127.1052131, 37.3595316]);
            map.getView().setZoom(13);
        } else {
            console.error('VWorld API가 아직 준비되지 않았습니다.');
        }
    }, []);

    // 반드시 id="mapVO" 로 맵 컨테이너를 만들어 주세요
    return <div id="mapVO" style={{ width: '100%', height: '100vh' }} />;
}
