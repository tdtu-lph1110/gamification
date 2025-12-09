import React, { useEffect, useRef } from 'react';

interface GameCameraProps {
    charX: number;
    charY: number;
    mapWidth: number;
    mapHeight: number;
    children: React.ReactNode;
}

const GameCamera: React.FC<GameCameraProps> = ({ charX, charY, mapWidth, mapHeight, children }) => {
    const viewportRef = useRef<HTMLDivElement>(null);

    // Logic Camera Follow: Chạy mỗi khi charX, charY thay đổi
    useEffect(() => {
        if (viewportRef.current) {
            const viewport = viewportRef.current;
            const screenW = viewport.clientWidth;
            const screenH = viewport.clientHeight;

            // Tính toán vị trí cần scroll tới để nhân vật vào giữa
            // Scroll = Vị trí nhân vật - Một nửa màn hình
            const scrollLeft = charX - screenW / 2;
            const scrollTop = charY - screenH / 2;

            // Dùng scrollTo với behavior 'smooth' để camera lướt theo
            viewport.scrollTo({
                left: scrollLeft,
                top: scrollTop,
                behavior: 'smooth', // Hoặc 'auto' nếu muốn cứng
            });
        }
    }, [charX, charY]);

    return (
        <div
            ref={viewportRef}
            style={{
                width: '100vw',
                height: '100vh',
                overflow: 'hidden',
                position: 'relative',
            }}
        >
            <div
                style={{
                    width: mapWidth,
                    height: mapHeight,
                    position: 'relative',
                }}
            >
                {children}
            </div>
        </div>
    );
};

export default GameCamera;
