import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import classNames from 'classnames/bind';
import styles from './HomeScene.module.css';
import images from '@/assets/images';
import { GameSprite } from '@/components/game';
import { ClickEffect, InteractionZone } from '@/components/common';
import { useSceneTransition } from '@/contexts/SceneTransitionContext';

const cx = classNames.bind(styles);

const HomeScene = () => {
    const containerRef = useRef<HTMLDivElement>(null);
    const { startTransition } = useSceneTransition();
    const [charPos, setCharPos] = useState({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
    const [clickEffect, setClickEffect] = useState<{ x: number; y: number; id: number } | null>(null);
    // Hàm xử lý khi click vào nền nhà (Di chuyển)
    const handleMapClick = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!containerRef.current) return;

        // Lấy hình chữ nhật bao quanh khung game
        const rect = containerRef.current.getBoundingClientRect();

        // Tính toán tọa độ click tương đối so với khung game
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Cập nhật vị trí nhân vật đi tới
        setCharPos({ x, y });

        // Kích hoạt hiệu ứng Click ngay tại điểm đó
        setClickEffect({ x, y, id: Date.now() });

        console.log(`Walking to: ${Math.round(x)}, ${Math.round(y)}`);
    };

    const handleExit = () => {
        // Gọi hàm chuyển cảnh mượt mà
        console.log('Ra khỏi nhà...');
        startTransition('/world-map');
    };

    const handleCharacterClick = () => {
        console.log('Click vào nhân vật: Hiện thông tin Profile');
    };

    return (
        <div className={cx('sceneContainer')} ref={containerRef} onClick={handleMapClick}>
            {/* Cổng ra vào */}
            <div onClick={(e) => e.stopPropagation()}>
                <InteractionZone
                    top="50%"
                    left="50%"
                    width="150px"
                    height="200px"
                    label="Ra ngoài (Bản đồ)"
                    onClick={handleExit}
                />
            </div>

            {clickEffect && (
                <ClickEffect
                    key={clickEffect.id}
                    x={clickEffect.x}
                    y={clickEffect.y}
                    onComplete={() => setClickEffect(null)}
                />
            )}

            <GameSprite
                x={charPos.x}
                y={charPos.y}
                width={80}
                src={images.spriteFullBody}
                name="Sĩ Tử Hào"
                onClick={handleCharacterClick}
            />
        </div>
    );
};

export default HomeScene;
