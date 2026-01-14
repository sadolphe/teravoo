"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navigation() {
    const pathname = usePathname();
    const [isOpen, setIsOpen] = useState(false);

    const links = [
        { href: "/", label: "Home" },
        { href: "/products", label: "Marketplace" },
        { href: "/producers", label: "Our Producers" },
    ];

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center px-6 mx-auto max-w-7xl">
                <div className="mr-8 hidden md:flex">
                    <Link href="/" className="mr-6 flex items-center space-x-2 font-bold text-xl font-serif">
                        <div className="h-8 w-8 bg-primary rounded-full" />
                        <span>TeraVoo</span>
                    </Link>
                    <div className="flex gap-6 text-sm font-medium">
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={cn(
                                    "transition-colors hover:text-foreground/80",
                                    pathname === link.href ? "text-foreground" : "text-foreground/60"
                                )}
                            >
                                {link.label}
                            </Link>
                        ))}
                        <Link
                            href="/traceability"
                            className={cn(
                                "transition-colors hover:text-foreground/80",
                                pathname === "/traceability" ? "text-foreground" : "text-foreground/60"
                            )}
                        >
                            Traceability
                        </Link>
                    </div>
                </div>

                <div className="hidden md:flex ml-auto items-center gap-4">
                    <Link href="/dashboard">
                        <Button variant="ghost" className="text-muted-foreground">My Dashboard</Button>
                    </Link>
                    <Link href="/requests/create">
                        <Button className="font-semibold shadow-lg shadow-primary/20">Sourcing Request</Button>
                    </Link>
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2 ml-auto"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <X /> : <Menu />}
                </button>

                {/* Mobile Menu */}
                {isOpen && (
                    <div className="absolute top-16 left-0 w-full bg-background border-b md:hidden p-4 flex flex-col gap-4 shadow-lg z-[100]">
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                onClick={() => setIsOpen(false)}
                                className={cn(
                                    "text-sm font-medium transition-colors hover:text-foreground/80",
                                    pathname === link.href ? "text-foreground" : "text-foreground/60"
                                )}
                            >
                                {link.label}
                            </Link>
                        ))}
                        {/* Missing Links */}
                        <Link
                            href="/traceability"
                            onClick={() => setIsOpen(false)}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-foreground/80",
                                pathname === "/traceability" ? "text-foreground" : "text-foreground/60"
                            )}
                        >
                            Traceability
                        </Link>
                        <hr className="border-border" />
                        <Link href="/dashboard" onClick={() => setIsOpen(false)}>
                            <Button variant="ghost" className="w-full justify-start text-muted-foreground">My Dashboard</Button>
                        </Link>
                        <Link href="/requests/create" onClick={() => setIsOpen(false)}>
                            <Button className="w-full shadow-lg shadow-primary/20">Sourcing Request</Button>
                        </Link>
                    </div>
                )}
            </div>
        </nav>
    );
}
