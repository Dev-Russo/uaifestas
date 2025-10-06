// app/dashboard/gerenciar-evento/[id]/ingressos/page.tsx

'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Ticket, PlusCircle, Pencil, Trash2 } from 'lucide-react';
import CreateTicketModal from '@/app/components/modal/CreateTicketModal';
import StatCard from '@/app/components/StatCard';

// Interface para os dados do ingresso
interface TicketData {
  id: number;
  name: string;
  stock: number;
  price: number;
  status: 'active' | 'inactive';
  // Adicionar 'sold' (vendidos)
}

export default function GerenciarIngressosPage() {
  const params = useParams();
  const eventId = params.id as string;
  
  const [tickets, setTickets] = useState<TicketData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchTickets = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
      const response = await fetch(`http://127.0.0.1:8000/events/${eventId}/products`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Falha ao buscar ingressos.');
      const data = await response.json();
      setTickets(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (eventId) {
      fetchTickets();
    }
  }, [eventId]);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Gerenciar Ingressos</h1>

      {/* Seção de Resumo*/}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Ingressos Aprovados" value={0} icon={Ticket} />
        {/* outros cards de status aqui */}
      </div>

      {/* Seção de Gerenciamento */}
      <div className="bg-white dark:bg-neutral-800 p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Tipos de Ingresso</h2>
          <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700">
            <PlusCircle size={16} />
            Novo Ingresso
          </button>
        </div>

        {/* Tabela de Ingressos */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
            <thead className="bg-gray-50 dark:bg-neutral-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendido / Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Preço</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ações</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-neutral-800 divide-y divide-gray-200 dark:divide-neutral-700">
              {isLoading ? (
                <tr><td colSpan={4} className="text-center py-4">Carregando ingressos...</td></tr>
              ) : error ? (
                <tr><td colSpan={4} className="text-center py-4 text-red-500">{error}</td></tr>
              ) : tickets.map((ticket) => (
                <tr key={ticket.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium">{ticket.name}</td>

                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        ticket.status === 'active' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                        : 'bg-gray-100 text-gray-800 dark:bg-neutral-700 dark:text-gray-300'
                    }`}>
                      <svg className={`-ml-0.5 mr-1.5 h-2 w-2 ${
                          ticket.status === 'active' ? 'text-green-400' : 'text-gray-400'
                      }`} fill="currentColor" viewBox="0 0 8 8">
                        <circle cx={4} cy={4} r={3} />
                      </svg>
                      {ticket.status === 'active' ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>

                  <td className="px-6 py-4 whitespace-nowrap">{`0 / ${ticket.stock}`}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{`R$ ${ticket.price.toFixed(2)}`}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button className="text-blue-500 hover:text-blue-700 mr-4"><Pencil size={16} /></button>
                    <button className="text-red-500 hover:text-red-700"><Trash2 size={16} /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* O Modal é renderizado aqui, mas só aparece quando isModalOpen for true */}
      <CreateTicketModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        eventId={eventId}
        onTicketCreated={fetchTickets}
      />
    </div>
  );
}