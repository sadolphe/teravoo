"use client";

import { useEffect, useState } from "react";
import { PriceTier, CalculatedPrice, calculatePrice } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface PriceTierGridProps {
  productId: number;
  basePriceFob: number;
  tiers: PriceTier[];
  moqKg?: number;
  quantityAvailable?: number;
  onQuantityChange?: (quantity: number, calculatedPrice: CalculatedPrice | null) => void;
  priceTrend?: {
    direction: 'up' | 'down' | 'stable';
    percent: number;
  };
}

export function PriceTierGrid({
  productId,
  basePriceFob,
  tiers,
  moqKg = 1,
  quantityAvailable = 500,
  onQuantityChange,
  priceTrend,
}: PriceTierGridProps) {
  const [quantity, setQuantity] = useState<number>(moqKg);
  const [calculatedPrice, setCalculatedPrice] = useState<CalculatedPrice | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  // Calculate price when quantity changes
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (quantity >= moqKg) {
        setIsCalculating(true);
        const result = await calculatePrice(productId, quantity);
        setCalculatedPrice(result);
        onQuantityChange?.(quantity, result);
        setIsCalculating(false);
      }
    }, 300); // Debounce

    return () => clearTimeout(timer);
  }, [quantity, productId, moqKg, onQuantityChange]);

  // Find active tier based on quantity
  const getActiveTierPosition = () => {
    if (!calculatedPrice?.tier_applied) return -1;
    return calculatedPrice.tier_applied.position;
  };

  const activeTierPosition = getActiveTierPosition();

  // Format quantity range for display
  const formatRange = (min: number, max: number | null) => {
    if (max === null) return `${min}+ kg`;
    return `${min} - ${max} kg`;
  };

  // If no tiers (SINGLE mode), show simple price
  if (!tiers || tiers.length === 0 || (tiers.length === 1 && tiers[0].discount_percent === 0)) {
    return (
      <div className="space-y-4">
        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-bold text-primary">${basePriceFob}</span>
          <span className="text-sm text-muted-foreground">/ kg (FOB)</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Price Trend Badge */}
      {priceTrend && priceTrend.direction !== 'stable' && (
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${
          priceTrend.direction === 'down'
            ? 'bg-green-100 text-green-800'
            : 'bg-orange-100 text-orange-800'
        }`}>
          {priceTrend.direction === 'down' ? '📉' : '📈'}
          Prix {priceTrend.direction === 'down' ? 'en baisse' : 'en hausse'} de {priceTrend.percent}%
        </div>
      )}

      {/* Tier Table */}
      <div className="border rounded-lg overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="font-semibold">Quantité</TableHead>
              <TableHead className="font-semibold">Prix/kg</TableHead>
              <TableHead className="font-semibold text-right">Économie</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tiers.map((tier, index) => {
              const isActive = tier.position === activeTierPosition;
              const savings = tier.discount_percent || 0;

              return (
                <TableRow
                  key={index}
                  className={`transition-colors ${isActive ? 'bg-primary/5 border-l-4 border-l-primary' : ''}`}
                >
                  <TableCell className="font-medium">
                    {formatRange(tier.min_quantity_kg, tier.max_quantity_kg)}
                    {isActive && (
                      <Badge variant="secondary" className="ml-2 text-xs">
                        Sélectionné
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <span className={`font-bold ${isActive ? 'text-primary text-lg' : ''}`}>
                      ${tier.price_per_kg.toFixed(2)}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    {savings > 0 ? (
                      <span className="text-green-600 font-semibold">
                        -{savings.toFixed(1)}%
                      </span>
                    ) : (
                      <span className="text-muted-foreground">Prix de base</span>
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* Quantity Input & Calculator */}
      <div className="p-4 bg-muted/30 rounded-lg border space-y-4">
        <div className="grid gap-2">
          <Label htmlFor="quantity" className="text-sm font-medium flex items-center justify-between">
            <span>Quantité souhaitée</span>
            <span className="text-xs text-muted-foreground">
              Disponible: {quantityAvailable} kg
            </span>
          </Label>
          <div className="flex gap-2">
            <Input
              id="quantity"
              type="number"
              min={moqKg}
              max={quantityAvailable}
              value={quantity}
              onChange={(e) => setQuantity(Math.max(moqKg, Number(e.target.value)))}
              className="text-lg font-semibold"
            />
            <span className="flex items-center text-muted-foreground px-3">kg</span>
          </div>
          {moqKg > 1 && (
            <p className="text-xs text-muted-foreground">
              Commande minimum: {moqKg} kg
            </p>
          )}
        </div>

        {/* Calculated Result */}
        {calculatedPrice && !isCalculating && (
          <div className="pt-4 border-t space-y-3">
            <div className="flex justify-between items-baseline">
              <span className="text-sm text-muted-foreground">Prix appliqué</span>
              <span className="text-lg font-bold text-primary">
                ${calculatedPrice.price_per_kg.toFixed(2)}/kg
              </span>
            </div>

            <div className="flex justify-between items-baseline">
              <span className="text-sm text-muted-foreground">Total</span>
              <span className="text-2xl font-bold text-primary">
                ${calculatedPrice.total.toLocaleString()}
              </span>
            </div>

            {calculatedPrice.savings_vs_base && calculatedPrice.savings_vs_base.amount > 0 && (
              <div className="flex justify-between items-center bg-green-50 text-green-800 px-3 py-2 rounded-md">
                <span className="text-sm font-medium">Vous économisez</span>
                <span className="font-bold">
                  ${calculatedPrice.savings_vs_base.amount.toLocaleString()} ({calculatedPrice.savings_vs_base.percent.toFixed(1)}%)
                </span>
              </div>
            )}

            {/* Next Tier Nudge */}
            {calculatedPrice.next_tier && (
              <div className="flex items-start gap-2 bg-blue-50 text-blue-800 px-3 py-2 rounded-md text-sm">
                <span className="text-lg">💡</span>
                <div>
                  <p className="font-medium">
                    Plus que {(calculatedPrice.next_tier.at_quantity_kg - quantity).toFixed(0)} kg pour ${calculatedPrice.next_tier.price_per_kg}/kg
                  </p>
                  <p className="text-xs opacity-80">
                    Économie supplémentaire: ${calculatedPrice.next_tier.extra_savings_total.toLocaleString()}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {isCalculating && (
          <div className="text-center py-4 text-muted-foreground">
            Calcul en cours...
          </div>
        )}
      </div>
    </div>
  );
}
