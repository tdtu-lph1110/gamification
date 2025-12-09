import React from 'react';
import classNames from 'classnames/bind';
import styles from './GameSprite.module.css';

const cx = classNames.bind(styles);

interface GameSpriteProps {
    // Tọa độ (Có thể là % hoặc px)
    x: string | number;
    y: string | number;

    // Hình ảnh nhân vật
    src: string;

    // Kích thước (mặc định 64px)
    width?: number;

    // Thông tin hiển thị thêm
    name?: string; // Tên hiển thị trên đầu

    // Sự kiện
    onClick?: () => void;

    // CSS tùy chỉnh thêm
    className?: string;
}

const GameSprite: React.FC<GameSpriteProps> = ({ x, y, src, width = 64, name, onClick, className }) => {
    return (
        <div
            className={cx('characterContainer', className)}
            style={{
                top: y,
                left: x,
                width: `${width}px`,
            }}
            onClick={onClick}
        >
            {/* Nếu có tên thì hiện NameTag */}
            {name && <div className={cx('nameTag')}>{name}</div>}

            {/* Hình ảnh nhân vật */}
            <img src={src} alt="Character" className={cx('characterImg')} draggable={false} />
        </div>
    );
};

export default GameSprite;
