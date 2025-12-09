import React from 'react';
import classNames from 'classnames/bind';
import styles from './SceneTransitionUI.module.css';
import images from '@/assets/images';
import { useSceneTransition } from '@/contexts/SceneTransitionContext';

const cx = classNames.bind(styles);

const SceneTransitionUI = () => {
    const { isTransiting } = useSceneTransition();

    return (
        <div className={cx('overlay', { active: isTransiting })}>
            <img src={images.book} alt="Loading..." className={cx('loadingIcon')} />
            <div className={cx('loadingText')}>ĐANG KHỞI HÀNH...</div>
        </div>
    );
};

export default SceneTransitionUI;
