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
  const res = await fetch(`${API_URL}/orders/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_id: productId,
      quantity_kg: quantity,
      offer_price_total: amount,
      buyer_name: "Sarah Import Corp" // Hardcoded for MVP flow
    }),
  });
  if (!res.ok) throw new Error('Failed to create order');
  return res.json();
}

export async function generateContract(orderId: number) {
  await fetch(`${API_URL}/orders/${orderId}/contract`, { method: 'POST' });
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
