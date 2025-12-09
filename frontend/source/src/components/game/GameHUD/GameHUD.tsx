import React from 'react';
import classNames from 'classnames/bind';
import styles from './GameHUD.module.css';
import images from '@/assets/images'; 
import icons from '@/assets/icons'; 
import { User } from '@/types/model'; 

const cx = classNames.bind(styles);

interface GameHUDProps {
    user?: User | null;
    onOpenInventory?: () => void;
    onOpenSettings?: () => void;
}

const GameHUD: React.FC<GameHUDProps> = ({ user, onOpenInventory, onOpenSettings }) => {
    // Mock user data nếu chưa có thật
    const currentUser = user || {
        username: 'Sĩ Tử Vô Danh',
        total_xp: 300,
        current_rank: { tier: 1, name: 'Đồng Ấu', min_xp: 0 },
    };

    return (
        <div className={cx('hudContainer')}>
            {/* 1. User Info (Góc trái trên) */}
            <div className={cx('userInfo')}>
                <div className={cx('avatarFrame')}>
                    <img src={images.female_char_head} alt="Avatar" className={cx('avatarImg')} />
                </div>
                <div className={cx('stats')}>
                    <span className={cx('username')}>{currentUser.username}</span>
                    <div className={cx('xpBarWrapper')}>
                        {/* Tính % XP demo */}
                        <div className={cx('xpBarFill')} style={{ width: '60%' }}></div>
                    </div>
                </div>
            </div>

            {/* 2. Toolbar (Góc phải dưới) - Thay thế Footer */}
            <div className={cx('toolbar')}>
                <button className={cx('toolButton')} onClick={onOpenInventory} title="Hành trang">
                    <img src={icons.bag} alt="Bag" className={cx('toolIcon')} />
                </button>
                <button className={cx('toolButton')} title="Bảng vàng">
                    <img src={icons.leaderboard} alt="Rank" className={cx('toolIcon')} />
                </button>
                <button className={cx('toolButton')} title="Luyện tập">
                    <img src={icons.training} alt="Quest" className={cx('toolIcon')} />
                </button>
            </div>
        </div>
    );
};

export default GameHUD;
