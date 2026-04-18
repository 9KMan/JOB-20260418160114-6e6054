import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Voice-Driven SaaS MVP',
  description: 'Voice input, document OCR, and financial tracking',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">{children}</body>
    </html>
  )
}
