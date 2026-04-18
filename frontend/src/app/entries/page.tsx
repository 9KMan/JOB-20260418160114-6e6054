'use client'

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { listEntries, deleteEntry } from '@/lib/api';
import { Entry } from '@/types';
import { formatDateTime } from '@/lib/utils';

const TYPE_COLORS: Record<string, string> = {
  text: 'bg-blue-100 text-blue-800',
  voice: 'bg-purple-100 text-purple-800',
  document: 'bg-green-100 text-green-800',
};

export default function EntriesPage() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [filter, setFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  const loadEntries = async () => {
    setLoading(true);
    try {
      const data = await listEntries();
      setEntries(data);
    } catch (err) {
      console.error('Failed to load entries:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteEntry(id);
      setEntries(prev => prev.filter(e => e.id !== id));
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const filteredEntries = filter === 'all'
    ? entries
    : entries.filter(e => e.type === filter);

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Entries</h1>
          <Link href="/" className="text-blue-600 hover:underline">← Back</Link>
        </div>

        {/* Filter */}
        <div className="flex gap-2 mb-6">
          {['all', 'text', 'voice', 'document'].map(type => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-4 py-2 rounded-lg capitalize ${
                filter === type
                  ? 'bg-gray-800 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {type}
            </button>
          ))}
        </div>

        {/* Entries table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Content</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {loading ? (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-gray-400">
                    Loading...
                  </td>
                </tr>
              ) : filteredEntries.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-gray-400">
                    No entries found
                  </td>
                </tr>
              ) : (
                filteredEntries.map(entry => (
                  <tr key={entry.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded ${TYPE_COLORS[entry.type]}`}>
                        {entry.type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-sm text-gray-900 max-w-md truncate">
                        {entry.content}
                      </p>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {formatDateTime(entry.created_at)}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDelete(entry.id)}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <button
          onClick={loadEntries}
          className="mt-4 text-blue-600 hover:underline"
        >
          Refresh
        </button>
      </div>
    </main>
  );
}
