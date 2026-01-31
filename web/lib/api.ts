export type Product = {
  id: number;
  name: string;
  price_fob: number;
  image_url_raw: string;
  image_url_ai: string;
  status: string;
  description?: string;
  origin?: string;
  farmer_name?: string;
  harvest_date?: string;
  moisture_content?: number;
  vanillin_content?: number;
  quantity_available?: number;
  // Pricing fields
  moq_kg?: number;
  pricing_mode?: 'SINGLE' | 'TIERED' | 'TEMPLATE';
  template_id?: number;
};

// --- Pricing Types ---
export type PriceTier = {
  id?: number;
  min_quantity_kg: number;
  max_quantity_kg: number | null;
  price_per_kg: number;
  position: number;
  discount_percent?: number;
};

export type PriceTierTemplate = {
  id: number;
  producer_id: number;
  name: string;
  description?: string;
  is_default: boolean;
  tiers: TemplateTier[];
  products_count: number;
};

export type TemplateTier = {
  id: number;
  min_quantity_kg: number;
  max_quantity_kg: number | null;
  discount_percent: number;
  position: number;
};

export type ProductPricingInfo = {
  product_id: number;
  pricing_mode: string;
  base_price_fob: number;
  moq_kg: number;
  template_id?: number;
  tiers: PriceTier[];
};

export type CalculatedPrice = {
  product_id: number;
  quantity_kg: number;
  pricing_mode: string;
  tier_applied?: {
    min_quantity_kg: number;
    max_quantity_kg: number | null;
    position: number;
  };
  price_per_kg: number;
  total: number;
  savings_vs_base?: {
    percent: number;
    amount: number;
  };
  next_tier?: {
    at_quantity_kg: number;
    price_per_kg: number;
    extra_savings_total: number;
  };
  price_trend?: {
    direction: 'up' | 'down' | 'stable';
    percent: number;
    since?: string;
  };
};

export type Order = {
  id: number;
  product_id: number;
  product_name: string;
  amount: number;
  status: string;
  contract_url?: string;
};

// --- Sourcing Types ---
export type SourcingOffer = {
  id: number;
  request_id: number;
  facilitator_id: number;
  volume_offered_kg: number;
  price_offered_usd: number;
  status: string;
  photos_json?: string[];
  cert_proofs_urls?: string[]; // Feature 7
  trust_score_snapshot?: number; // Feature 9
}

