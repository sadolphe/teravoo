"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getProducers, Producer } from "@/lib/producers";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MapPin, ShieldCheck, Star, Users } from "lucide-react";

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

    // Deterministic visual assets based on ID
    const getCoverImage = (id: number) => {
        const variants = [
            "https://placehold.co/600x300/1B5E20/FFFFFF?text=Vanilla+Fields",
            "https://placehold.co/600x300/2E7D32/FFFFFF?text=Curing+Station",
            "https://placehold.co/600x300/388E3C/FFFFFF?text=Harvest+Day"
        ];
        return variants[id % variants.length];
    };

    const getAvatarColor = (id: number) => {
        const colors = ["bg-blue-100 text-blue-700", "bg-green-100 text-green-700", "bg-orange-100 text-orange-700", "bg-purple-100 text-purple-700"];
        return colors[id % colors.length];
    };

    if (loading) return (
        <div className="min-h-screen flex items-center justify-center bg-background">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
    );

    return (
        <div className="min-h-screen bg-background font-sans">
            {/* Header Section */}
            <div className="bg-[#1B5E20] text-white py-20">
                <div className="container mx-auto px-6 text-center">
                    <Badge className="mb-4 bg-white/10 text-white hover:bg-white/20 border-none uppercase tracking-widest text-xs">
                        Trusted Partners
                    </Badge>
                    <h1 className="text-4xl md:text-5xl font-serif font-bold mb-6">Meet the Guardians of Quality</h1>
                    <p className="text-white/80 max-w-2xl mx-auto text-lg leading-relaxed">
                        We work directly with audited cooperatives and facilitators in Madagascar.
                        Every partner is vetted for fair labor practices and sustainable farming.
                    </p>
                </div>
            </div>

            <div className="container mx-auto max-w-7xl px-6 py-16">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {producers.length === 0 && (
                        <div className="col-span-full py-20 text-center border-2 border-dashed border-gray-200 rounded-xl bg-gray-50">
                            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-gray-700">No producers found</h3>
                            <p className="text-gray-500">Check back soon as we onboard new partners.</p>
                        </div>
                    )}

                    {producers.map(producer => (
                        <Card
                            key={producer.id}
                            className="group hover:shadow-xl transition-all duration-300 border-border/60 overflow-hidden bg-card"
                        >
                            {/* Visual Header */}
                            <div className="relative h-48 overflow-hidden bg-gray-100 cursor-pointer" onClick={() => router.push(`/producers/${producer.id}`)}>
                                <img
                                    src={getCoverImage(producer.id)}
                                    alt="Farm cover"
                                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                                <div className="absolute bottom-4 left-4 text-white">
                                    <h2 className="text-2xl font-serif font-bold shadow-sm">{producer.name}</h2>
                                    <div className="flex items-center gap-2 text-sm opacity-90">
                                        <MapPin className="w-3 h-3" />
                                        {producer.location_district}, {producer.location_region}
                                    </div>
                                </div>
                            </div>

                            <CardContent className="pt-6 relative">
                                {/* Trust Badge overlay */}
                                <div className="absolute -top-6 right-4">
                                    <div className="bg-white p-1 rounded-full shadow-md">
                                        <div className="bg-green-100 text-green-800 p-2 rounded-full flex items-center gap-1 text-xs font-bold border border-green-200" title="Trust Score">
                                            <ShieldCheck className="w-4 h-4" />
                                            <span>{producer.trust_score.toFixed(1)}/10</span>
                                        </div>
                                    </div>
                                </div>

                                <p className="text-muted-foreground line-clamp-3 mb-6 leading-relaxed text-sm">
                                    {producer.bio || "A dedicated partner committed to excellence in vanilla curing and sustainable agriculture."}
                                </p>

                                <div className="flex items-center justify-between p-4 bg-muted/40 rounded-lg">
                                    <div className="text-center">
                                        <div className="text-xl font-bold text-primary">{producer.years_experience}</div>
                                        <div className="text-xs text-muted-foreground uppercase tracking-wide">Years Exp.</div>
                                    </div>
                                    <div className="h-8 w-[1px] bg-border"></div>
                                    <div className="text-center">
                                        <div className="text-xl font-bold text-primary">{producer.transactions_count}</div>
                                        <div className="text-xs text-muted-foreground uppercase tracking-wide">Deals</div>
                                    </div>
                                    <div className="h-8 w-[1px] bg-border"></div>
                                    <div className="text-center">
                                        <div className="text-xl font-bold text-primary">{producer.badges?.length || 0}</div>
                                        <div className="text-xs text-muted-foreground uppercase tracking-wide">Badges</div>
                                    </div>
                                </div>

                                <div className="flex flex-wrap gap-2 mt-6">
                                    {producer.badges?.map(badge => (
                                        <Badge key={badge} variant="outline" className="text-xs border-primary/20 text-primary bg-primary/5">
                                            {badge}
                                        </Badge>
                                    ))}
                                </div>
                            </CardContent>

                            <CardFooter className="pt-0 pb-6">
                                <Button
                                    className="w-full bg-secondary text-primary hover:bg-secondary/90 transition-colors shadow-none font-semibold"
                                    onClick={() => router.push(`/producers/${producer.id}`)}
                                >
                                    View Full Profile
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}
