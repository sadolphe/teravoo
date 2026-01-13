"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getProducers, Producer } from "@/lib/producers";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function ProducersListPage() {
    const router = useRouter();
    const [producers, setProducers] = useState<Producer[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getProducers().then(data => {
            setProducers(data);
            setLoading(false);
        });
    }, []);

    if (loading) return <div className="p-10 text-center text-muted-foreground">Loading trusted partners...</div>;

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="container mx-auto max-w-6xl">
                <div className="mb-8 text-center">
                    <h1 className="text-4xl font-serif font-bold mb-2">Our Producers</h1>
                    <p className="text-muted-foreground max-w-2xl mx-auto">
                        Discover our network of verified facilitators and cooperatives.
                        TeraVoo ensures direct trade with complete traceability and impact.
                    </p>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {producers.length === 0 && (
                        <div className="col-span-full text-center py-12 border rounded bg-muted/20">
                            No producers found.
                        </div>
                    )}
                    {producers.map(producer => (
                        <Card key={producer.id} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push(`/producers/${producer.id}`)}>
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle className="text-xl font-bold">{producer.name}</CardTitle>
                                        <p className="text-sm text-muted-foreground">{producer.location_district}, {producer.location_region}</p>
                                    </div>
                                    <div className="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded border border-yellow-200">
                                        <span className="text-yellow-600 font-bold">★ {producer.trust_score.toFixed(1)}</span>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="pb-4">
                                <p className="text-sm text-gray-600 line-clamp-3 mb-4">{producer.bio || "No biography available."}</p>
                                <div className="flex flex-wrap gap-2">
                                    {producer.badges?.map(badge => (
                                        <Badge key={badge} variant="secondary" className="text-xs">{badge}</Badge>
                                    ))}
                                </div>
                            </CardContent>
                            <CardFooter className="pt-0 flex justify-between items-center text-sm text-muted-foreground border-t bg-muted/10 p-4">
                                <span>{producer.years_experience} Yrs Exp.</span>
                                <span>{producer.transactions_count} Sales</span>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}
