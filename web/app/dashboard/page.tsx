"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getOrders, Order } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

export default function Dashboard() {
    const [orders, setOrders] = useState<Order[]>([]);

    useEffect(() => {
        getOrders().then(setOrders);
    }, []);

    return (
        <div className="min-h-screen bg-background font-sans text-foreground">
            <main className="container mx-auto px-6 py-12">
                <div className="flex gap-4 mb-8">
                    <Button variant="default">My Orders</Button>
                    <Button variant="outline" onClick={() => window.location.href = '/dashboard/requests'}>Sourcing Requests (RFP)</Button>
                </div>

                <h1 className="text-3xl font-serif font-bold text-primary mb-8">My Orders</h1>

                {orders.length === 0 ? (
                    <div className="text-center py-20 bg-muted/30 rounded-lg">
                        <p className="text-muted-foreground mb-4">No active orders found.</p>
                        <Button onClick={() => window.location.href = '/'}>Browse Marketplace</Button>
                    </div>
                ) : (
                    <div className="grid gap-6">
                        {orders.map((order) => (
                            <Card key={order.id} className="flex flex-col md:flex-row items-center justify-between p-2">
                                <CardHeader className="flex-1">
                                    <div className="flex items-center gap-4 mb-2">
                                        <Badge variant={order.status === 'SECURED' ? 'default' : 'secondary'}>
                                            {order.status}
                                        </Badge>
                                        <span className="text-xs text-muted-foreground">Order #{order.id}</span>
                                    </div>
                                    <Link href={`/products/${order.product_id}`} className="hover:underline">
                                        <CardTitle className="text-lg">{order.product_name}</CardTitle>
                                    </Link>
                                    <CardDescription>Target: 10kg • Delivery to Toamasina</CardDescription>
                                </CardHeader>
                                <CardContent className="flex items-center gap-8 md:pr-8 py-4 md:py-0 w-full md:w-auto">
                                    <div className="text-right">
                                        <div className="text-sm text-muted-foreground">Total Value</div>
                                        <div className="text-xl font-bold text-primary">${order.amount}</div>
                                    </div>
                                    <div className="flex flex-col gap-2 min-w-[140px]">
                                        {order.contract_url ? (
                                            <Button size="sm" variant="outline" onClick={() => window.open(order.contract_url, '_blank')}>
                                                📄 Download Contract
                                            </Button>
                                        ) : (
                                            <span className="text-xs text-muted-foreground text-center">No contract yet</span>
                                        )}

                                        {order.status === 'SECURED' ? (
                                            <Badge className="bg-green-100 text-green-800 hover:bg-green-100 text-center justify-center">
                                                Funds Hosted
                                            </Badge>
                                        ) : (
                                            <Button size="sm" disabled={!order.contract_url}>
                                                Pay to Escrow
                                            </Button>
                                        )}
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
