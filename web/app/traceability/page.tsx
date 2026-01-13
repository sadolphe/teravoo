"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Search } from "lucide-react";

export default function TraceabilityPage() {
    const [orderId, setOrderId] = useState("");
    const router = useRouter();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (orderId) {
            router.push(`/orders/${orderId}/traceability`);
        }
    };

    const handleDemo = () => {
        router.push("/orders/123/traceability");
    };

    return (
        <div className="container mx-auto px-6 py-20 flex flex-col items-center justify-center min-h-[80vh]">
            <div className="text-center max-w-2xl mb-12">
                <h1 className="text-4xl font-serif font-bold text-primary mb-4">Track Your Shipment</h1>
                <p className="text-muted-foreground text-lg">
                    Enter your Order ID to view the complete blockchain-verified history of your vanilla, from the vine to your warehouse.
                </p>
            </div>

            <Card className="w-full max-w-md shadow-xl border-primary/10">
                <CardHeader>
                    <CardTitle>Traceability Search</CardTitle>
                    <CardDescription>Enter the ID found on your Sales Agreement.</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSearch} className="flex gap-2">
                        <Input
                            placeholder="Order ID (e.g. 123)"
                            value={orderId}
                            onChange={(e) => setOrderId(e.target.value)}
                            className="flex-1"
                        />
                        <Button type="submit" disabled={!orderId}>
                            <Search className="w-4 h-4 mr-2" />
                            Track
                        </Button>
                    </form>

                    <div className="mt-8 pt-6 border-t border-border/50 text-center">
                        <p className="text-sm text-muted-foreground mb-4">No order yet? Try our live demo.</p>
                        <Button variant="outline" className="w-full" onClick={handleDemo}>
                            View Demo Timeline (Order #123)
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
