"use client";

import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File, Trash2, CheckCircle, Loader2 } from 'lucide-react';
import api from '@/lib/api';

export default function DocumentUpload() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);

  const fetchDocuments = async () => {
    try {
      const res = await api.get('/documents');
      setDocuments(res.data);
    } catch (err) {
      console.error('Failed to fetch documents', err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/documents', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchDocuments();
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] }
  });

  const deleteDocument = async (id: string) => {
    try {
      await api.delete(`/documents/${id}`);
      fetchDocuments();
    } catch (err) {
      console.error('Delete failed', err);
    }
  };

  return (
    <div className="space-y-6">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 bg-white'}`}
      >
        <input {...getInputProps()} />
        <UploadCloud className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        {isDragActive ? (
          <p className="text-blue-600 font-medium">Drop the PDF here...</p>
        ) : (
          <div>
            <p className="text-gray-700 font-medium">Drag & drop a PDF document here, or click to select</p>
            <p className="text-sm text-gray-500 mt-1">Supports engineering specs, modification packages, and UFSAR sections.</p>
          </div>
        )}
      </div>

      {uploading && (
        <div className="flex items-center gap-2 text-blue-600">
          <Loader2 className="animate-spin" size={20} /> Uploading and indexing document...
        </div>
      )}

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="font-semibold text-lg">Ingested Documents</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {documents.length === 0 ? (
            <div className="p-6 text-center text-gray-500">No documents uploaded yet.</div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                <div className="flex items-center gap-3">
                  <div className="bg-red-100 p-2 rounded text-red-600">
                    <File size={20} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{doc.filename}</p>
                    <div className="flex gap-4 text-xs text-gray-500 mt-1">
                      <span>Status: {doc.status}</span>
                      <span>Chunks: {doc.chunk_count}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {doc.status === 'processing' ? (
                    <Loader2 className="animate-spin text-blue-500" size={18} />
                  ) : (
                    <CheckCircle className="text-emerald-500" size={18} />
                  )}
                  <button onClick={() => deleteDocument(doc.id)} className="text-gray-400 hover:text-red-500 p-2">
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}