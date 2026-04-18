'use client'

import { useState, useRef } from 'react';
import Link from 'next/link';
import { uploadDocument, listDocuments, deleteDocument } from '@/lib/api';
import { Document } from '@/types';
import { formatDateTime } from '@/lib/utils';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadDocuments = async () => {
    try {
      const docs = await listDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    }
  };

  const handleUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;

    setUploading(true);
    try {
      for (const file of Array.from(files)) {
        await uploadDocument(file);
      }
      await loadDocuments();
    } catch (err) {
      console.error('Upload failed:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteDocument(id);
      setDocuments(prev => prev.filter(d => d.id !== id));
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    handleUpload(e.dataTransfer.files);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Documents</h1>
          <Link href="/" className="text-blue-600 hover:underline">← Back</Link>
        </div>

        {/* Upload area */}
        <div
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer mb-8 transition ${
            dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".jpg,.jpeg,.png,.pdf,.doc,.docx"
            onChange={(e) => handleUpload(e.target.files)}
            className="hidden"
          />
          {uploading ? (
            <p className="text-blue-600">Uploading...</p>
          ) : (
            <>
              <p className="text-lg text-gray-600 mb-2">
                Drag and drop files here, or click to select
              </p>
              <p className="text-sm text-gray-400">
                Supports: JPG, PNG, PDF, DOC, DOCX
              </p>
            </>
          )}
        </div>

        {/* Document list */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b">
            <h2 className="text-xl font-semibold">Uploaded Documents</h2>
            <button onClick={loadDocuments} className="text-sm text-blue-600 hover:underline mt-1">
              Refresh list
            </button>
          </div>

          {documents.length === 0 ? (
            <p className="p-8 text-center text-gray-400">No documents uploaded yet</p>
          ) : (
            <div className="divide-y">
              {documents.map((doc) => (
                <div key={doc.id} className="p-4 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-medium">{doc.filename}</p>
                        <span className={`text-xs px-2 py-1 rounded ${getStatusColor(doc.status)}`}>
                          {doc.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mt-1">
                        {formatDateTime(doc.created_at)}
                      </p>
                      {doc.ocr_text && (
                        <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                          {doc.ocr_text.substring(0, 200)}...
                        </p>
                      )}
                      {doc.extracted_data && Object.keys(doc.extracted_data).length > 0 && (
                        <div className="mt-2">
                          <p className="text-xs text-gray-500">Extracted data:</p>
                          <pre className="text-xs bg-gray-100 p-2 rounded mt-1 overflow-x-auto">
                            {JSON.stringify(doc.extracted_data, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="text-red-600 hover:text-red-800 text-sm ml-4"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
