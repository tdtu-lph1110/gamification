// Khai báo cho file CSS Module (.module.css)
declare module '*.module.css' {
    const classes: { [key: string]: string };
    export default classes;
}

// Khai báo cho file CSS thường (nếu cần)
declare module '*.css';

// Khai báo cho file ảnh (để import ảnh không bị lỗi)
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.svg';
