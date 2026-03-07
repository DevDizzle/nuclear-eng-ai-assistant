"use client";

import React, { useState } from 'react';
import { ShieldAlert, Loader2, FileDown } from 'lucide-react';
import api from '@/lib/api';
import CitationTable from './CitationTable';

export default function ScreeningForm() {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const generateScreening = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await api.post('/screening', { modification_description: description });
      setResult(res.data);
    } catch (err) {
      console.error('Screening generation failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full">
      {/* Input Section */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm flex flex-col h-full">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <ShieldAlert className="text-amber-500" size={20} />
          Modification Description
        </h2>
        <form onSubmit={generateScreening} className="flex flex-col flex-1">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full flex-1 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none font-mono text-sm"
            placeholder="Describe the proposed plant modification in detail...&#10;&#10;Example: Replacement of the existing analog feedwater flow controllers with digital controllers. The new digital controllers will interface with the existing valve actuators but introduce a new software-based control algorithm..."
          />
          <button
            type="submit"
            disabled={loading || !description.trim()}
            className="mt-4 w-full bg-amber-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
          >
            {loading ? <><Loader2 className="animate-spin" size={20} /> Analyzing UFSAR & Generating Draft...</> : 'Generate 50.59 Screening Draft'}
          </button>
        </form>
      </div>

      {/* Output Section */}
      <div className="bg-gray-50 rounded-lg border border-gray-200 shadow-sm overflow-hidden flex flex-col h-full relative">
        <div className="bg-gray-200 px-6 py-3 border-b border-gray-300 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-800">Preliminary Draft</h2>
          {result && (
            <button className="flex items-center gap-2 text-sm bg-white border border-gray-300 px-3 py-1.5 rounded hover:bg-gray-50 transition">
              <FileDown size={16} /> Export PDF
            </button>
          )}
        </div>
        <div className="p-6 flex-1 overflow-y-auto">
          {!result && !loading && (
            <div className="h-full flex items-center justify-center text-gray-400 text-center">
              <p>Enter a modification description to generate a screening draft.</p>
            </div>
          )}
          {loading && (
            <div className="h-full flex flex-col items-center justify-center text-gray-500">
              <Loader2 className="animate-spin mb-4" size={32} />
              <p>Searching design basis documents...</p>
            </div>
          )}
          {result && (
            <div className="space-y-6 text-sm text-gray-800">
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded text-yellow-800 font-semibold text-center mb-6">
                {result.preliminary_warning}
              </div>

              <div>
                <h3 className="font-bold text-lg border-b pb-1 mb-2">1. Applicability Determination</h3>
                <p>{result.applicability_determination}</p>
              </div>

              <div>
                <h3 className="font-bold text-lg border-b pb-1 mb-2">2. Affected Design Functions</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {result.affected_design_functions?.length > 0 ? 
                    result.affected_design_functions.map((f: string, i: number) => <li key={i}>{f}</li>) : 
                    <li className="text-gray-500 italic">None identified in mock response</li>}
                </ul>
              </div>

              <div>
                <h3 className="font-bold text-lg border-b pb-1 mb-2">3. UFSAR Cross-References</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {result.ufsar_cross_references?.length > 0 ? 
                    result.ufsar_cross_references.map((r: string, i: number) => <li key={i}>{r}</li>) :
                    <li className="text-gray-500 italic">None identified in mock response</li>}
                </ul>
              </div>

              {result.citations && result.citations.length > 0 && (
                <div className="pt-4 mt-8 border-t border-gray-300">
                  <h3 className="font-bold text-lg mb-2">Sources</h3>
                  <CitationTable citations={result.citations} />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}