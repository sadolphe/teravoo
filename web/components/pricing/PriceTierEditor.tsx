"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface TierInput {
  min_quantity_kg: number;
  max_quantity_kg: number | null;
  price_per_kg: number;
}

interface PriceTierEditorProps {
  productId: number;
  productName: string;
  basePriceFob: number;
  currentMode: 'SINGLE' | 'TIERED' | 'TEMPLATE';
  currentTiers?: TierInput[];
  templates?: { id: number; name: string; tiers: any[] }[];
  currentTemplateId?: number;
  onSave: (mode: string, tiers?: TierInput[], templateId?: number) => Promise<void>;
  onCancel?: () => void;
}

export function PriceTierEditor({
  productId,
  productName,
  basePriceFob,
  currentMode,
  currentTiers = [],
  templates = [],
  currentTemplateId,
  onSave,
  onCancel,
}: PriceTierEditorProps) {
  const [mode, setMode] = useState<'SINGLE' | 'TIERED' | 'TEMPLATE'>(currentMode);
  const [tiers, setTiers] = useState<TierInput[]>(
    currentTiers.length > 0 ? currentTiers : [
      { min_quantity_kg: 1, max_quantity_kg: 49, price_per_kg: basePriceFob },
    ]
  );
  const [selectedTemplateId, setSelectedTemplateId] = useState<number | undefined>(currentTemplateId);
  const [isSaving, setIsSaving] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);

  // Validate tiers
  useEffect(() => {
    const newErrors: string[] = [];

    if (mode === 'TIERED') {
      // Check for contiguity
      const sortedTiers = [...tiers].sort((a, b) => a.min_quantity_kg - b.min_quantity_kg);

      for (let i = 1; i < sortedTiers.length; i++) {
        const prev = sortedTiers[i - 1];
        const curr = sortedTiers[i];

        // Check if prices are decreasing
        if (curr.price_per_kg > prev.price_per_kg) {
          newErrors.push(`Les prix doivent être décroissants (palier ${i + 1} > palier ${i})`);
        }
      }

      // Check for minimum tier
      if (tiers.length === 0) {
        newErrors.push('Au moins un palier est requis');
      }

      if (tiers.length > 5) {
        newErrors.push('Maximum 5 paliers autorisés');
      }
    }

    setErrors(newErrors);
  }, [tiers, mode]);

  const addTier = () => {
    if (tiers.length >= 5) return;

    const lastTier = tiers[tiers.length - 1];
    const newMinQty = lastTier ? (lastTier.max_quantity_kg || lastTier.min_quantity_kg) + 1 : 1;
    const newPrice = lastTier ? Math.round(lastTier.price_per_kg * 0.95 * 100) / 100 : basePriceFob;

    setTiers([
      ...tiers,
      {
        min_quantity_kg: newMinQty,
        max_quantity_kg: null,
        price_per_kg: newPrice,
      },
    ]);
  };

  const removeTier = (index: number) => {
    if (tiers.length <= 1) return;
    setTiers(tiers.filter((_, i) => i !== index));
  };

  const updateTier = (index: number, field: keyof TierInput, value: number | null) => {
    const newTiers = [...tiers];
    newTiers[index] = { ...newTiers[index], [field]: value };
    setTiers(newTiers);
  };

  const handleSave = async () => {
    if (errors.length > 0) return;

    setIsSaving(true);
    try {
      if (mode === 'SINGLE') {
        await onSave('SINGLE');
      } else if (mode === 'TIERED') {
        await onSave('TIERED', tiers);
      } else if (mode === 'TEMPLATE') {
        await onSave('TEMPLATE', undefined, selectedTemplateId);
      }
    } finally {
      setIsSaving(false);
    }
  };

  const calculateDiscount = (price: number) => {
    if (basePriceFob <= 0) return 0;
    return Math.round((1 - price / basePriceFob) * 100 * 10) / 10;
  };

  const previewTotal = (qty: number, price: number) => {
    return (qty * price).toFixed(2);
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <span>Configuration des Tarifs</span>
          <Badge variant="outline">{productName}</Badge>
        </CardTitle>
        <CardDescription>
          Prix de base: <strong>${basePriceFob}/kg</strong> — Choisissez votre stratégie tarifaire
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Mode Selection */}
        <div className="grid gap-4">
          <Label>Mode de tarification</Label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* SINGLE Mode */}
            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                mode === 'SINGLE'
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              }`}
              onClick={() => setMode('SINGLE')}
            >
              <div className="font-semibold mb-1">Prix Unique</div>
              <p className="text-sm text-muted-foreground">
                Un seul prix quelle que soit la quantité
              </p>
            </div>

            {/* TIERED Mode */}
            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                mode === 'TIERED'
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              }`}
              onClick={() => setMode('TIERED')}
            >
              <div className="font-semibold mb-1">Paliers Personnalisés</div>
              <p className="text-sm text-muted-foreground">
                Définissez vos propres paliers de prix
              </p>
            </div>

            {/* TEMPLATE Mode */}
            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                mode === 'TEMPLATE'
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              } ${templates.length === 0 ? 'opacity-50' : ''}`}
              onClick={() => templates.length > 0 && setMode('TEMPLATE')}
            >
              <div className="font-semibold mb-1">Utiliser un Template</div>
              <p className="text-sm text-muted-foreground">
                {templates.length > 0
                  ? `${templates.length} template(s) disponible(s)`
                  : 'Aucun template créé'}
              </p>
            </div>
          </div>
        </div>

        {/* TIERED Mode Editor */}
        {mode === 'TIERED' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label>Paliers tarifaires</Label>
              <Button
                variant="outline"
                size="sm"
                onClick={addTier}
                disabled={tiers.length >= 5}
              >
                + Ajouter un palier
              </Button>
            </div>

            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[80px]">Palier</TableHead>
                  <TableHead>Qté Min (kg)</TableHead>
                  <TableHead>Qté Max (kg)</TableHead>
                  <TableHead>Prix/kg ($)</TableHead>
                  <TableHead>Réduction</TableHead>
                  <TableHead className="w-[60px]"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tiers.map((tier, index) => (
                  <TableRow key={index}>
                    <TableCell className="font-medium">{index + 1}</TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min={1}
                        value={tier.min_quantity_kg}
                        onChange={(e) => updateTier(index, 'min_quantity_kg', Number(e.target.value))}
                        className="w-24"
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min={tier.min_quantity_kg}
                        value={tier.max_quantity_kg ?? ''}
                        placeholder="∞"
                        onChange={(e) =>
                          updateTier(
                            index,
                            'max_quantity_kg',
                            e.target.value ? Number(e.target.value) : null
                          )
                        }
                        className="w-24"
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min={0}
                        step={0.01}
                        value={tier.price_per_kg}
                        onChange={(e) => updateTier(index, 'price_per_kg', Number(e.target.value))}
                        className="w-28"
                      />
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={calculateDiscount(tier.price_per_kg) > 0 ? 'default' : 'secondary'}
                        className={calculateDiscount(tier.price_per_kg) > 0 ? 'bg-green-600' : ''}
                      >
                        {calculateDiscount(tier.price_per_kg) > 0
                          ? `-${calculateDiscount(tier.price_per_kg)}%`
                          : 'Base'}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeTier(index)}
                        disabled={tiers.length <= 1}
                        className="text-red-500 hover:text-red-700"
                      >
                        ×
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            {/* Preview */}
            <div className="p-4 bg-muted/50 rounded-lg">
              <div className="text-sm font-medium mb-2">Aperçu pour l'acheteur</div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                {tiers.map((tier, index) => (
                  <div key={index} className="p-2 bg-background rounded border">
                    <div className="text-muted-foreground text-xs">
                      {tier.max_quantity_kg ? `${tier.min_quantity_kg}-${tier.max_quantity_kg}` : `${tier.min_quantity_kg}+`} kg
                    </div>
                    <div className="font-bold">${tier.price_per_kg}/kg</div>
                    <div className="text-xs text-muted-foreground">
                      Ex: {tier.min_quantity_kg}kg = ${previewTotal(tier.min_quantity_kg, tier.price_per_kg)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TEMPLATE Mode Selector */}
        {mode === 'TEMPLATE' && templates.length > 0 && (
          <div className="space-y-4">
            <Label>Sélectionner un template</Label>
            <Select
              value={selectedTemplateId?.toString()}
              onValueChange={(v) => setSelectedTemplateId(Number(v))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Choisir un template..." />
              </SelectTrigger>
              <SelectContent>
                {templates.map((template) => (
                  <SelectItem key={template.id} value={template.id.toString()}>
                    {template.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Template Preview */}
            {selectedTemplateId && (
              <div className="p-4 bg-muted/50 rounded-lg">
                <div className="text-sm font-medium mb-2">Aperçu du template</div>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Quantité</TableHead>
                      <TableHead>Réduction</TableHead>
                      <TableHead>Prix calculé</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {templates
                      .find((t) => t.id === selectedTemplateId)
                      ?.tiers.map((tier: any, index: number) => (
                        <TableRow key={index}>
                          <TableCell>
                            {tier.max_quantity_kg
                              ? `${tier.min_quantity_kg}-${tier.max_quantity_kg} kg`
                              : `${tier.min_quantity_kg}+ kg`}
                          </TableCell>
                          <TableCell>
                            <Badge variant={tier.discount_percent > 0 ? 'default' : 'secondary'}>
                              {tier.discount_percent > 0 ? `-${tier.discount_percent}%` : 'Base'}
                            </Badge>
                          </TableCell>
                          <TableCell className="font-bold">
                            ${(basePriceFob * (1 - tier.discount_percent / 100)).toFixed(2)}/kg
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>
        )}

        {/* Errors */}
        {errors.length > 0 && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="font-medium text-red-800 mb-2">Erreurs de validation</div>
            <ul className="list-disc list-inside text-sm text-red-700">
              {errors.map((error, i) => (
                <li key={i}>{error}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-end gap-4 pt-4 border-t">
          {onCancel && (
            <Button variant="outline" onClick={onCancel}>
              Annuler
            </Button>
          )}
          <Button
            onClick={handleSave}
            disabled={isSaving || errors.length > 0 || (mode === 'TEMPLATE' && !selectedTemplateId)}
          >
            {isSaving ? 'Enregistrement...' : 'Enregistrer'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