export type SourcingRequest = {
  id: number;
  product_type: string;
  volume_target_kg: number;
  price_target_usd: number;
  grade_target: string;
  status: string;
  logistics_status: string; // Feature 8
  required_certs?: string[]; // Feature 7
  offers: SourcingOffer[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export async function getProducts(): Promise<Product[]> {
  try {
    const res = await fetch(`${API_URL}/products/`, {
      cache: 'no-store',
    });
    if (!res.ok) throw new Error('Failed to fetch products');
    return res.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getOrders(): Promise<Order[]> {
  try {
    const res = await fetch(`${API_URL}/orders/`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch orders');
    return res.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function createOrder(productId: number, amount: number, quantity: number): Promise<Order> {
  // Get buyer name from session storage, or use a generic buyer name
  // In production, this would come from the authenticated user session
  const buyerName = typeof window !== 'undefined'
    ? sessionStorage.getItem('buyer_name') || 'Anonymous Buyer'
    : 'Web Client';

  const res = await fetch(`${API_URL}/orders/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_id: productId,
      quantity_kg: quantity,
      offer_price_total: amount,
      buyer_name: buyerName  // UPDATED: Use dynamic buyer name instead of hardcoded "Sarah Import Corp"
    }),
  });
  if (!res.ok) throw new Error('Failed to create order');
  return res.json();
}

export async function generateContract(orderId: number) {
  await fetch(`${API_URL}/orders/${orderId}/contract`, { method: 'POST' });
}

export async function payToEscrow(orderId: number): Promise<Order> {
  const res = await fetch(`${API_URL}/orders/${orderId}/pay`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!res.ok) throw new Error('Failed to process payment');
  return res.json();
}


// --- Sourcing Endpoints ---

export async function getRequests(): Promise<SourcingRequest[]> {
  try {
    const res = await fetch(`${API_URL}/requests/`, { cache: 'no-store' });
    return res.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getRequestDetail(id: number): Promise<SourcingRequest> {
  const res = await fetch(`${API_URL}/requests/${id}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Request not found');
  return res.json();
}

export async function createRequest(data: any): Promise<SourcingRequest> {
  const res = await fetch(`${API_URL}/requests/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      buyer_id: 1 // Mock
    }),
  });
  if (!res.ok) throw new Error('Failed to create request');
  return res.json();
}

export async function updateOfferStatus(offerId: number, status: string) {
  const res = await fetch(`${API_URL}/requests/offers/${offerId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  return res.json();
}

export async function getAiInsight(offerId: number) {
  const res = await fetch(`${API_URL}/requests/offers/${offerId}/ai-insight`);
  return res.json();
}

export async function generateSourcingContract(requestId: number): Promise<{ contract_url: string }> {
  const res = await fetch(`${API_URL}/requests/${requestId}/contract`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to generate contract');
  return res.json();
}

export async function updateLogisticsStatus(requestId: number, status: string) {
  const res = await fetch(`${API_URL}/requests/${requestId}/logistics?status=${status}`, { method: 'PUT' });
  return res.json();
}
export async function deleteRequest(requestId: number) {
  const res = await fetch(`${API_URL}/requests/${requestId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete request');
  return res.json();
}

export async function getProductTraceability(productId: number) {
  try {
    const res = await fetch(`${API_URL}/traceability/product/${productId}`, { cache: 'no-store' });
    if (!res.ok) return [];
    return res.json();
  } catch (e) {
    console.error(e);
    return [];
  }
}

// --- Pricing Endpoints ---

export async function getProductPriceTiers(productId: number): Promise<ProductPricingInfo | null> {
  try {
    const res = await fetch(`${API_URL}/pricing/products/${productId}/price-tiers`, { cache: 'no-store' });
    if (!res.ok) return null;
    return res.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

export async function calculatePrice(productId: number, quantityKg: number): Promise<CalculatedPrice | null> {
  try {
    const res = await fetch(`${API_URL}/pricing/products/${productId}/calculate-price?quantity_kg=${quantityKg}`, {
      cache: 'no-store'
    });
    if (!res.ok) return null;
    return res.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

export async function setProductPriceTiers(productId: number, tiers: Omit<PriceTier, 'id' | 'position' | 'discount_percent'>[]): Promise<PriceTier[]> {
  const res = await fetch(`${API_URL}/pricing/products/${productId}/price-tiers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tiers }),
  });
  if (!res.ok) throw new Error('Failed to set price tiers');
  return res.json();
}

export async function updateProductPricingMode(productId: number, mode: string, templateId?: number) {
  const res = await fetch(`${API_URL}/pricing/products/${productId}/pricing-mode`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode, template_id: templateId }),
  });
  if (!res.ok) throw new Error('Failed to update pricing mode');
  return res.json();
}

// --- Producer Template Endpoints ---

export async function getProducerTemplates(producerId: number): Promise<PriceTierTemplate[]> {
  try {
    const res = await fetch(`${API_URL}/pricing/producers/${producerId}/price-templates`, { cache: 'no-store' });
    if (!res.ok) return [];
    return res.json();
  } catch (e) {
    console.error(e);
    return [];
  }
}

export async function createProducerTemplate(producerId: number, template: {
  name: string;
  description?: string;
  is_default?: boolean;
  tiers: { min_quantity_kg: number; max_quantity_kg?: number; discount_percent: number }[];
}): Promise<PriceTierTemplate> {
  const res = await fetch(`${API_URL}/pricing/producers/${producerId}/price-templates`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(template),
  });
  if (!res.ok) throw new Error('Failed to create template');
  return res.json();
}
