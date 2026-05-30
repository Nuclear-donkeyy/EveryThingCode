import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EveryThingCode Next.js Quickstart",
  description: "A minimal App Router teaching project"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
