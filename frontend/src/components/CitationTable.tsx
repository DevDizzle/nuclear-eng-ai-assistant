import React from 'react';

interface Citation {
  source_document: string;
  page_number: number;
  relevant_passage: string;
  confidence: string;
}

export default function CitationTable({ citations }: { citations: Citation[] }) {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="mt-4 border border-gray-200 rounded-lg overflow-hidden text-sm bg-white">
      <div className="bg-gray-100 px-4 py-2 font-semibold text-gray-700 border-b border-gray-200">
        Supporting Citations
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 border-b">Source Document</th>
              <th className="px-4 py-2 border-b">Page</th>
              <th className="px-4 py-2 border-b">Relevant Passage</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {citations.map((cite, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-4 py-2 whitespace-nowrap font-medium text-blue-600">{cite.source_document}</td>
                <td className="px-4 py-2 whitespace-nowrap">{cite.page_number}</td>
                <td className="px-4 py-2 text-gray-600 line-clamp-3" title={cite.relevant_passage}>
                  {cite.relevant_passage}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}