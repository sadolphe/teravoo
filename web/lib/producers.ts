const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export type Producer = {
    id: number;
    name: string;
    location_region: string;
    location_district: string;
    bio?: string;
    badges?: string[];
    trust_score: number;
    years_experience: number;
    transactions_count: number;
};

export async function getProducers(): Promise<Producer[]> {
    try {
        const res = await fetch(`${API_URL}/producers/`, { cache: 'no-store' });
        if (!res.ok) throw new Error('Failed to fetch producers');
        return res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

export async function getProducer(id: number): Promise<Producer> {
    const res = await fetch(`${API_URL}/producers/${id}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Producer not found');
    return res.json();
}
