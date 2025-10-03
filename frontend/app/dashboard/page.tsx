'use client'; 

import { useState, useMemo, useEffect } from 'react';
import EventCard from '@/app/components/EventCard';
import EventFilters from '@/app/components/EventFilters';

export default function DashboardPage({ events }: { events: any[] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('upcoming'); // Valor padrão do filtro
  const [eventos, setEventos] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEvents() {
      try {
        const response = await fetch("http://127.0.0.1:8000/events/");
        if (!response.ok) throw new Error('Erro ao buscar eventos');
        const data = await response.json();
        setEventos(data);
      } catch (err: any){
        setError(err.message);
      }
    }
    fetchEvents();
  }, []);

  const mappedEvents = useMemo(() => {
    return eventos.map((event) => {
      const eventDate = new Date(event.event_date);
      const now = new Date();
      const status = eventDate >= now ? 'upcoming' : 'past';
      const formattedDate = eventDate.toLocaleDateString('pt-BR');
      return {
        id: event.id,
        name: event.name,
        date: formattedDate,
        status,
      };
    });
  }, [eventos]);

  const filteredEvents = useMemo(() => {
    return mappedEvents.filter((event) => {
      const matchesSearch = event.name.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesFilter =
        filter === 'all' ||
        (filter === 'upcoming' && event.status === 'upcoming') ||
        (filter === 'past' && event.status === 'past');

      return matchesSearch && matchesFilter;
    });
  }, [mappedEvents, searchTerm, filter]);

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-4 text-green-400 ">Meus Eventos</h2>
      <EventFilters
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        filter={filter}
        setFilter={setFilter}
      />
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {filteredEvents.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredEvents.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">Nenhum evento encontrado.</p>
        </div>
      )}
    </div>
  );
}