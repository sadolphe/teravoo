"use client";

import { useEffect, useState, use } from "react";
import { getProducts, createOrder, Product, getProductTraceability } from "@/lib/api";
import { Timeline, TraceabilityEvent } from "@/components/traceability/Timeline";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
    Card,
    CardContent,
} from "@/components/ui/card";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { BuyerSignupDialog } from "@/components/auth/buyer-signup-dialog";

export default function ProductPage({ params }: { params: Promise<{ id: string }> }) {
    // In Next.js 15+ params is a promise
    const resolvedParams = use(params);
    const [product, setProduct] = useState<Product | null>(null);
    const [offerPrice, setOfferPrice] = useState<number>(0);
    const [isOrderCreated, setIsOrderCreated] = useState(false);
    const [contractUrl, setContractUrl] = useState<string | null>(null);
    const [showSignupDialog, setShowSignupDialog] = useState(false);
    const [traceEvents, setTraceEvents] = useState<TraceabilityEvent[]>([]);

    useEffect(() => {
        // In a real app we would have getProductById(id)
        // For MVP we fetch all and filter client side
        getProducts().then((products) => {
            const p = products.find(p => p.id === Number(resolvedParams.id));
            if (p) {
                setProduct(p);
                setOfferPrice(p.price_fob * 10);

                // Fetch Traceability
                getProductTraceability(p.id).then(setTraceEvents);
            }
        });
    }, [resolvedParams.id]);

    const handleConfirmOffer = async () => {
        if (!product) return;
        try {
            const order = await createOrder(product.id, offerPrice);
            // Simulate Contract Gen instantly for MVP demo
            const contractPath = `/api/v1/orders/${order.id}/contract`;
            await fetch(`http://localhost:8000${contractPath}`, { method: 'POST' });

            setIsOrderCreated(true);
            setContractUrl(`http://localhost:8000/api/v1/orders/${order.id}/contract`);
        } catch (e) {
            alert("Error creating order");
        }
    };

    if (!product) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

    return (
        <div className="min-h-screen bg-background font-sans text-foreground pb-20">
            {/* Header (Simplified) */}
            <header className="sticky top-0 z-20 w-full backdrop-blur-md bg-background/80 border-b border-border">
                <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="font-serif text-xl font-bold text-primary cursor-pointer" onClick={() => window.location.href = '/'}>
                        ← Back to Marketplace
                    </div>
                </div>
            </header>

            <main className="container mx-auto px-6 py-10">
                <div className="grid md:grid-cols-2 gap-12">
                    {/* Left: Visuals */}
                    <div className="space-y-6">
                        <div className="aspect-[4/3] bg-muted rounded-xl overflow-hidden shadow-xl relative">
                            <img src={product.image_url_ai} alt={product.name} className="w-full h-full object-cover" />
                            <div className="absolute top-4 left-4">
                                <Badge variant="secondary" className="bg-primary/90 text-primary-foreground backdrop-blur px-3 py-1 text-sm">
                                    ✨ AI Grade A
                                </Badge>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="aspect-video bg-muted rounded-lg overflow-hidden opacity-80 hover:opacity-100 transition-opacity">
                                <img src={product.image_url_raw} alt="Raw source" className="w-full h-full object-cover grayscale" />
                                <div className="p-2 text-xs absolute text-white font-bold drop-shadow-md">Original Scan</div>
                            </div>
                            {/* Placeholder for Map or Certificate */}
                            <div className="aspect-video bg-secondary/20 rounded-lg flex items-center justify-center text-sm font-medium text-primary">
                                📍 GPS Coordinates
                            </div>
                        </div>
                    </div>

                    {/* Right: Info & Action */}
                    <div className="space-y-8">
                        <div>
                            <Badge variant="outline" className="mb-2 border-primary/20 text-primary uppercase tracking-widest text-xs">
                                {product.origin}
                            </Badge>
                            <h1 className="text-4xl md:text-5xl font-serif font-bold text-primary mb-4 leading-tight">
                                {product.name}
                            </h1>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                <div className="flex items-center gap-1">
                                    <span>👨‍🌾</span>
                                    <span className="font-semibold text-foreground">{product.farmer_name}</span>
                                </div>
                                <div>•</div>
                                <div className="flex items-center gap-1">
                                    <span>📅</span>
                                    <span>Harvest: {product.harvest_date}</span>
                                </div>
                            </div>
                        </div>

                        <div className="p-6 bg-muted/30 rounded-xl border border-border">
                            <div className="flex items-baseline justify-between mb-2">
                                <span className="text-sm font-medium text-muted-foreground uppercase tracking-wide">FOB Price</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-bold text-primary">${product.price_fob}</span>
                                    <span className="text-sm text-muted-foreground">/ kg</span>
                                </div>
                            </div>
                            <Separator className="my-4" />
                            <div className="space-y-3">
                                <div className="flex justify-between text-sm">
                                    <span>Moisture Content</span>
                                    <span className="font-bold">{product.moisture_content}%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Vanillin Content</span>
                                    <span className="font-bold">{product.vanillin_content}%</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Available Quantity</span>
                                    <span className="font-bold">250 kg</span>
                                </div>
                            </div>

                            <div className="flex gap-4 mt-6">
                                <Button
                                    size="lg"
                                    variant="outline"
                                    className="flex-1 border-primary/20 text-primary font-semibold h-14"
                                    onClick={() => {
                                        // Demo Mode: Bypass Checks
                                        alert("Sample Requested! We will contact you shortly.");
                                    }}
                                >
                                    Request Sample
                                </Button>

                                <Button
                                    size="lg"
                                    className="flex-1 text-lg h-14 shadow-lg shadow-primary/20"
                                    onClick={() => {
                                        // Demo Mode: Bypass Checks
                                        // const token = localStorage.getItem("buyer_token");
                                        // const kyb = localStorage.getItem("kyb_status");

                                        // if (!token) { setShowSignupDialog(true); return; }
                                        // if (kyb !== "VALIDATED") { ... }

                                        const dialogTrigger = document.getElementById("offer-dialog-trigger");
                                        if (dialogTrigger) dialogTrigger.click();
                                    }}
                                >
                                    Make an Offer
                                </Button>
                            </div>

                            <Dialog>
                                <DialogTrigger asChild>
                                    <button id="offer-dialog-trigger" className="hidden">Open</button>
                                </DialogTrigger>
                                <DialogContent className="sm:max-w-[500px]">
                                    {!isOrderCreated ? (
                                        <>
                                            <DialogHeader>
                                                <DialogTitle className="font-serif text-2xl">Make an Offer</DialogTitle>
                                                <DialogDescription>
                                                    Negotiate directly for <strong>{product.name}</strong>.
                                                </DialogDescription>
                                            </DialogHeader>

                                            <div className="py-6 space-y-4">
                                                <div className="grid gap-2">
                                                    <Label htmlFor="price" className="text-sm font-medium">
                                                        Your Offer Price (Total USD for 10kg)
                                                    </Label>
                                                    <Input
                                                        id="price"
                                                        type="number"
                                                        value={offerPrice}
                                                        onChange={(e) => setOfferPrice(Number(e.target.value))}
                                                        className="text-lg font-semibold h-12"
                                                    />
                                                    <p className="text-xs text-muted-foreground">Based on $ {product.price_fob}/kg</p>
                                                </div>
                                            </div>
                                            <DialogFooter>
                                                <Button size="lg" className="w-full" onClick={handleConfirmOffer}>Confirm & Generate Contract</Button>
                                            </DialogFooter>
                                        </>
                                    ) : (
                                        <>
                                            <DialogHeader>
                                                <DialogTitle className="text-center font-serif text-2xl">Offer Accepted</DialogTitle>
                                            </DialogHeader>
                                            <div className="flex flex-col gap-3 py-6">
                                                <div className="bg-green-50 p-4 rounded text-center text-green-800 border border-green-100">
                                                    Contract Generated Successfully
                                                </div>
                                                <Button variant="outline" onClick={() => window.open(contractUrl!, '_blank')}>Download PDF</Button>
                                            </div>
                                        </>
                                    )}
                                </DialogContent>
                            </Dialog>
                        </div>

                        <div className="prose prose-stone max-w-none">
                            <h3 className="font-serif text-2xl font-bold mb-4">Product Story</h3>
                            <p className="leading-relaxed text-lg text-muted-foreground">
                                {product.description}
                            </p>
                            <p className="mt-4 leading-relaxed text-justify text-muted-foreground">
                                Harvested by the cooperative in the {product.origin}, this vanilla has undergone a traditional curing process of 6 months.
                                The beans are massaged daily to ensure optimal oil distribution.
                                Our AI grade analysis confirms zero mold and consistent sizing suitable for Gourmet grade export.
                            </p>
                        </div>

                        <Separator className="my-10" />

                        <div>
                            <h3 className="font-serif text-2xl font-bold mb-6">Live Traceability</h3>
                            <Timeline events={traceEvents} />
                        </div>

                    </div>
                </div >
            </main >
            <BuyerSignupDialog
                open={showSignupDialog}
                onOpenChange={setShowSignupDialog}
                onSuccess={() => alert("Welcome! Sample Request Sent.")}
            />
        </div >
    );
}
