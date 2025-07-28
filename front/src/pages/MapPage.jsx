export default function MapPage() {
    return (
        <div className="w-full h-screen">
            <iframe
                title="공공데이터포털 지도"
                src="여기에-공공데이터포털-지도-embed-URL"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen
            ></iframe>
        </div>
    );
}