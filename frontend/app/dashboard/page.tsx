'use client'; 

import { useState, useMemo } from 'react';
import EventCard from '@/app/components/EventCard';
import EventFilters from '@/app/components/EventFilters';

// Dummy data (substituir por chamadas da API)
const EVENTOS = [
  { id: 1, name: 'Festival de Rock Independente', date: '15/10/2025', status: 'upcoming' as const },
  { id: 2, name: 'Show de Stand-up Comedy', date: '22/10/2025', status: 'upcoming' as const },
  { id: 3, name: 'Feira de Tecnologia e Inovação', date: '01/08/2025', status: 'past' as const },
  { id: 4, name: 'Concerto de Jazz & Blues', date: '05/11/2025', status: 'upcoming' as const },
  { id: 5, name: 'Workshop de Marketing Digital', date: '10/09/2025', status: 'past' as const },
  { id: 6, name: 'Festival Gastronômico Local', date: '12/12/2025', status: 'upcoming' as const },
];

export default function DashboardPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('upcoming'); // Valor padrão do filtro

  const filteredEvents = useMemo(() => {
    return EVENTOS.filter((event) => {
      const matchesSearch = event.name.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesFilter =
        filter === 'all' ||
        (filter === 'upcoming' && event.status === 'upcoming') ||
        (filter === 'past' && event.status === 'past');

      return matchesSearch && matchesFilter;
    });
  }, [searchTerm, filter]);

  return (
    <div>
      <h2 className="text-3xl font-bold mb-4 text-green-400 ">Meus Eventos</h2>
      
      <EventFilters
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        filter={filter}
        setFilter={setFilter}
      />

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