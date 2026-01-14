import Link from 'next/link';
import { Product } from '@/lib/api';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { MapPin, Droplets, FlaskConical } from 'lucide-react';

interface ProductCardProps {
    product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
    // Safe defaults
    const moisture = product.moisture_content ?? 30.0;
    const vanillin = product.vanillin_content ?? 1.8;
    const region = product.origin || 'SAVA Region';

    return (
        <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300 border-border/50 group">
            <div className="relative aspect-[4/3] overflow-hidden">
                <img
                    src={product.image_url_ai || product.image_url_raw || 'https://placehold.co/600x400?text=Vanilla'}
                    alt={product.name}
                    className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-2 right-2 flex gap-1">
                    {product.status === 'SECURED' && (
                        <Badge variant="secondary" className="bg-orange-100 text-orange-800 hover:bg-orange-200">
                            Reserved
                        </Badge>
                    )}
                    <Badge variant="default" className="bg-green-600/90 backdrop-blur-sm">
                        Spot Deal
                    </Badge>
                </div>
            </div>

            <CardHeader className="p-4 pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <h3 className="font-bold text-lg text-primary line-clamp-1" title={product.name}>
                            {product.name}
                        </h3>
                        <div className="flex items-center text-muted-foreground text-sm mt-1">
                            <MapPin className="w-3 h-3 mr-1" />
                            {region}
                        </div>
                    </div>
                    <div className="text-right">
                        <span className="block text-xl font-bold text-primary">
                            ${product.price_fob}
                        </span>
                        <span className="text-xs text-muted-foreground">/ kg FOB</span>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="p-4 pt-2">
                <div className="grid grid-cols-2 gap-2 mt-2">
                    <div className="bg-muted/50 p-2 rounded-lg flex items-center justify-center gap-2" title="Moisture Content">
                        <Droplets className="w-4 h-4 text-blue-500" />
                        <span className="text-sm font-medium">{moisture.toFixed(1)}%</span>
                    </div>
                    <div className="bg-muted/50 p-2 rounded-lg flex items-center justify-center gap-2" title="Vanillin Content">
                        <FlaskConical className="w-4 h-4 text-purple-500" />
                        <span className="text-sm font-medium">{vanillin.toFixed(1)}%</span>
                    </div>
                </div>
            </CardContent>

            <CardFooter className="p-4 pt-0 gap-2">
                <Button asChild variant="outline" className="w-full">
                    <Link href={`/products/${product.id}`}>
                        Details
                    </Link>
                </Button>
                <Button className="w-full bg-primary hover:bg-primary/90">
                    Buy Now
                </Button>
            </CardFooter>
        </Card>
    );
}
