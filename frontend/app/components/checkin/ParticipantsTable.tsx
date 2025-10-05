'use client';

export interface Participant {
  id: number;
  name: string;
  ticketType: string;
  uniqueCode: string;
  checkedIn: boolean;
}

interface ParticipantsTableProps {
  participants: Participant[];
  onToggleCheckin: (participantId: number) => void;
}

export default function ParticipantsTable({ participants, onToggleCheckin }: ParticipantsTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-neutral-400">
        <thead>
          <tr>
            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-white">Check-in</th>
            <th className="px-3 py-3.5 text-left text-sm font-semibold text-white">Participante</th>
            <th className="px-3 py-3.5 text-left text-sm font-semibold text-white">Tipo Ingresso</th>
            <th className="px-3 py-3.5 text-left text-sm font-semibold text-white">Nº do Ingresso</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-400">
          {participants.map((person) => (
            <tr key={person.id}>
              <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm">
                <input
                  type="checkbox"
                  checked={person.checkedIn}
                  onChange={() => onToggleCheckin(person.id)}
                  className="h-5 w-5 rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
              </td>
              <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-white">{person.name}</td>
              <td className="whitespace-nowrap px-3 py-4 text-sm text-white">{person.ticketType}</td>
              <td className="whitespace-nowrap px-3 py-4 text-sm text-white font-mono">{person.uniqueCode}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}