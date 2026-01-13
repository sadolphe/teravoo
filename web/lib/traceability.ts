const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export type TraceabilityEvent = {
    id: number;
    stage: string; // ORIGIN, QUALITY, TRANSIT, FOB, DELIVERED
    status: "VALIDATED" | "PENDING" | "ALERT" | "CORRECTION"; // VALIDATED, PENDING, ALERT
    description: string;
    timestamp: string;
    location_scan?: string;
    documents_urls?: string[];
    created_by?: string;
};

export async function getRequestTimeline(requestId: number): Promise<TraceabilityEvent[]> {
    try {
        const res = await fetch(`${API_URL}/traceability/request/${requestId}`, { cache: 'no-store' });
        if (!res.ok) throw new Error('Failed to fetch timeline');
        return res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}
