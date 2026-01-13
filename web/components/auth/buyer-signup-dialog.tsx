"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface BuyerSignupDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onSuccess: () => void;
}

export function BuyerSignupDialog({ open, onOpenChange, onSuccess }: BuyerSignupDialogProps) {
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [company, setCompany] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/api/v1/auth/signup/buyer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, company_name: company }),
            });

            if (res.ok) {
                const data = await res.json();
                // MVP: Store token in localStorage
                localStorage.setItem("buyer_token", data.access_token);
                if (data.kyb_status) localStorage.setItem("kyb_status", data.kyb_status);
                onSuccess();
                onOpenChange(false);
            } else {
                alert("Signup failed");
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to server");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Unlock Full Access</DialogTitle>
                    <DialogDescription>
                        Join the circle of trusted buyers to request samples and view detailed quality reports.
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit}>
                    <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                            <Label htmlFor="email">Work Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="you@company.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="company">Company Name</Label>
                            <Input
                                id="company"
                                placeholder="Global Vanilla Inc."
                                value={company}
                                onChange={(e) => setCompany(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button type="submit" disabled={loading}>
                            {loading ? "Verifying..." : "Continue to Sample Request"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
