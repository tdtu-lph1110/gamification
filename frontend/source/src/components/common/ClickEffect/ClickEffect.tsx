import React, { useEffect } from 'react';
import classNames from 'classnames/bind';
import styles from './ClickEffect.module.css';

const cx = classNames.bind(styles);

interface ClickEffectProps {
    x: number;
    y: number;
    onComplete?: () => void; // Hàm gọi khi chạy xong animation để xóa component
}

const ClickEffect: React.FC<ClickEffectProps> = ({ x, y, onComplete }) => {
    // Tự động hủy sau 600ms (bằng thời gian animation trong CSS)
    useEffect(() => {
        const timer = setTimeout(() => {
            if (onComplete) onComplete();
        }, 600);

        return () => clearTimeout(timer);
    }, [onComplete]);

    return (
        <div className={cx('rippleContainer')} style={{ top: y, left: x }}>
            <div className={cx('dot')}></div>
            <div className={cx('ripple')}></div>
        </div>
    );
};

export default ClickEffect;
