"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createRequest } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function CreateRequestPage() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);

    // Form Data
    const [formData, setFormData] = useState({
        product_type: "Vanilla",
        grade_target: "B",
        volume_target_kg: 1000,
        price_target_usd: 215,
        accepts_partial: true
    });

    const handleNext = () => setStep(step + 1);
    const handleBack = () => setStep(step - 1);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await createRequest(formData);
            router.push('/dashboard/requests'); // Go to list
        } catch (e) {
            console.error(e);
            alert("Error creating request");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6">
            <div className="w-full max-w-2xl">
                <div className="mb-8 flex justify-between items-center">
                    <h1 className="text-2xl font-serif font-bold text-primary">New Sourcing Request</h1>
                    <span className="text-sm text-muted-foreground">Step {step} of 3</span>
                </div>

                <Card>
                    <CardHeader>
                        <CardTitle>
                            {step === 1 && "1. Product & Quality"}
                            {step === 2 && "2. Volume & Logistics"}
                            {step === 3 && "3. Price Target"}
                        </CardTitle>
                        <CardDescription>
                            Define your requirements precisely to get the best AI-matched offers.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">

                        {/* STEP 1: PRODUCT */}
                        {step === 1 && (
                            <>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Product Type</label>
                                    <Select
                                        defaultValue={formData.product_type}
                                        onValueChange={(v) => setFormData({ ...formData, product_type: v })}
                                    >
                                        <SelectTrigger><SelectValue /></SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="Vanilla">Vanilla (Beans)</SelectItem>
                                            <SelectItem value="Clove">Clove</SelectItem>
                                            <SelectItem value="Lychee">Lychee</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Target Grade</label>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        {["A", "B", "C"].map((grade) => (
                                            <div
                                                key={grade}
                                                className={`border rounded-lg p-4 cursor-pointer hover:border-primary transition-all ${formData.grade_target === grade ? 'border-primary bg-primary/5 ring-1 ring-primary' : 'border-border'}`}
                                                onClick={() => setFormData({ ...formData, grade_target: grade })}
                                            >
                                                <div className="font-bold mb-1">Grade {grade}</div>
                                                <div className="text-xs text-muted-foreground">
                                                    {grade === 'A' && "Gourmet, >30% Moisture"}
                                                    {grade === 'B' && "Extraction, 20-30% Moisture"}
                                                    {grade === 'C' && "Industrial/Cuts"}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                <div className="bg-blue-50 text-blue-800 p-4 rounded-md text-sm">
                                    💡 <strong>AI Insight:</strong> Grade B is currently abundant in Sava Region (Harvest 2025). Expect fast replies.
                                </div>
                            </>
                        )}

                        {/* STEP 2: VOLUME */}
                        {step === 2 && (
                            <>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Total Volume (kg)</label>
                                    <Input
                                        type="number"
                                        value={formData.volume_target_kg}
                                        onChange={(e) => setFormData({ ...formData, volume_target_kg: Number(e.target.value) })}
                                    />
                                </div>

                                <div className="flex items-center justify-between border p-4 rounded-md">
                                    <div>
                                        <div className="font-medium">Multi-Seller Sourcing</div>
                                        <div className="text-sm text-muted-foreground">Accept partial offers from different producers?</div>
                                    </div>
                                    <input
                                        type="checkbox"
                                        className="h-5 w-5"
                                        checked={formData.accepts_partial}
                                        onChange={(e) => setFormData({ ...formData, accepts_partial: e.target.checked })}
                                    />
                                </div>
                                <div className="bg-yellow-50 text-yellow-800 p-4 rounded-md text-sm">
                                    📊 Choosing Multi-Seller increases your fill rate by <strong>300%</strong>.
                                </div>
                            </>
                        )}

                        {/* STEP 3: PRICE */}
                        {step === 3 && (
                            <>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Target FOB Price (USD/kg)</label>
                                    <Input
                                        type="number"
                                        value={formData.price_target_usd}
                                        onChange={(e) => setFormData({ ...formData, price_target_usd: Number(e.target.value) })}
                                    />
                                    <p className="text-xs text-muted-foreground">Current Market Avg: $218 - $230</p>
                                </div>

                                {formData.price_target_usd < 210 && (
                                    <div className="bg-red-50 text-red-800 p-4 rounded-md text-sm flex items-start gap-2">
                                        <span>⚠️</span>
                                        <div>
                                            <strong>Low Price Warning:</strong> Your offer is 5% below market floor. Facilitators may ignore this request.
                                        </div>
                                    </div>
                                )}
                            </>
                        )}

                    </CardContent>
                    <div className="p-6 pt-0 flex justify-between">
                        {step > 1 ? (
                            <Button variant="outline" onClick={handleBack}>Back</Button>
                        ) : (
                            <Button variant="ghost" onClick={() => router.back()}>Cancel</Button>
                        )}

                        {step < 3 ? (
                            <Button onClick={handleNext}>Next Step</Button>
                        ) : (
                            <Button onClick={handleSubmit} disabled={loading}>
                                {loading ? "Publishing..." : "Publish Request"}
                            </Button>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    );
}
