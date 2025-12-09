export interface Rank {
    id: number;
    name: string;
    tier: number;
    min_xp: number;
    metadata?: {
        color?: string;
    };
}

export interface User {
    id: string;
    username: string;
    email: string;
    total_xp: number;
    currency: number;
    current_rank: Rank | null;
    current_streak: number;
}
