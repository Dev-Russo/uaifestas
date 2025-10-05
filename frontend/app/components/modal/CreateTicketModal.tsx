'use client';
import { useState, FormEvent } from 'react';

interface CreateTicketModalProps {
  isOpen: boolean;
  onClose: () => void;
  eventId: string;
  onTicketCreated: () => void; // recarregar a lista de ingressos
}

export default function CreateTicketModal({ isOpen, onClose, eventId, onTicketCreated }: CreateTicketModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [stock, setStock] = useState(0);
  const [price, setPrice] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Se o modal não estiver aberto, não renderiza nada
  if (!isOpen) return null;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');

    const requestBody = {
      name,
      description,
      stock,
      price,
      image_url: "" // Enviando um valor dummy como placeholder
    };

    const url = `http://127.0.0.1:8000/products/?event_id=${eventId}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Falha ao criar ingresso.');
      }
      
      alert('Ingresso criado com sucesso!');
      onTicketCreated(); // Avisa a página principal para recarregar a lista
      onClose(); // Fecha o modal
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-neutral-800/80 z-50 flex justify-center items-center">
      {/* Conteúdo*/}
      <div className="bg-white dark:bg-neutral-800 rounded-lg shadow-xl p-6 w-full max-w-lg">
        <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Criar Novo Ingresso</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Campos do formulário */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Ingresso (ex: Lote 1)</label>
            <input type="text" id="name" value={name} onChange={e => setName(e.target.value)} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
          </div>
          <div>
            <label htmlFor="stock" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Quantidade Disponível</label>
            <input type="number" id="stock" value={stock} onChange={e => setStock(parseInt(e.target.value, 10))} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
          </div>
          <div>
            <label htmlFor="price" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Preço (R$)</label>
            <input type="number" step="0.01" id="price" value={price} onChange={e => setPrice(parseFloat(e.target.value))} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição (Opcional)</label>
            <textarea id="description" value={description} onChange={e => setDescription(e.target.value)} rows={3} className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm"></textarea>
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {/* Botões de Ação */}
          <div className="flex justify-end gap-4 pt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-neutral-700 hover:bg-gray-200">Cancelar</button>
            <button type="submit" disabled={isLoading} className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 disabled:opacity-50">
              {isLoading ? 'Salvando...' : 'Salvar Ingresso'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}