"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getProducts, createOrder, Product } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator"; // A beautiful separator would be nice if installed, or just HR

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [offerPrice, setOfferPrice] = useState<number>(0);
  const [isOrderCreated, setIsOrderCreated] = useState(false);
  const [contractUrl, setContractUrl] = useState<string | null>(null);
  const [isPaid, setIsPaid] = useState(false);
  const [isRejected, setIsRejected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [orderId, setOrderId] = useState<number | null>(null);


  useEffect(() => {
    getProducts().then(setProducts);
  }, []);

  const handleOpenOffer = (product: Product) => {
    setSelectedProduct(product);
    setOfferPrice(product.price_fob * 10); // Default 10kg
    setIsOrderCreated(false);
    setIsPaid(false);
    setIsRejected(false);
    setOrderId(null);
  };

  const handleConfirmOffer = async () => {
    if (!selectedProduct) return;

    // 1. Negotiation Logic (Simple Rule: Reject if < 85% of default price)
    const targetPrice = selectedProduct.price_fob * 10;
    const minAcceptablePrice = targetPrice * 0.85;

    if (offerPrice < minAcceptablePrice) {
      setIsRejected(true);
      return;
    }

    setIsLoading(true);
    try {
      const order = await createOrder(selectedProduct.id, offerPrice);
      setOrderId(order.id);

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const contractPath = `/orders/${order.id}/contract`;
      await fetch(`${API_URL}${contractPath}`, { method: 'POST' });

      setIsOrderCreated(true);
      setContractUrl(`${API_URL}/orders/${order.id}/download_contract`);
    } catch (e) {
      alert("Error creating order");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePayment = async () => {
    if (!orderId) return;
    setIsLoading(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    try {
      await fetch(`${API_URL}/orders/${orderId}/pay`, { method: 'POST' });
      setIsPaid(true);
    } catch (e) {
      alert("Payment failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      {/* Hero Section */}
      <section className="relative bg-primary text-primary-foreground py-24 md:py-32 overflow-hidden">
        {/* Abstract Background Shapes */}
        <div className="absolute inset-0 opacity-10 pointer-events-none">
          <div className="absolute top-0 right-0 w-96 h-96 bg-secondary rounded-full blur-3xl translate-x-1/2 -translate-y-1/2"></div>
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary rounded-full blur-3xl -translate-x-1/2 translate-y-1/2"></div>
        </div>

        <div className="container mx-auto px-6 relative z-10 text-center">
          <Badge variant="secondary" className="mb-6 px-4 py-1 text-sm font-medium uppercase tracking-widest bg-secondary/20 text-secondary-foreground border-none">
            Direct Trade • 2025 Harvest
          </Badge>
          <h1 className="text-5xl md:text-7xl font-serif font-bold mb-6 leading-tight">
            The World's Finest Vanilla.<br />
            <span className="text-secondary opacity-90">Straight from the Source.</span>
          </h1>
          <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
            TeraVoo connects you directly with audited producers in Madagascar.
            No middlemen. AI-verified quality. Secured payments.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/products">
              <Button size="lg" className="text-lg h-14 px-8 bg-secondary text-primary hover:bg-white transition-all transform hover:scale-105">View Marketplace</Button>
            </Link>
            <Button size="lg" className="text-lg h-14 px-8 bg-transparent border border-white/20 text-white hover:bg-white/10 transition-all" onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}>How it Works</Button>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-16 bg-muted/50 border-b border-border">
        <div className="container mx-auto px-6 grid md:grid-cols-3 gap-8 text-center">
          <div className="p-6">
            <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">🌍</div>
            <h3 className="text-lg font-bold mb-2">100% Direct Trade</h3>
            <p className="text-muted-foreground text-sm">We cut out the 5-7 middlemen. Farmers earn more, you pay less.</p>
          </div>
          <div className="p-6">
            <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">✨</div>
            <h3 className="text-lg font-bold mb-2">AI Grading Quality</h3>
            <p className="text-muted-foreground text-sm">Every batch is scanned and graded by our proprietary AI Vision tech.</p>
          </div>
          <div className="p-6">
            <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">🔒</div>
            <h3 className="text-lg font-bold mb-2">Secure Escrow</h3>
            <p className="text-muted-foreground text-sm">Your funds are held safely until you receive and validate the goods.</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-background">
        <div className="container mx-auto px-6 text-center">
          <Badge variant="outline" className="mb-4 border-primary/20 text-primary uppercase tracking-widest">The Process</Badge>
          <h2 className="text-4xl font-serif font-bold text-primary mb-16">Sourcing Made Simple</h2>

          <div className="grid md:grid-cols-4 gap-8 relative">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-24 left-0 w-full h-0.5 bg-gradient-to-r from-primary/10 via-primary/30 to-primary/10 -z-10"></div>

            <div className="relative group">
              <div className="w-16 h-16 mx-auto bg-background border-2 border-primary/20 rounded-full flex items-center justify-center text-xl font-bold text-primary mb-6 group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300 z-10">1</div>
              <img src="https://placehold.co/400x300/e6e6e6/1a1a1a?text=Source" className="w-full h-40 object-cover rounded-lg mb-4 opacity-80" />
              <h3 className="text-xl font-bold mb-2">Browse & Select</h3>
              <p className="text-muted-foreground text-sm">Explore real-time lots uploaded directly by producers with AI-verified specs.</p>
            </div>

            <div className="relative group">
              <div className="w-16 h-16 mx-auto bg-background border-2 border-primary/20 rounded-full flex items-center justify-center text-xl font-bold text-primary mb-6 group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300 z-10">2</div>
              <img src="https://placehold.co/400x300/e6e6e6/1a1a1a?text=Offer" className="w-full h-40 object-cover rounded-lg mb-4 opacity-80" />
              <h3 className="text-xl font-bold mb-2">Make an Offer</h3>
              <p className="text-muted-foreground text-sm">Negotiate price directly. Once accepted, a Smart Contract is auto-generated.</p>
            </div>

            <div className="relative group">
              <div className="w-16 h-16 mx-auto bg-background border-2 border-primary/20 rounded-full flex items-center justify-center text-xl font-bold text-primary mb-6 group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300 z-10">3</div>
              <img src="https://placehold.co/400x300/e6e6e6/1a1a1a?text=Secure" className="w-full h-40 object-cover rounded-lg mb-4 opacity-80" />
              <h3 className="text-xl font-bold mb-2">Secure Funds</h3>
              <p className="text-muted-foreground text-sm">Pay into our secure Escrow. Funds are released only after shipping verification.</p>
            </div>

            <div className="relative group">
              <div className="w-16 h-16 mx-auto bg-background border-2 border-primary/20 rounded-full flex items-center justify-center text-xl font-bold text-primary mb-6 group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300 z-10">4</div>
              <img src="https://placehold.co/400x300/e6e6e6/1a1a1a?text=Ship" className="w-full h-40 object-cover rounded-lg mb-4 opacity-80" />
              <h3 className="text-xl font-bold mb-2">Receive & Validate</h3>
              <p className="text-muted-foreground text-sm">Goods are shipped. You validate quality on arrival. Deal closed.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Product Grid */}
      <main id="marketplace" className="container mx-auto px-6 py-20">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h2 className="text-3xl font-serif font-bold text-primary mb-2">Curated Selection</h2>
            <p className="text-muted-foreground">Available for immediate shipping from Toamasina.</p>
          </div>
          <Button variant="outline">View All Lots</Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((product) => (
            <Card key={product.id} className="group overflow-hidden border-none shadow-lg hover:shadow-xl transition-all duration-300 bg-card">
              <div className="relative aspect-[4/3] bg-muted overflow-hidden">
                <img
                  src={product.image_url_ai || product.image_url_raw || 'https://placehold.co/600x400/e6e6e6/1a1a1a?text=Vanilla+Beans'}
                  alt={product.name}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                <div className="absolute top-4 right-4 flex gap-2">
                  <Badge className="bg-white/90 text-primary backdrop-blur shadow-sm hover:bg-white">
                    {product.origin?.split(',')[0]}
                  </Badge>
                </div>
                {/* AI Badge Overlay on bottom left */}
                <div className="absolute bottom-4 left-4">
                  <Badge variant="secondary" className="bg-primary/90 text-primary-foreground backdrop-blur shadow-sm">
                    ✨ AI Grade A
                  </Badge>
                </div>
              </div>

              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-xl font-serif font-semibold">{product.name}</CardTitle>
                    <CardDescription className="mt-1 flex items-center gap-1">
                      By {product.farmer_name || "Unknown"}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-3xl font-bold text-primary">${product.price_fob}</span>
                  <span className="text-sm text-muted-foreground font-medium uppercase tracking-wide">/ kg (FOB)</span>
                </div>

                {/* Micro Specs */}
                <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground bg-muted/30 p-3 rounded-lg">
                  <div className="flex flex-col">
                    <span className="text-xs uppercase tracking-wider opacity-70">Moisture</span>
                    <span className="font-semibold text-foreground">{product.moisture_content}%</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs uppercase tracking-wider opacity-70">Vanillin</span>
                    <span className="font-semibold text-foreground">{product.vanillin_content}%</span>
                  </div>
                </div>

                <p className="mt-4 text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                  {product.description}
                </p>
              </CardContent>

              <CardFooter className="gap-3 pt-2">
                <Link href={`/products/${product.id}`} className="flex-1">
                  <Button className="w-full" variant="outline">Details</Button>
                </Link>

                <Dialog>
                  <DialogTrigger asChild>
                    <Button className="flex-1 shadow-md shadow-primary/10" onClick={() => handleOpenOffer(product)}>Make Offer</Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[500px]">
                    {isRejected ? (
                      <>
                        <DialogHeader>
                          <div className="mx-auto w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-xl mb-2">✕</div>
                          <DialogTitle className="text-center font-serif text-2xl">Offer Declined</DialogTitle>
                          <DialogDescription className="text-center">
                            The producer cannot accept an offer this low.
                          </DialogDescription>
                        </DialogHeader>
                        <div className="py-6 text-center space-y-4">
                          <p className="text-sm text-muted-foreground">
                            The bid is too far below the market price for this quality (AI Grade A).
                            Please respect our partners' fair trade value.
                          </p>
                          <Button size="lg" className="w-full bg-secondary text-primary hover:bg-secondary/90" onClick={() => setIsRejected(false)}>Make a Fair Offer</Button>
                        </div>
                      </>
                    ) : !isOrderCreated ? (
                      <>
                        <DialogHeader>
                          <DialogTitle className="font-serif text-2xl">Make an Offer</DialogTitle>
                          <DialogDescription>
                            Negotiate directly with <strong>{selectedProduct?.farmer_name}</strong>.
                          </DialogDescription>
                        </DialogHeader>

                        <div className="py-6 space-y-6">
                          <div className="p-4 bg-muted/50 rounded-lg flex gap-4 items-center">
                            <div className="h-16 w-16 bg-gray-200 rounded-md overflow-hidden shrink-0">
                              <img src={selectedProduct?.image_url_ai || selectedProduct?.image_url_raw || 'https://placehold.co/100x100/e6e6e6/1a1a1a?text=Vanilla'} className="w-full h-full object-cover" />
                            </div>
                            <div>
                              <h4 className="font-semibold">{selectedProduct?.name}</h4>
                              <p className="text-sm text-muted-foreground">Lot of 10kg • Grade A</p>
                            </div>
                          </div>

                          <div className="grid gap-2">
                            <Label htmlFor="price" className="text-sm font-medium">
                              Your Offer Price (Total USD)
                            </Label>
                            <div className="relative">
                              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">$</span>
                              <Input
                                id="price"
                                type="number"
                                value={offerPrice}
                                onChange={(e) => setOfferPrice(Number(e.target.value))}
                                className="pl-8 text-lg font-semibold h-12"
                              />
                            </div>
                            <p className="text-xs text-muted-foreground">Recommended range: ${selectedProduct ? selectedProduct.price_fob * 10 * 0.9 : 0} - ${selectedProduct ? selectedProduct.price_fob * 10 * 1.1 : 0}</p>
                          </div>
                        </div>
                        <DialogFooter>
                          <Button size="lg" className="w-full" onClick={handleConfirmOffer}>Confirm & Generate Contract</Button>
                        </DialogFooter>
                      </>
                    ) : !isPaid ? (
                      <>
                        <DialogHeader>
                          <div className="mx-auto w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl mb-2">✓</div>
                          <DialogTitle className="text-center font-serif text-2xl">Offer Accepted</DialogTitle>
                          <DialogDescription className="text-center">
                            The producer has accepted your offer. The Smart Contract is ready.
                          </DialogDescription>
                        </DialogHeader>

                        <div className="flex flex-col gap-3 py-6">
                          <div className="border border-border p-4 rounded-lg flex justify-between items-center bg-card">
                            <div className="flex items-center gap-3">
                              <div className="h-10 w-8 bg-red-50 border border-red-100 flex items-center justify-center rounded text-red-500 text-xs font-bold">PDF</div>
                              <div className="text-sm font-medium">Sales_Agreement_#{Math.floor(Math.random() * 1000)}.pdf</div>
                            </div>
                            <Button variant="ghost" size="sm" onClick={() => window.open(contractUrl!, '_blank')}>Download</Button>
                          </div>

                          <Button size="lg" className="w-full mt-2" onClick={handlePayment} disabled={isLoading}>
                            {isLoading ? "Processing..." : "Proceed to Escrow Payment"}
                          </Button>
                        </div>
                      </>
                    ) : (
                      <>
                        <DialogHeader>
                          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-600 text-white rounded-full flex items-center justify-center text-3xl mb-4 shadow-lg shadow-green-500/30">🎉</div>
                          <DialogTitle className="text-center font-serif text-2xl">Funds Secured!</DialogTitle>
                          <DialogDescription className="text-center">
                            Your payment is held safely in the Smart Escrow.
                          </DialogDescription>
                        </DialogHeader>
                        <div className="py-6 text-center space-y-4">
                          <p className="text-sm text-muted-foreground">The producer has been notified to start shipping. You will be alerted when the goods arrive for validation.</p>
                          <div className="p-4 bg-muted/30 rounded-lg text-sm font-mono text-xs text-muted-foreground break-all">
                            Escrow_Tx: 0x71C...9A23 • Status: LOCKED
                          </div>
                          <DialogClose asChild>
                            <Button size="lg" className="w-full" onClick={() => setIsOrderCreated(false)}>Close & Track Order</Button>
                          </DialogClose>
                        </div>
                      </>
                    )}
                  </DialogContent>
                </Dialog>

              </CardFooter>
            </Card>
          ))}
        </div>
      </main >

      {/* Footer */}
      < footer className="bg-primary text-primary-foreground py-12 mt-12" >
        <div className="container mx-auto px-6 grid md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="font-serif text-2xl font-bold mb-4">TeraVoo</div>
            <p className="opacity-80 max-w-sm">The 1st trusted marketplace for direct vanilla sourcing. Empowering farmers, securing buyers.</p>
          </div>
          <div>
            <h4 className="font-bold mb-4">Platform</h4>
            <ul className="space-y-2 opacity-80 text-sm">
              <li>Marketplace</li>
              <li>Pricing</li>
              <li>Logistics</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Legal</h4>
            <ul className="space-y-2 opacity-80 text-sm">
              <li>Terms of Sale</li>
              <li>Escrow Agreement</li>
              <li>Quality Charts</li>
            </ul>
          </div>
        </div>
        <div className="container mx-auto px-6 mt-12 pt-8 border-t border-white/20 text-center opacity-60 text-sm">
          © 2025 TeraVoo Inc. All rights reserved.
        </div>
      </footer >
    </div >
  );
}
