"use client";

import { CheckCircle2, Circle, AlertCircle, Clock, FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Types matching backend response
export type TraceabilityEvent = {
    id: number;
    stage: string;
    status: "VALIDATED" | "PENDING" | "ALERT" | "CORRECTION";
    description: string;
    location_scan?: string;
    documents_urls?: string[];
    timestamp: string;
    created_by?: string;
};

type TimelineProps = {
    events: TraceabilityEvent[];
};

export function Timeline({ events }: TimelineProps) {
    if (!events || events.length === 0) {
        return <div className="text-center py-10 text-muted-foreground">No traceability events recorded yet.</div>;
    }

    return (
        <div className="relative border-l-2 border-muted ml-4 space-y-8 pb-8">
            {events.map((event, index) => {
                const isLast = index === events.length - 1;

                let Icon = Circle;
                let colorClass = "text-muted-foreground bg-background border-muted";

                if (event.status === "VALIDATED") {
                    Icon = CheckCircle2;
                    colorClass = "text-green-600 bg-green-50 border-green-200";
                } else if (event.status === "ALERT") {
                    Icon = AlertCircle;
                    colorClass = "text-red-600 bg-red-50 border-red-200";
                } else if (event.status === "CORRECTION") {
                    Icon = AlertCircle;
                    colorClass = "text-orange-600 bg-orange-50 border-orange-200";
                } else if (event.status === "PENDING") {
                    Icon = Clock;
                    colorClass = "text-blue-600 bg-blue-50 border-blue-200";
                }

                return (
                    <div key={event.id} className="relative pl-8">
                        {/* Dot Icon */}
                        <div className={cn(
                            "absolute -left-[9px] top-0 rounded-full p-1 border shadow-sm",
                            colorClass
                        )}>
                            <Icon size={16} />
                        </div>

                        {/* Content */}
                        <div className="flex flex-col gap-2">
                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                                <h3 className="font-bold text-lg">{event.stage}</h3>
                                <span className="text-xs text-muted-foreground">
                                    {new Date(event.timestamp).toLocaleString()}
                                </span>
                            </div>

                            <Card className={cn("border-l-4",
                                event.status === "VALIDATED" ? "border-l-green-500" :
                                    event.status === "ALERT" ? "border-l-red-500" :
                                        "border-l-gray-300"
                            )}>
                                <CardContent className="pt-4 pb-4">
                                    <p className="text-sm text-gray-800">{event.description}</p>

                                    {event.location_scan && (
                                        <div className="mt-2 text-xs text-muted-foreground flex items-center gap-1">
                                            📍 GPS: {event.location_scan}
                                        </div>
                                    )}

                                    {event.created_by && (
                                        <div className="mt-1 text-xs text-muted-foreground font-mono">
                                            By: {event.created_by}
                                        </div>
                                    )}

                                    {event.documents_urls && event.documents_urls.length > 0 && (
                                        <div className="mt-3 flex gap-2">
                                            {event.documents_urls.map((doc, i) => (
                                                <Button key={i} variant="outline" size="sm" className="h-7 text-xs gap-1">
                                                    <FileText size={12} />
                                                    View Document
                                                </Button>
                                            ))}
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
