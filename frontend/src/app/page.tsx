'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">
          Voice-Driven SaaS MVP
        </h1>

        <div className="grid md:grid-cols-2 gap-6">
          <Link href="/voice" className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-2 text-blue-600">Voice Input</h2>
            <p className="text-gray-600">Record or upload voice messages for transcription</p>
          </Link>

          <Link href="/documents" className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-2 text-green-600">Documents</h2>
            <p className="text-gray-600">Upload receipts and files for OCR processing</p>
          </Link>

          <Link href="/entries" className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-2 text-purple-600">Entries</h2>
            <p className="text-gray-600">View and manage all voice, text, and document entries</p>
          </Link>

          <Link href="/transactions" className="block p-6 bg-white rounded-lg shadow hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-2 text-orange-600">Transactions</h2>
            <p className="text-gray-600">Financial tracking and summary dashboards</p>
          </Link>
        </div>
      </div>
    </main>
  )
}
