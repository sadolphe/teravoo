"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Timeline, TraceabilityEvent } from "@/components/traceability/Timeline";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Mock fetch function (replace with real API call later)
async function getTraceabilityEvents(orderId: number): Promise<TraceabilityEvent[]> {
    // Simulate API delay
    await new Promise(r => setTimeout(r, 800));

    // Return mock data for verification
    return [
        {
            id: 1,
            stage: "ORIGIN",
            status: "VALIDATED",
            description: "Harvest declared by Sava Gold Collectors. Batch #BATCH-2024-001 created.",
            location_scan: "-14.266, 50.166",
            timestamp: new Date(Date.now() - 86400000 * 5).toISOString(),
            created_by: "Facilitator App",
            documents_urls: ["harvest_log.pdf"]
        },
        {
            id: 2,
            stage: "QUALITY_CHECK",
            status: "VALIDATED",
            description: "Moisture content analyzed: 32%. Vanillin content: 1.8%.",
            timestamp: new Date(Date.now() - 86400000 * 4).toISOString(),
            created_by: "System (AI Scan)",
        },
        {
            id: 3,
            stage: "TRANSIT",
            status: "PENDING",
            description: "Goods loaded for transport to Port of Vohemar.",
            timestamp: new Date(Date.now() - 3600000).toISOString(),
            created_by: "Logistics Partner",
        }
    ];
}

export default function OrderTraceabilityPage() {
    const params = useParams();
    const [events, setEvents] = useState<TraceabilityEvent[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (params.id) {
            getTraceabilityEvents(Number(params.id)).then(data => {
                setEvents(data);
                setLoading(false);
            });
        }
    }, [params.id]);

    if (loading) return <div className="p-10 text-center">Loading Traceability Data...</div>;

    return (
        <div className="container mx-auto p-6 max-w-4xl">
            <h1 className="text-3xl font-bold font-serif mb-6">Order Traceability</h1>
            <p className="text-muted-foreground mb-8">
                Tracking history for Order #{params.id}. All events are immutable and verified.
            </p>

            <Card>
                <CardHeader>
                    <CardTitle>Shipment Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                    <Timeline events={events} />
                </CardContent>
            </Card>
        </div>
    );
}
