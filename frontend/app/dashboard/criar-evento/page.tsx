'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import DatePicker from "react-datepicker";
import { ptBR } from "date-fns/locale";
import "react-datepicker/dist/react-datepicker.css";
//import Cookies from "js-cookie";

export default function CriarEventoPage() {
    const [nomeEvento, setnomeEvento] = useState('');
    const [descricao, setDescricao] = useState('');
    const [dataInicio, setDataInicio] = useState<Date | null>(null);
    const [dataFim, setDataFim] = useState<Date | null>(null);
    const [imagemFile, setImagemFile] = useState<File | null>(null);
    const [cep, setCep] = useState('');
    const [rua, setRua] = useState('');
    const [numero, setNumero] = useState('');
    const [bairro, setBairro] = useState('');
    const [cidade, setCidade] = useState('');
    const [visibilidade, setVisibilidade] = useState<'publico' | 'privado'>('publico');
    const [aceiteTermos, setAceiteTermos] = useState(false);
    const [formError, setFormError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    function validarCampos() {
        if (
            !nomeEvento.trim() ||
            !descricao.trim() ||
            !imagemFile ||
            !dataInicio ||
            !dataFim ||
            !cep.trim() ||
            !rua.trim() ||
            !numero.trim() ||
            !bairro.trim() ||
            !cidade.trim() ||
            !aceiteTermos
        ) {
            setFormError("Preencha todos os campos obrigatórios e aceite os termos.");
            return false;
        }
        setFormError(null);
        return true;
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!validarCampos()) return;
        setIsLoading(true);
        setFormError(null);

        let imageUrl = '';
        if (imagemFile) {
        imageUrl = URL.createObjectURL(imagemFile);
        //fazer upload do arquivo e usar a URL retornada pelo backend
        }

        const eventData = {
        name: nomeEvento,
        description: descricao,
        street: rua,
        cep: cep,
        neighborhood: bairro,
        number: numero,
        city: cidade,
        created: dataInicio ? dataInicio.toISOString() : new Date().toISOString(),
        event_date: dataInicio ? dataInicio.toISOString() : new Date().toISOString(),
        image_url: imageUrl,
        status: visibilidade === 'publico' ? 'active' : 'inactive'
        };

        const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        //const token = Cookies.get('auth_token');

        try {
            // ======================= VERSÃO PROVISÓRIA) =======================
            
            const response = await fetch('http://127.0.0.1:8000/events/', {
                method: 'POST',
                headers: headers, 
                body: JSON.stringify(eventData),
            });

            // ======================= VERSÃO FINAL (HttpOnly) =======================
            // O navegador enviará o cookie HttpOnly automaticamente.
            /*
            const response = await fetch('http://127.0.0.1:8000/events/', {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });
            */
            // ====================================================================================

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Erro ao criar evento.');
            }
            
            const newEvent = await response.json();
            alert('Evento criado com sucesso!');
            router.push(`/dashboard`);

        } catch (error: any) {
            console.error('Erro ao criar evento:', error);
            setFormError(error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h1 className="text-3xl px-1 font-bold mb-6 dark:bg-neutral-800 rounded-lg space-y-12 space-x-12">Criar Novo Evento</h1>
            <form className="space-y-6 bg-white dark:bg-neutral-800 p-8 rounded-lg shadow-md" onSubmit={handleSubmit}>

                {/* Informações Básicas */}
                <div className="border-b border-gray-700 pb-8">
                    <h2 className="text-2xl font-semibold leading-7 text-gray-900 dark:text-white">
                        Informações Básicas
                    </h2>
                    <p className="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-400">
                        Preencha as principais informações do seu evento.
                    </p>
                    <div className="mt-6 grid grid-cols-1 gap-y-6">
                        <label className="text-lg font-semibold leading-7 text-gray-900 dark:text-white">Nome do Evento *</label>
                        <input
                            type="text" id="nomeEvento" name="nomeEvento" required
                            value={nomeEvento}
                            onChange={e => setnomeEvento(e.target.value)}
                            className="block w-1/2 border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                            placeholder="Nome do Evento*"
                        />

                        <label className="text-lg font-semibold leading-7 text-gray-900 dark:text-white">Descrição *</label>
                        <textarea
                            name="descricao" id="descricao" required
                            value={descricao}
                            onChange={e => setDescricao(e.target.value)}
                            className="mt-1 block w-1/2 duration-300 resize-none rounded-md border-gray-300 outline-neutral-700 outline-2 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-solid focus:outline-green-400 focus:ring-gray-500 placeholder:text-gray-400 text-gray-700 dark:text-white"
                            placeholder="Insira aqui a descrição do seu evento"
                        />

                        {/* Imagem de capa */}
                        <label className="text-lg font-semibold leading-7 text-gray-900 dark:text-white">Imagem de Capa *</label>
                        <input
                            type="file"
                            id="imagem"
                            name="imagem"
                            accept="image/*"
                            required
                            onChange={e => {
                                const file = e.target.files?.[0] ?? null;
                                setImagemFile(file);
                            }}
                            className="block w-100 border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0 bg-white dark:bg-neutral-700"
                        />
                        {imagemFile && (
                            <div className="mt-2">
                                <span className="text-xs text-gray-600 dark:text-gray-400">Arquivo selecionado: {imagemFile.name}</span>
                            </div>
                        )}

                        {/* Data do evento */}
                        <div className="flex flex-col w-1/2 space-y-4">
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Data e hora de início *</label>
                            <DatePicker
                                selected={dataInicio}
                                onChange={(date) => setDataInicio(date)}
                                showTimeSelect
                                timeFormat="HH:mm"
                                timeIntervals={15}
                                dateFormat="Pp"
                                locale={ptBR}
                                placeholderText="Selecione data e hora de início"
                                className="mt-1 w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-green-400 focus:ring focus:ring-green-200 dark:bg-neutral-700 dark:text-white dark:placeholder:text-gray-400"
                                required
                            />
                        </div>
                        <div className="flex flex-col w-1/2 space-y-4">
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Data e hora de término *</label>
                            <DatePicker
                                selected={dataFim}
                                onChange={(date) => setDataFim(date)}
                                showTimeSelect
                                timeFormat="HH:mm"
                                timeIntervals={15}
                                dateFormat="Pp"
                                locale={ptBR}
                                placeholderText="Selecione data e hora de término"
                                className="mt-1 w-full rounded-md border-gray-300 px-3 py-2 shadow-sm focus:border-green-400 focus:ring focus:ring-green-200 dark:bg-neutral-700 dark:text-white dark:placeholder:text-gray-400"
                                required
                            />
                        </div>
                    </div>
                </div>

                {/* Local do Evento */}
                <div className="border-b border-gray-700 pb-8">
                    <h2 className="text-2xl font-semibold leading-7 text-gray-900 dark:text-white">
                        Local do Evento
                    </h2>
                    <p className="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-400">
                        Informe o endereço do evento.
                    </p>
                    <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-4 w-full">
                        <div>
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">CEP *</label>
                            <input
                                type="text"
                                id="cep"
                                name="cep"
                                required
                                value={cep}
                                onChange={e => setCep(e.target.value)}
                                className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                                placeholder="CEP"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Rua *</label>
                            <input
                                type="text"
                                id="rua"
                                name="rua"
                                required
                                value={rua}
                                onChange={e => setRua(e.target.value)}
                                className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                                placeholder="Rua"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Número *</label>
                            <input
                                type="text"
                                id="numero"
                                name="numero"
                                required
                                value={numero}
                                onChange={e => setNumero(e.target.value)}
                                className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                                placeholder="Número"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Bairro *</label>
                            <input
                                type="text"
                                id="bairro"
                                name="bairro"
                                required
                                value={bairro}
                                onChange={e => setBairro(e.target.value)}
                                className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                                placeholder="Bairro"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-gray-900 dark:text-white">Cidade *</label>
                            <input
                                type="text"
                                id="cidade"
                                name="cidade"
                                required
                                value={cidade}
                                onChange={e => setCidade(e.target.value)}
                                className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 placeholder:text-gray-400 text-gray-700 dark:text-white focus:border-transparent focus:ring-transparent focus:outline-0"
                                placeholder="Cidade"
                            />
                        </div>
                    </div>
                </div>

                {/* Configurações Técnicas */}
                <div>
                    <h2 className="text-2xl font-semibold leading-7 text-gray-900 dark:text-white">
                        Configurações Técnicas
                    </h2>
                    <p className="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-400">
                        Defina opções avançadas do evento.
                    </p>
                    <div className="mt-6 flex flex-col w-1/2 space-y-4">
                        <label className="text-sm font-semibold text-gray-900 dark:text-white">Visibilidade *</label>
                        <select
                            value={visibilidade}
                            onChange={e => setVisibilidade(e.target.value as 'publico' | 'privado')}
                            required
                            className="block w-full border-b-2 duration-300 rounded-md focus:border-b-green-400 dark:border-neutral-900 px-3 py-1 text-gray-700 dark:text-white bg-white dark:bg-neutral-700"
                        >
                            <option value="publico">Público</option>
                            <option value="privado">Privado</option>
                        </select>
                    </div>
                </div>

                {/* Termos de Uso */}
                <div className="mt-8 flex items-center">
                    <input
                        type="checkbox"
                        id="aceiteTermos"
                        checked={aceiteTermos}
                        onChange={e => setAceiteTermos(e.target.checked)}
                        required
                        className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                    />
                    <label htmlFor="aceiteTermos" className="ml-2 block text-sm text-gray-900 dark:text-white">
                        Concordo com os <a href="/termos" target="_blank" className="underline text-green-600">termos de uso</a> e obrigações legais *
                    </label>
                </div>

                {/* Erro de validação */}
                {formError && (
                    <div className="mt-4 text-red-600 text-sm font-semibold">
                        {formError}
                    </div>
                )}

                {/* Botão de continuar/concluir */}
                <div className="mt-8 flex justify-end">
                    <button
                        type="submit"
                        className="px-6 py-2 bg-green-600 text-white font-bold rounded-md hover:bg-green-700 transition-colors"
                    >
                        Continuar
                    </button>
                </div>
            </form>
        </div>
    );
}