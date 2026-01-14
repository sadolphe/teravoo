'use client';

import { useEffect, useState } from 'react';
import { getProducts, Product } from '@/lib/api';
import { ProductCard } from '@/components/marketplace/ProductCard';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, SlidersHorizontal } from 'lucide-react';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";


export default function MarketplacePage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [regionFilter, setRegionFilter] = useState('ALL');

    useEffect(() => {
        async function fetchProducts() {
            try {
                const data = await getProducts();
                setProducts(data);
                setFilteredProducts(data);
            } catch (error) {
                console.error('Failed to load products', error);
            } finally {
                setLoading(false);
            }
        }
        fetchProducts();
    }, []);

    useEffect(() => {
        let result = products;

        // Search Filter
        if (searchQuery) {
            const lowerQuery = searchQuery.toLowerCase();
            result = result.filter(p =>
                p.name.toLowerCase().includes(lowerQuery) ||
                (p.origin || '').toLowerCase().includes(lowerQuery)
            );
        }

        // Region Filter (Mocking regions for now based on origin string)
        if (regionFilter !== 'ALL') {
            result = result.filter(p => (p.origin || "SAVA").toUpperCase().includes(regionFilter));
        }

        setFilteredProducts(result);
    }, [searchQuery, regionFilter, products]);


    if (loading) {
        return (
            <div className="container mx-auto py-12 px-4 flex justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Hero Section */}
            <section className="relative bg-primary text-primary-foreground py-24 md:py-32 overflow-hidden">
                {/* Abstract Background Shapes */}
                <div className="absolute inset-0 opacity-10 pointer-events-none">
                    <div className="absolute top-0 right-0 w-96 h-96 bg-secondary rounded-full blur-3xl translate-x-1/2 -translate-y-1/2"></div>
                    <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary rounded-full blur-3xl -translate-x-1/2 translate-y-1/2"></div>
                </div>

                <div className="container mx-auto px-6 relative z-10 text-center">
                    <h1 className="text-5xl md:text-6xl font-serif font-bold mb-6">Spot Connections</h1>
                    <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto text-center leading-relaxed font-light">
                        Access verified vanilla lots directly from Malagasy producer cooperatives.
                        Traceable, graded, and ready for export.
                    </p>
                </div>
            </section>

            <div className="container mx-auto px-4 py-8">
                {/* Filters Bar */}
                <div className="flex flex-col md:flex-row gap-4 mb-8 items-center bg-card p-4 rounded-xl shadow-sm border">
                    <div className="relative flex-1 w-full">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground w-4 h-4" />
                        <Input
                            placeholder="Search by name, origin, or grade..."
                            className="pl-9 bg-background"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    <div className="flex gap-2 w-full md:w-auto">
                        <Select value={regionFilter} onValueChange={setRegionFilter}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Region" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="ALL">All Regions</SelectItem>
                                <SelectItem value="SAVA">SAVA Region</SelectItem>
                                <SelectItem value="DIANA">Diana Region</SelectItem>
                                <SelectItem value="ANALANJIROFO">Analanjirofo</SelectItem>
                            </SelectContent>
                        </Select>

                        <Button variant="outline" className="gap-2">
                            <SlidersHorizontal className="w-4 h-4" />
                            Filters
                        </Button>
                    </div>
                </div>

                {/* Results Grid */}
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-semibold text-primary">
                            Available Lots <span className="text-muted-foreground ml-2 text-base font-normal">({filteredProducts.length})</span>
                        </h2>
                    </div>

                    {filteredProducts.length === 0 ? (
                        <div className="text-center py-20 bg-muted/20 rounded-xl">
                            <p className="text-xl text-muted-foreground">No products found for your search.</p>
                            <Button variant="link" onClick={() => { setSearchQuery(''); setRegionFilter('ALL'); }}>Clear Filters</Button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {filteredProducts.map(product => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
