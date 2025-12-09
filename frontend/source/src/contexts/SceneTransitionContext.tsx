import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';

interface TransitionContextType {
    startTransition: (to: string) => void;
    isTransiting: boolean;
}

const TransitionContext = createContext<TransitionContextType | undefined>(undefined);

export const SceneTransitionProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const navigate = useNavigate();
    const [isTransiting, setIsTransiting] = useState(false);

    const startTransition = (to: string) => {
        // 1. Bắt đầu hiệu ứng che màn hình
        setIsTransiting(true);

        // 2. Đợi một chút cho màn hình tối hẳn (500ms)
        setTimeout(() => {
            // 3. Thực hiện chuyển trang (Lúc này màn hình đang tối om nên user không thấy giật)
            navigate(to);

            // 4. Đợi thêm một chút để scene mới load xong DOM rồi mới mở màn hình (tùy chọn)
            setTimeout(() => {
                // 5. Kết thúc hiệu ứng (Màn hình sáng dần trở lại)
                setIsTransiting(false);
            }, 300); // Thời gian fade-out
        }, 500); // Thời gian fade-in
    };

    return (
        <TransitionContext.Provider value={{ startTransition, isTransiting }}>{children}</TransitionContext.Provider>
    );
};

// Hook để các Scene khác sử dụng
export const useSceneTransition = () => {
    const context = useContext(TransitionContext);
    if (!context) {
        throw new Error('useSceneTransition must be used within a SceneTransitionProvider');
    }
    return context;
};
