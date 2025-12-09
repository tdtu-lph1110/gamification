import React from 'react';
import classNames from 'classnames/bind';
import styles from './InteractionZone.module.css';

const cx = classNames.bind(styles);

interface InteractionZoneProps {
    // Vị trí và kích thước (đơn vị % hoặc px)
    top: string | number;
    left: string | number;
    width: string | number;
    height: string | number;

    // Nội dung & Hành động
    label?: string; // Tên hiện ra khi hover (VD: "Ra ngoài")
    onClick?: () => void; // Hàm chạy khi click

    // Tùy chọn nâng cao
    className?: string; // Class CSS thêm nếu cần
    debug?: boolean; // Bật true để hiện khung đỏ (dễ căn chỉnh vị trí)
    children?: React.ReactNode; // Nếu muốn bọc một hình ảnh nào đó (VD: NPC, Rương)
}

const InteractionZone: React.FC<InteractionZoneProps> = ({
    top,
    left,
    width,
    height,
    label,
    onClick,
    className,
    debug = false,
    children,
}) => {
    return (
        <div
            className={cx('zone', { debug }, className)}
            style={{
                top,
                left,
                width,
                height,
            }}
            onClick={onClick}
        >
            {label && <div className={cx('label')}>{label}</div>}
            {children}
        </div>
    );
};

export default InteractionZone;
