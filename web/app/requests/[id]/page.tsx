"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getRequestDetail, SourcingRequest, updateOfferStatus, getAiInsight, generateSourcingContract, updateLogisticsStatus } from "@/lib/api";
import { getRequestTimeline, TraceabilityEvent } from "@/lib/traceability";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Timeline } from "@/components/traceability/Timeline";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

export default function RequestDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [req, setReq] = useState<SourcingRequest | null>(null);
    const [insight, setInsight] = useState<any>(null); // Quick storage for AI insight
    const [viewingOfferId, setViewingOfferId] = useState<number | null>(null);
    const [contractUrl, setContractUrl] = useState<string | null>(null);
    const [timelineEvents, setTimelineEvents] = useState<TraceabilityEvent[]>([]);

    useEffect(() => {
        if (params.id) {
            const rid = Number(params.id);
            getRequestDetail(rid).then(setReq);
            getRequestTimeline(rid).then(setTimelineEvents);
        }
    }, [params.id]);

    const handleAction = async (offerId: number, status: string) => {
        await updateOfferStatus(offerId, status);
        // Refresh
        getRequestDetail(Number(params.id)).then(setReq);
    };

    const handleGenerateContract = async () => {
        if (!req) return;
        try {
            const data = await generateSourcingContract(req.id);
            setContractUrl(data.contract_url);
            alert("Contract Generated and Sent to Stakeholders!");
        } catch (e) {
            console.error(e);
            alert("Error generating contract");
        }
    };

    const handleLogisticsUpdate = async (status: string) => {
        if (!req) return;
        await updateLogisticsStatus(req.id, status);
        getRequestDetail(Number(params.id)).then(setReq);
    }

    const loadInsight = async (offerId: number) => {
        setViewingOfferId(offerId);
        const data = await getAiInsight(offerId);
        setInsight(data);
    };

    if (!req) return <div className="p-10 text-center">Loading Request...</div>;

    // Calc stats
    const acceptedKg = req.offers.filter(o => o.status === 'ACCEPTED').reduce((acc, o) => acc + o.volume_offered_kg, 0);
    const pendingKg = req.offers.filter(o => o.status === 'PENDING' || o.status === 'NEGOTIATING').reduce((acc, o) => acc + o.volume_offered_kg, 0);

    // Percentages
    const acceptedPct = (acceptedKg / req.volume_target_kg) * 100;
    const pendingPct = (pendingKg / req.volume_target_kg) * 100;

    // Logistics Steps
    const logisticsSteps = ["PREPARING", "TRANSIT_TO_PORT", "AT_PORT", "FOB_COMPLETE"];
    const currentStepIndex = logisticsSteps.indexOf(req.logistics_status || "PREPARING");

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="container mx-auto max-w-5xl">
                <Button variant="ghost" className="mb-4 pl-0" onClick={() => router.push('/dashboard/requests')}>
                    ← Back to Dashboard
                </Button>

                <div className="flex justify-between items-start mb-6">
                    <div>
                        <h1 className="text-3xl font-bold font-serif">Product Request #{req.id}</h1>
                        <p className="text-muted-foreground">{req.volume_target_kg}kg {req.product_type} (Grade {req.grade_target}) @ ${req.price_target_usd}/kg</p>
                        {req.required_certs && req.required_certs.length > 0 && (
                            <div className="mt-2 flex gap-2">
                                <span className="text-sm font-medium">Required Certs:</span>
                                {req.required_certs.map(c => <Badge key={c} variant="outline" className="text-xs">{c}</Badge>)}
                            </div>
                        )}
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <Badge className="text-lg px-4 py-1">{req.status}</Badge>
                        {acceptedKg > 0 && (
                            <Button size="sm" onClick={handleGenerateContract} disabled={!!contractUrl}>
                                {contractUrl ? "Contract Sent ✅" : "📄 Generate Contract"}
                            </Button>
                        )}
                    </div>
                </div>

                <Tabs defaultValue="overview" className="w-full">
                    <TabsList className="mb-8">
                        <TabsTrigger value="overview">Overview & Offers</TabsTrigger>
                        <TabsTrigger value="traceability">Traceability & Logistics</TabsTrigger>
                    </TabsList>

                    <TabsContent value="overview">
                        {/* MEGA BAR */}
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="text-sm uppercase tracking-wide text-muted-foreground">Sourcing Progress</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="h-8 w-full bg-secondary rounded-full overflow-hidden flex relative">
                                    {/* Accepted Segment */}
                                    <div className="bg-green-500 h-full flex items-center justify-center text-xs font-bold text-white transition-all" style={{ width: `${acceptedPct}%` }}>
                                        {acceptedKg > 0 && `${acceptedKg}kg`}
                                    </div>
                                    {/* Pending Segment */}
                                    <div className="bg-yellow-400 h-full flex items-center justify-center text-xs font-bold text-black opacity-80 transition-all" style={{ width: `${pendingPct}%` }}>
                                        {pendingKg > 0 && `${pendingKg}kg`}
                                    </div>

                                    {/* Target Marker (if < 100%) */}
                                    {acceptedPct + pendingPct < 100 && (
                                        <div className="absolute right-0 top-0 h-full w-full flex items-center justify-end pr-2 text-xs text-muted-foreground">
                                            Target: {req.volume_target_kg}kg
                                        </div>
                                    )}
                                </div>
                                <div className="flex gap-6 mt-4 text-sm">
                                    <div className="flex items-center gap-2">
                                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                        <span>Secured ({Math.round(acceptedPct)}%)</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                                        <span>Negotiating ({Math.round(pendingPct)}%)</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className="w-3 h-3 rounded-full bg-secondary"></div>
                                        <span>Remaining to source</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* OFFERS LIST */}
                        <h2 className="text-xl font-bold mb-4">Offers Received</h2>
                        <Card>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Seller / Facil.</TableHead>
                                        <TableHead>Volume</TableHead>
                                        <TableHead>Price (FOB)</TableHead>
                                        <TableHead>Trust Score</TableHead>
                                        <TableHead>Status</TableHead>
                                        <TableHead>AI Insight</TableHead>
                                        <TableHead className="text-right">Action</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {req.offers.length === 0 && (
                                        <TableRow>
                                            <TableCell colSpan={7} className="text-center py-8 text-muted-foreground">
                                                No offers yet. The "Smart Match" AI is notifying facilitators...
                                            </TableCell>
                                        </TableRow>
                                    )}
                                    {req.offers.map((offer) => (
                                        <TableRow key={offer.id}>
                                            <TableCell className="font-medium">
                                                Facilitator #{offer.facilitator_id}
                                                {offer.cert_proofs_urls && offer.cert_proofs_urls.length > 0 && (
                                                    <div className="flex gap-1 mt-1">
                                                        <Badge variant="outline" className="text-[10px] bg-green-50 text-green-700 border-green-200">Cert Verified ✅</Badge>
                                                    </div>
                                                )}
                                            </TableCell>
                                            <TableCell>{offer.volume_offered_kg} kg</TableCell>
                                            <TableCell className={offer.price_offered_usd > req.price_target_usd ? "text-red-500 font-bold" : "text-green-600 font-bold"}>
                                                ${offer.price_offered_usd}
                                            </TableCell>
                                            <TableCell>
                                                <div className="flex items-center gap-1">
                                                    ⭐ {offer.trust_score_snapshot || 4.5}
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant={offer.status === 'ACCEPTED' ? 'default' : 'secondary'}>{offer.status}</Badge>
                                            </TableCell>
                                            <TableCell>
                                                {viewingOfferId === offer.id ? (
                                                    <div className="text-xs max-w-[200px] bg-blue-50 p-2 rounded border border-blue-100">
                                                        {insight ? insight.ai_advice : "Analyzing..."}
                                                    </div>
                                                ) : (
                                                    <Button variant="link" size="sm" onClick={() => loadInsight(offer.id)}>
                                                        Ask AI 🤖
                                                    </Button>
                                                )}
                                            </TableCell>
                                            <TableCell className="text-right space-x-2">
                                                {offer.status !== 'ACCEPTED' && (
                                                    <>
                                                        <Button size="sm" variant="outline" onClick={() => handleAction(offer.id, 'NEGOTIATING')}>Negotiate</Button>
                                                        <Button size="sm" variant="default" onClick={() => handleAction(offer.id, 'ACCEPTED')}>Accept</Button>
                                                    </>
                                                )}
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </Card>
                    </TabsContent>

                    <TabsContent value="traceability">
                        <div className="grid md:grid-cols-3 gap-8">
                            {/* LEFT: Timeline */}
                            <div className="md:col-span-2">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="font-serif">Audit Trail & Traceability</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <Timeline events={timelineEvents} />
                                    </CardContent>
                                </Card>
                            </div>

                            {/* RIGHT: Logistics Control */}
                            <div>
                                {/* LOGISTICS TRACKER (Feature 8) MOVED HERE */}
                                <Card className="border-blue-200 bg-blue-50/30 sticky top-6">
                                    <CardHeader className="pb-2">
                                        <div className="flex justify-between items-center">
                                            <CardTitle className="text-sm uppercase tracking-wide text-blue-800">Supply Chain Control</CardTitle>
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="flex flex-col gap-2">
                                            {logisticsSteps.map((step, idx) => (
                                                <div key={step} className={`p-2 rounded border flex items-center justify-between ${currentStepIndex >= idx ? 'bg-white border-blue-200 shadow-sm' : 'border-transparent text-muted-foreground'}`}>
                                                    <div className="flex items-center gap-2">
                                                        <div className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border ${currentStepIndex >= idx ? 'bg-blue-600 text-white border-blue-600' : 'bg-gray-100 text-gray-400'}`}>
                                                            {idx + 1}
                                                        </div>
                                                        <span className="text-xs font-semibold">{step}</span>
                                                    </div>
                                                    {acceptedKg > 0 && (
                                                        <Button
                                                            size="sm"
                                                            variant={currentStepIndex === idx ? "default" : "ghost"}
                                                            className="h-6 text-[10px]"
                                                            onClick={() => handleLogisticsUpdate(step)}
                                                            disabled={currentStepIndex > idx} // Can go back? Maybe. For now disable future
                                                        >
                                                            {currentStepIndex === idx ? "Active" : "Set"}
                                                        </Button>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                        <div className="mt-6 pt-4 border-t border-blue-200">
                                            <h4 className="text-xs font-bold text-blue-900 mb-2">Evidence Vault</h4>
                                            {contractUrl ? (
                                                <Button size="sm" variant="outline" className="w-full justify-start text-xs h-8 bg-white" onClick={() => window.open(contractUrl, '_blank')}>
                                                    📄 Signed Contract (PDF)
                                                </Button>
                                            ) : (
                                                <div className="text-xs text-muted-foreground italic">No documents yet.</div>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}
