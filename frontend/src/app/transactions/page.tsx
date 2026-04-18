'use client'

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { listTransactions, getTransactionSummary, deleteTransaction, createTransaction } from '@/lib/api';
import { Transaction, TransactionSummary, Entry } from '@/types';
import { formatDate, formatCurrency } from '@/lib/utils';
import { listEntries } from '@/lib/api';

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<TransactionSummary | null>(null);
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  // Form state
  const [selectedEntry, setSelectedEntry] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('general');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [txs, sum, ents] = await Promise.all([
        listTransactions(),
        getTransactionSummary(),
        listEntries(),
      ]);
      setTransactions(txs);
      setSummary(sum);
      setEntries(ents);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createTransaction({
        entry_id: selectedEntry,
        amount: parseFloat(amount),
        category,
        description,
        date,
      });
      setShowForm(false);
      setSelectedEntry('');
      setAmount('');
      setCategory('general');
      setDescription('');
      setDate(new Date().toISOString().split('T')[0]);
      await loadData();
    } catch (err) {
      console.error('Create failed:', err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteTransaction(id);
      setTransactions(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const CATEGORIES = ['general', 'food', 'transport', 'office', 'utilities', 'entertainment', 'shopping'];

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Transactions</h1>
          <Link href="/" className="text-blue-600 hover:underline">← Back</Link>
        </div>

        {/* Summary cards */}
        {summary && (
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-green-100 rounded-lg p-4">
              <p className="text-sm text-green-800">Total Amount</p>
              <p className="text-2xl font-bold text-green-900">
                {formatCurrency(summary.total_amount)}
              </p>
            </div>
            <div className="bg-blue-100 rounded-lg p-4">
              <p className="text-sm text-blue-800">Transactions</p>
              <p className="text-2xl font-bold text-blue-900">
                {summary.transaction_count}
              </p>
            </div>
            <div className="bg-purple-100 rounded-lg p-4">
              <p className="text-sm text-purple-800">Categories</p>
              <p className="text-2xl font-bold text-purple-900">
                {Object.keys(summary.by_category).length}
              </p>
            </div>
          </div>
        )}

        {/* Category breakdown */}
        {summary && Object.keys(summary.by_category).length > 0 && (
          <div className="bg-white rounded-lg shadow p-4 mb-8">
            <h2 className="text-lg font-semibold mb-3">By Category</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.by_category).map(([cat, amt]) => (
                <span key={cat} className="bg-gray-100 px-3 py-1 rounded-full text-sm">
                  {cat}: {formatCurrency(amt as number)}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Add transaction button */}
        <button
          onClick={() => setShowForm(!showForm)}
          className="mb-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          {showForm ? 'Cancel' : '+ Add Transaction'}
        </button>

        {/* Transaction form */}
        {showForm && (
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-lg font-semibold mb-4">New Transaction</h2>
            <div className="grid gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Entry</label>
                <select
                  value={selectedEntry}
                  onChange={(e) => setSelectedEntry(e.target.value)}
                  required
                  className="w-full p-2 border rounded-lg"
                >
                  <option value="">Select an entry...</option>
                  {entries.map(e => (
                    <option key={e.id} value={e.id}>
                      [{e.type}] {e.content.substring(0, 50)}...
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Amount ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                    className="w-full p-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full p-2 border rounded-lg"
                  >
                    {CATEGORIES.map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full p-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  required
                  className="w-full p-2 border rounded-lg"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Create Transaction
              </button>
            </div>
          </form>
        )}

        {/* Transactions list */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-4 border-b">
            <h2 className="text-xl font-semibold">All Transactions</h2>
          </div>

          {loading ? (
            <p className="p-8 text-center text-gray-400">Loading...</p>
          ) : transactions.length === 0 ? (
            <p className="p-8 text-center text-gray-400">No transactions yet</p>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {transactions.map(txn => (
                  <tr key={txn.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm">{formatDate(txn.date)}</td>
                    <td className="px-4 py-3 text-sm font-medium text-green-600">
                      {formatCurrency(txn.amount)}
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {txn.category}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">{txn.description}</td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDelete(txn.id)}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <button onClick={loadData} className="mt-4 text-blue-600 hover:underline">
          Refresh
        </button>
      </div>
    </main>
  );
}
