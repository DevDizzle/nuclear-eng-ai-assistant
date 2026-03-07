import { FileText, MessageSquare, ShieldAlert } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  return (
    <div className="flex flex-col h-full overflow-y-auto">
      <div className="p-8 max-w-5xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-2">Nuclear Engineering AI Assistant</h1>
        <p className="text-gray-600 mb-8">Purpose-built for nuclear power plant engineering teams.</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-1">Total Documents</h3>
            <p className="text-3xl font-bold text-blue-600">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-1">Recent Queries</h3>
            <p className="text-3xl font-bold text-green-600">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-1">System Status</h3>
            <p className="text-3xl font-bold text-emerald-600">Online</p>
          </div>
        </div>

        <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link href="/documents" className="flex items-center gap-4 bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:border-blue-500 transition">
            <div className="bg-blue-100 p-3 rounded-full text-blue-600">
              <FileText size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Upload Documents</h3>
              <p className="text-sm text-gray-500">Ingest PDFs for RAG retrieval</p>
            </div>
          </Link>
          <Link href="/query" className="flex items-center gap-4 bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:border-green-500 transition">
            <div className="bg-green-100 p-3 rounded-full text-green-600">
              <MessageSquare size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Ask a Question</h3>
              <p className="text-sm text-gray-500">Query engineering documents with citations</p>
            </div>
          </Link>
          <Link href="/screening" className="flex items-center gap-4 bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:border-amber-500 transition">
            <div className="bg-amber-100 p-3 rounded-full text-amber-600">
              <ShieldAlert size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">10 CFR 50.59 Screening</h3>
              <p className="text-sm text-gray-500">Generate preliminary screening drafts</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}