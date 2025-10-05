'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import ProgressCircle from '@/app/components/checkin/ProgressCircle';
import ParticipantsTable, { Participant } from '@/app/components/checkin/ParticipantsTable';
import { QrCode } from 'lucide-react';

// Dummy data
const DUMMY_PARTICIPANTS: Participant[] = [
  { id: 1, name: 'Ana Luiza Alves Santana', ticketType: 'Lote Promocional', uniqueCode: '672845092999', checkedIn: true },
  { id: 2, name: 'Ana Lara Monteiro Queiroz', ticketType: 'Lote Promocional', uniqueCode: '8519692470722', checkedIn: true },
  { id: 3, name: 'Milena Ester de Almeida', ticketType: 'Primeiro Lote', uniqueCode: '7517332667878', checkedIn: false },
  { id: 4, name: 'Carlos Flores', ticketType: 'Cortesia', uniqueCode: '6334885269668', checkedIn: true },
  { id: 5, name: 'Miguel Ferreira', ticketType: 'Segundo Lote', uniqueCode: '3210059223723', checkedIn: false },
];

// Dummy data
const DUMMY_BREAKDOWN = {
  "Lote Promocional": { checked: 2, total: 2 },
  "Primeiro Lote": { checked: 0, total: 1 },
  "Cortesia": { checked: 1, total: 1 },
  "Segundo Lote": { checked: 0, total: 1 },
};


export default function CheckinPage() {
  const params = useParams();
  const eventId = params.id as string;
  const [participants, setParticipants] = useState<Participant[]>(DUMMY_PARTICIPANTS);

  const handleToggleCheckin = (participantId: number) => {
    setParticipants(
      participants.map(p =>
        p.id === participantId ? { ...p, checkedIn: !p.checkedIn } : p
      )
    );
  };

  // Calcula os totais usando useMemo
  const { checkedInCount, totalCount } = useMemo(() => {
    const checkedIn = participants.filter(p => p.checkedIn).length;
    return { checkedInCount: checkedIn, totalCount: participants.length };
  }, [participants]);


  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Check-in dos Participantes</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <div className="lg:col-span-2 bg-neutral-700 p-6 rounded-lg shadow-md">
          <div className="flex justify-between items-center mb-6">
            <input 
              type="text" 
              placeholder="Pesquise pelo nome, pedido ou Nº do Ingresso"
              className="w-full max-w-xs rounded-md bg-neutral-700 border-neutral-600"
            />
            <Link 
              href={`/dashboard/gerenciar-evento/${eventId}/check-in/validar-qrcode`}
              className="flex items-center gap-2 px-4 py-2 font-bold text-white bg-green-600 rounded-lg hover:bg-green-700"
            >
              <QrCode size={20} />
              Validar QR Code
            </Link>
          </div>
          <ParticipantsTable participants={participants} onToggleCheckin={handleToggleCheckin} />
          {/* Adicionar paginação aqui no futuro */}
        </div>

        {/* Coluna da Sidebar (Direita) */}
        <div className="lg:col-span-1 space-y-8">
          <div className="bg-neutral-700 p-6 rounded-lg shadow-md">
            <ProgressCircle value={checkedInCount} total={totalCount} />
          </div>

          <div className="bg-neutral-700 p-6 rounded-lg shadow-md">
            <h3 className="font-semibold text-lg mb-4 text-white">Check-ins por Lote</h3>
            <div className="space-y-4">
              {Object.entries(DUMMY_BREAKDOWN).map(([lote, data]) => {
                const percentage = data.total > 0 ? (data.checked / data.total) * 100 : 0;
                return (
                  <div key={lote}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-300">{lote}</span>
                      <span className="text-gray-400">{data.checked} / {data.total}</span>
                    </div>
                    <div className="w-full bg-neutral-700 rounded-full h-2.5">
                      <div className="bg-green-500 h-2.5 rounded-full" style={{ width: `${percentage}%` }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}