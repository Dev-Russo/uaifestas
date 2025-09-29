interface Event {
  id: number;
  name: string;
  date: string;
  status: 'upcoming' | 'past';
}

interface EventCardProps {
  event: Event;
}

export default function EventCard({ event }: EventCardProps) {
  const isUpcoming = event.status === 'upcoming';
  
  return (
    <div className="bg-white dark:bg-neutral-800 border border-gray-200 dark:border-neutral-700 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-bold">{event.name}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">{event.date}</p>
        </div>
        <span
          className={`px-2 py-1 text-xs font-semibold rounded-full ${
            isUpcoming
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
          }`}
        >
          {isUpcoming ? 'Próximo' : 'Passado'}
        </span>
      </div>
      <div className="mt-4 flex justify-end">
        <button className="px-4 py-2 text-sm shadow-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-400">
          Gerenciar
        </button>
      </div>
    </div>
  );
}