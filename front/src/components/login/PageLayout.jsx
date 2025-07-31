export default function PageLayout({ left, right }) {
    return (
        <div className="flex w-screen h-screen overflow-hidden">
            <div className="flex-none w-[70%]">{left}</div>
            <div className="flex-none w-[30%]">{right}</div>
        </div>
    );
}