"use client";

import { useEffect, useState } from "react";
import {
  getProducts,
  Product,
  getProductPriceTiers,
  setProductPriceTiers,
  updateProductPricingMode,
  getProducerTemplates,
  createProducerTemplate,
  PriceTierTemplate,
  ProductPricingInfo,
} from "@/lib/api";
import { PriceTierEditor } from "@/components/pricing/PriceTierEditor";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import {
  Card,
  CardContent,
  CardDescription,
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
} from "@/components/ui/dialog";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";

// Mock producer ID for MVP
const MOCK_PRODUCER_ID = 1;

export default function ProducerPricingPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [templates, setTemplates] = useState<PriceTierTemplate[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productPricing, setProductPricing] = useState<ProductPricingInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showTemplateDialog, setShowTemplateDialog] = useState(false);

  // Template creation form
  const [newTemplateName, setNewTemplateName] = useState("");
  const [newTemplateTiers, setNewTemplateTiers] = useState([
    { min_quantity_kg: 1, max_quantity_kg: 49, discount_percent: 0 },
    { min_quantity_kg: 50, max_quantity_kg: 199, discount_percent: 5 },
    { min_quantity_kg: 200, max_quantity_kg: null, discount_percent: 10 },
  ]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [productsData, templatesData] = await Promise.all([
        getProducts(),
        getProducerTemplates(MOCK_PRODUCER_ID),
      ]);
      setProducts(productsData);
      setTemplates(templatesData);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectProduct = async (product: Product) => {
    setSelectedProduct(product);
    const pricing = await getProductPriceTiers(product.id);
    setProductPricing(pricing);
  };

  const handleSaveProductPricing = async (
    mode: string,
    tiers?: { min_quantity_kg: number; max_quantity_kg: number | null; price_per_kg: number }[],
    templateId?: number
  ) => {
    if (!selectedProduct) return;

    try {
      if (mode === 'TIERED' && tiers) {
        await setProductPriceTiers(selectedProduct.id, tiers);
      } else {
        await updateProductPricingMode(selectedProduct.id, mode, templateId);
      }

      // Refresh pricing info
      const pricing = await getProductPriceTiers(selectedProduct.id);
      setProductPricing(pricing);

      // Refresh products list
      await loadData();
    } catch (error) {
      console.error('Error saving pricing:', error);
      alert('Erreur lors de la sauvegarde');
    }
  };

  const handleCreateTemplate = async () => {
    if (!newTemplateName.trim()) return;

    try {
      await createProducerTemplate(MOCK_PRODUCER_ID, {
        name: newTemplateName,
        is_default: templates.length === 0,
        tiers: newTemplateTiers,
      });

      // Refresh templates
      const templatesData = await getProducerTemplates(MOCK_PRODUCER_ID);
      setTemplates(templatesData);

      // Reset form
      setNewTemplateName("");
      setShowTemplateDialog(false);
    } catch (error) {
      console.error('Error creating template:', error);
      alert('Erreur lors de la création du template');
    }
  };

  const getPricingModeLabel = (mode?: string) => {
    switch (mode) {
      case 'TIERED':
        return { label: 'Paliers', color: 'bg-green-600' };
      case 'TEMPLATE':
        return { label: 'Template', color: 'bg-blue-600' };
      default:
        return { label: 'Prix unique', color: 'bg-gray-500' };
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      {/* Header */}
      <header className="sticky top-0 z-20 w-full backdrop-blur-md bg-background/80 border-b border-border">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="font-serif text-xl font-bold text-primary cursor-pointer" onClick={() => window.location.href = '/'}>
            TeraVoo
          </div>
          <div className="flex items-center gap-4">
            <Badge variant="outline">Producteur Dashboard</Badge>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-serif font-bold text-primary mb-2">Gestion des Tarifs</h1>
          <p className="text-muted-foreground">
            Configurez vos paliers tarifaires pour encourager les achats en volume
          </p>
        </div>

        <Tabs defaultValue="products" className="space-y-6">
          <TabsList>
            <TabsTrigger value="products">Mes Produits</TabsTrigger>
            <TabsTrigger value="templates">Mes Templates</TabsTrigger>
          </TabsList>

          {/* Products Tab */}
          <TabsContent value="products" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              {/* Products List */}
              <div className="md:col-span-1 space-y-4">
                <h2 className="font-semibold text-lg">Sélectionner un produit</h2>
                <div className="space-y-3">
                  {products.map((product) => {
                    const modeInfo = getPricingModeLabel(product.pricing_mode);
                    return (
                      <Card
                        key={product.id}
                        className={`cursor-pointer transition-all hover:shadow-md ${
                          selectedProduct?.id === product.id ? 'ring-2 ring-primary' : ''
                        }`}
                        onClick={() => handleSelectProduct(product)}
                      >
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between gap-2">
                            <div className="flex-1 min-w-0">
                              <h3 className="font-medium truncate">{product.name}</h3>
                              <p className="text-sm text-muted-foreground">
                                ${product.price_fob}/kg
                              </p>
                            </div>
                            <Badge className={modeInfo.color}>
                              {modeInfo.label}
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}

                  {products.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                      Aucun produit trouvé
                    </div>
                  )}
                </div>
              </div>

              {/* Editor */}
              <div className="md:col-span-2">
                {selectedProduct ? (
                  <PriceTierEditor
                    productId={selectedProduct.id}
                    productName={selectedProduct.name}
                    basePriceFob={selectedProduct.price_fob}
                    currentMode={(productPricing?.pricing_mode as 'SINGLE' | 'TIERED' | 'TEMPLATE') || 'SINGLE'}
                    currentTiers={productPricing?.tiers?.map(t => ({
                      min_quantity_kg: t.min_quantity_kg,
                      max_quantity_kg: t.max_quantity_kg,
                      price_per_kg: t.price_per_kg,
                    }))}
                    templates={templates}
                    currentTemplateId={productPricing?.template_id}
                    onSave={handleSaveProductPricing}
                  />
                ) : (
                  <Card className="h-full flex items-center justify-center min-h-[400px]">
                    <CardContent className="text-center">
                      <div className="text-4xl mb-4">👈</div>
                      <p className="text-muted-foreground">
                        Sélectionnez un produit pour configurer ses tarifs
                      </p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Templates Tab */}
          <TabsContent value="templates" className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-lg">Templates de paliers</h2>
                <p className="text-sm text-muted-foreground">
                  Créez des templates réutilisables pour vos produits
                </p>
              </div>
              <Dialog open={showTemplateDialog} onOpenChange={setShowTemplateDialog}>
                <DialogTrigger asChild>
                  <Button>+ Créer un template</Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Nouveau Template de Paliers</DialogTitle>
                    <DialogDescription>
                      Définissez des réductions en pourcentage qui s'appliqueront au prix de base de chaque produit
                    </DialogDescription>
                  </DialogHeader>

                  <div className="space-y-4 py-4">
                    <div className="grid gap-2">
                      <Label htmlFor="template-name">Nom du template</Label>
                      <Input
                        id="template-name"
                        value={newTemplateName}
                        onChange={(e) => setNewTemplateName(e.target.value)}
                        placeholder="Ex: Paliers Standard"
                      />
                    </div>

                    <Separator />

                    <div className="space-y-3">
                      <Label>Paliers de réduction</Label>
                      {newTemplateTiers.map((tier, index) => (
                        <div key={index} className="flex items-center gap-3">
                          <div className="flex-1 grid grid-cols-3 gap-2">
                            <div>
                              <Label className="text-xs">Min (kg)</Label>
                              <Input
                                type="number"
                                value={tier.min_quantity_kg}
                                onChange={(e) => {
                                  const updated = [...newTemplateTiers];
                                  updated[index].min_quantity_kg = Number(e.target.value);
                                  setNewTemplateTiers(updated);
                                }}
                              />
                            </div>
                            <div>
                              <Label className="text-xs">Max (kg)</Label>
                              <Input
                                type="number"
                                value={tier.max_quantity_kg ?? ''}
                                placeholder="∞"
                                onChange={(e) => {
                                  const updated = [...newTemplateTiers];
                                  updated[index].max_quantity_kg = e.target.value ? Number(e.target.value) : null;
                                  setNewTemplateTiers(updated);
                                }}
                              />
                            </div>
                            <div>
                              <Label className="text-xs">Réduction (%)</Label>
                              <Input
                                type="number"
                                value={tier.discount_percent}
                                onChange={(e) => {
                                  const updated = [...newTemplateTiers];
                                  updated[index].discount_percent = Number(e.target.value);
                                  setNewTemplateTiers(updated);
                                }}
                              />
                            </div>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-red-500"
                            onClick={() => {
                              if (newTemplateTiers.length > 1) {
                                setNewTemplateTiers(newTemplateTiers.filter((_, i) => i !== index));
                              }
                            }}
                          >
                            ×
                          </Button>
                        </div>
                      ))}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          const last = newTemplateTiers[newTemplateTiers.length - 1];
                          setNewTemplateTiers([
                            ...newTemplateTiers,
                            {
                              min_quantity_kg: last?.max_quantity_kg ? last.max_quantity_kg + 1 : 500,
                              max_quantity_kg: null,
                              discount_percent: (last?.discount_percent || 0) + 5,
                            },
                          ]);
                        }}
                        disabled={newTemplateTiers.length >= 5}
                      >
                        + Ajouter un palier
                      </Button>
                    </div>
                  </div>

                  <DialogFooter>
                    <Button variant="outline" onClick={() => setShowTemplateDialog(false)}>
                      Annuler
                    </Button>
                    <Button onClick={handleCreateTemplate} disabled={!newTemplateName.trim()}>
                      Créer le template
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {templates.map((template) => (
                <Card key={template.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{template.name}</CardTitle>
                        <CardDescription>
                          {template.products_count} produit(s) utilisent ce template
                        </CardDescription>
                      </div>
                      {template.is_default && (
                        <Badge variant="secondary">Par défaut</Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {template.tiers.map((tier, index) => (
                        <div
                          key={index}
                          className="flex justify-between text-sm py-1 border-b last:border-0"
                        >
                          <span className="text-muted-foreground">
                            {tier.max_quantity_kg
                              ? `${tier.min_quantity_kg}-${tier.max_quantity_kg} kg`
                              : `${tier.min_quantity_kg}+ kg`}
                          </span>
                          <Badge variant={tier.discount_percent > 0 ? 'default' : 'secondary'}>
                            {tier.discount_percent > 0 ? `-${tier.discount_percent}%` : 'Base'}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}

              {templates.length === 0 && (
                <Card className="col-span-full">
                  <CardContent className="py-12 text-center">
                    <div className="text-4xl mb-4">📋</div>
                    <p className="text-muted-foreground mb-4">
                      Vous n'avez pas encore de templates
                    </p>
                    <Button onClick={() => setShowTemplateDialog(true)}>
                      Créer mon premier template
                    </Button>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
