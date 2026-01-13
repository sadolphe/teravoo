"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getRequests, SourcingRequest } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

export default function RequestsDashboard() {
    const router = useRouter();
    const [requests, setRequests] = useState<SourcingRequest[]>([]);

    useEffect(() => {
        getRequests().then(setRequests);
    }, []);

    return (
        <div className="min-h-screen bg-background font-sans text-foreground">
            <main className="container mx-auto px-6 py-12">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-serif font-bold text-primary">Sourcing Requests</h1>
                    <Button onClick={() => router.push('/requests/create')}>+ New Request</Button>
                </div>

                {requests.length === 0 ? (
                    <div className="text-center py-20 bg-muted/30 rounded-lg">
                        <p className="text-muted-foreground mb-4">You haven't posted any sourcing requests yet.</p>
                        <Button onClick={() => router.push('/requests/create')}>Start Sourcing</Button>
                    </div>
                ) : (
                    <div className="grid gap-6">
                        {requests.map((req) => {
                            // Calculate coverage logic (mock for list view if offers not populated deeply)
                            const coveredKg = req.offers ? req.offers.reduce((acc, o) => acc + o.volume_offered_kg, 0) : 0;
                            const percent = Math.min(100, Math.round((coveredKg / req.volume_target_kg) * 100));

                            return (
                                <Card key={req.id} className="cursor-pointer hover:border-primary transition-colors" onClick={() => router.push(`/requests/${req.id}`)}>
                                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                                        <div className="space-y-1">
                                            <CardTitle className="text-lg flex items-center gap-3">
                                                {req.product_type} <Badge variant="outline">Grade {req.grade_target}</Badge>
                                            </CardTitle>
                                            <div className="text-sm text-muted-foreground">
                                                Target: {req.volume_target_kg} kg @ ${req.price_target_usd}/kg
                                            </div>
                                        </div>
                                        <Badge className={req.status === 'OPEN' ? 'bg-green-100 text-green-800' : ''}>
                                            {req.status}
                                        </Badge>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="mt-4 space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span>Sourcing Progress</span>
                                                <span className="font-bold">{percent}% ({coveredKg} kg)</span>
                                            </div>
                                            <Progress value={percent} className="h-2" />
                                            <div className="flex justify-between items-center mt-4">
                                                <div className="flex gap-2 text-xs text-muted-foreground">
                                                    <span>{req.offers ? req.offers.length : 0} Offers received</span>
                                                </div>

                                                {/* Only show Delete if no accepted offers and logistics in PREPARING */}
                                                {(!req.offers?.some(o => o.status === 'ACCEPTED') && (!req.logistics_status || req.logistics_status === 'PREPARING')) && (
                                                    <Button
                                                        size="sm"
                                                        variant="ghost"
                                                        className="h-7 text-xs text-muted-foreground hover:bg-red-50 hover:text-red-600"
                                                        onClick={async (e) => {
                                                            e.stopPropagation();
                                                            if (!confirm("Are you sure you want to delete this request?")) return;
                                                            try {
                                                                const { deleteRequest } = await import("@/lib/api");
                                                                await deleteRequest(req.id);
                                                                setRequests(prev => prev.filter(r => r.id !== req.id));
                                                            } catch (err: any) {
                                                                alert("Failed to delete: " + (err.message || "Unknown error"));
                                                            }
                                                        }}
                                                    >
                                                        Delete
                                                    </Button>
                                                )}
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            );
                        })}
                    </div>
                )}
            </main>
        </div>
    );
}
