export interface LevelNode {
    id: string; // ID định danh (vd: 'lv1')
    label: string; // Tên hiển thị (vd: 'Nhập Môn')
    status: 'locked' | 'unlocked' | 'completed';
    x: number; // Vị trí trái phải (%) - Ví dụ: 50 là giữa màn hình
    y: number; // Vị trí trên dưới (px) - Tính từ đỉnh map
    icon?: string; // Icon riêng nếu có
}

export const levels: LevelNode[] = [
    { id: 'lv1', label: 'Cổng Làng', status: 'completed', x: 50, y: 100 },
    { id: 'lv2', label: 'Ruộng Lúa', status: 'unlocked', x: 20, y: 250 }, // Lượn sang trái
    { id: 'lv3', label: 'Giếng Nước', status: 'locked', x: 80, y: 400 }, // Lượn sang phải
    { id: 'lv4', label: 'Trường Thi', status: 'locked', x: 50, y: 550 }, // Về giữa
    { id: 'lv5', label: 'Kinh Thành', status: 'locked', x: 50, y: 700 }, // Đích đến
];
