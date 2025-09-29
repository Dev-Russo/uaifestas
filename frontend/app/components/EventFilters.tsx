import { Search } from 'lucide-react';

interface EventFiltersProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  filter: string;
  setFilter: (filter: string) => void;
}

export default function EventFilters({
  searchTerm,
  setSearchTerm,
  filter,
  setFilter,
}: EventFiltersProps) {
  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6">
      <div className="relative flex-grow">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
        <input
          type="text"
          placeholder="Pesquisar por nome do evento..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-md bg-white dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-green-400"
        />
      </div>
      <select
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-md bg-white dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-green-400"
      >
        <option value="upcoming">Próximos eventos</option>
        <option value="past">Eventos passados</option>
        <option value="all">Todos</option>
      </select>
    </div>
  );
}