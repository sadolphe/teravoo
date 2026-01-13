"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getProducer, Producer } from "@/lib/producers";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function ProducerDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [producer, setProducer] = useState<Producer | null>(null);

    useEffect(() => {
        if (params.id) {
            getProducer(Number(params.id)).then(setProducer);
        }
    }, [params.id]);

    if (!producer) return <div className="p-10 text-center">Loading Profile...</div>;

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="container mx-auto max-w-4xl">
                <Button variant="ghost" className="mb-4 pl-0" onClick={() => router.push('/producers')}>
                    ← Back to List
                </Button>

                {/* HEADER */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                    <div>
                        <h1 className="text-4xl font-bold font-serif">{producer.name}</h1>
                        <div className="flex items-center gap-2 text-muted-foreground mt-2">
                            <span>📍 {producer.location_district}, {producer.location_region}</span>
                            <span>•</span>
                            <span>Member since 2024</span>
                        </div>
                    </div>
                    <Button size="lg" className="bg-primary text-primary-foreground shadow-lg" onClick={() => router.push('/requests/create')}>
                        Ask for a Quote
                    </Button>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {/* LEFT: INFO & BIO */}
                    <div className="md:col-span-2 space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>About the Facilitator</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-gray-700 leading-relaxed whitespace-pre-line">{producer.bio || "No biography provided."}</p>

                                <div className="mt-6">
                                    <h3 className="font-bold mb-2 text-sm uppercase text-muted-foreground">Verified Badges</h3>
                                    <div className="flex gap-2">
                                        {producer.badges?.map(badge => (
                                            <Badge key={badge} variant="outline" className="border-green-600 text-green-700 bg-green-50 px-3 py-1">
                                                {badge}
                                            </Badge>
                                        ))}
                                        {(!producer.badges || producer.badges.length === 0) && <span className="text-sm italic text-muted-foreground">No badges yet.</span>}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* MOCK MAP */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Location</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="h-64 bg-muted rounded-md flex items-center justify-center relative overflow-hidden">
                                    <div className="absolute inset-0 bg-blue-50 opacity-50"></div>
                                    <span className="relative z-10 font-mono text-muted-foreground"> Interactive Map Placeholder (Mapbox/Leaflet) </span>
                                </div>
                                <p className="text-xs text-muted-foreground mt-2 text-center">
                                    * Detailed GPS coordinates are protected for security reasons.
                                </p>
                            </CardContent>
                        </Card>
                    </div>

                    {/* RIGHT: TRUST SCORE */}
                    <div className="space-y-6">
                        <Card className="border-yellow-200 bg-yellow-50/30">
                            <CardHeader>
                                <CardTitle className="text-center text-yellow-800">Trust Score</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="text-center">
                                    <span className="text-5xl font-bold text-yellow-600">{producer.trust_score.toFixed(1)}</span>
                                    <span className="text-xl text-yellow-600/60">/5.0</span>
                                </div>

                                <div className="space-y-3">
                                    <div className="space-y-1">
                                        <div className="flex justify-between text-xs font-medium">
                                            <span>Quality Match</span>
                                            <span>98%</span>
                                        </div>
                                        <Progress value={98} className="h-2 bg-yellow-100" />
                                    </div>
                                    <div className="space-y-1">
                                        <div className="flex justify-between text-xs font-medium">
                                            <span>Logistics Speed</span>
                                            <span>92%</span>
                                        </div>
                                        <Progress value={92} className="h-2 bg-yellow-100" />
                                    </div>
                                    <div className="space-y-1">
                                        <div className="flex justify-between text-xs font-medium">
                                            <span>Response Rate</span>
                                            <span>100%</span>
                                        </div>
                                        <Progress value={100} className="h-2 bg-yellow-100" />
                                    </div>
                                </div>

                                <div className="pt-4 border-t border-yellow-200/50 flex justify-between text-sm">
                                    <div className="text-center w-1/2 border-r border-yellow-200/50">
                                        <div className="font-bold text-lg">{producer.transactions_count}</div>
                                        <div className="text-xs text-muted-foreground">Deals</div>
                                    </div>
                                    <div className="text-center w-1/2">
                                        <div className="font-bold text-lg">{producer.years_experience}</div>
                                        <div className="text-xs text-muted-foreground">Years Exp.</div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="bg-blue-50 p-4 rounded text-xs text-blue-900 leading-snug">
                            <strong>Why Trust?</strong> This profile is verified by TeraVoo on-ground agents. Last audit: 2 weeks ago.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
