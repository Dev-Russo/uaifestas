'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import StatCard from '@/app/components/StatCard';
import { DollarSign, Ticket, Users, BarChart3 } from 'lucide-react';

interface EventDetails {
  id: number;
  name: string;
  description: string;
  event_date: string;
  status: string;
  street: string;
  number: string;
  neighborhood: string;
  city: string;
  cep: string;
}

export default function PainelDoEventoPage() {
  const [event, setEvent] = useState<EventDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const params = useParams();
  const eventId = params.id as string;

  useEffect(() => {
    if (!eventId) return; // Não faz nada se o ID ainda não estiver disponível

    async function fetchEventDetails() {
      try {
        const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');

        if (!token) {
          throw new Error('Usuário não autenticado.');
        }
        const headers = {
          'Authorization': `Bearer ${token}`
        };

        const response = await fetch(`http://127.0.0.1:8000/events/${eventId}`, {
          headers: headers,
        });

        if (response.status === 404) {
          throw new Error('Evento não encontrado.');
        }
        if (!response.ok) {
          throw new Error('Falha ao buscar os detalhes do evento.');
        }

        const data = await response.json();
        setEvent(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
    fetchEventDetails();
  }, [eventId]);

  if (isLoading) {
    return <div>Carregando informações do evento...</div>;
  }

  if (error) {
    return <div className="text-red-500">Erro: {error}</div>;
  }
  
  if (!event) {
    return <div>Evento não encontrado.</div>
  }

    // Dummy data
  const stats = [
    { title: "Receita Total", value: "R$ 0,00", icon: DollarSign },
    { title: "Ingressos Vendidos", value: 0, icon: Ticket },
    { title: "Participantes", value: 0, icon: Users },
    { title: "Visualizações", value: 0, icon: BarChart3 },
  ];


  const formattedDate = new Date(event.event_date).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
   <div>

      <div className="my-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <StatCard 
              key={index} 
              title={stat.title} 
              value={stat.value} 
              icon={stat.icon} 
            />
          ))}
        </div>
      </div>


      <h1 className="text-3xl font-bold">{event.name}</h1>
      {/* dev */}
      <p className="mt-2 text-gray-400">Gerenciando o evento com ID: <strong>{eventId}</strong></p> 
      
      <div className="mt-8 p-6 bg-neutral-900 rounded-lg">
        <h2 className="text-xl font-semibold mb-4 text-green-400">Detalhes do Evento</h2>
        <p><strong className="text-gray-300">Descrição:</strong> {event.description}</p>
        <p className="mt-2"><strong className="text-gray-300">Data:</strong> {formattedDate}</p>
        <p className="mt-2"><strong className="text-gray-300">Status:</strong> <span className="px-2 py-1 text-s font-semibold rounded-full bg-green-900 text-green-200">{event.status}</span></p>
        <div className="mt-4">
          <p className="font-semibold text-gray-300">Localização:</p>
          <p className="text-sm text-gray-400">{event.street}, {event.number} - {event.neighborhood}, {event.city} - CEP: {event.cep}</p>
        </div>
      </div>
    </div>
  );
}