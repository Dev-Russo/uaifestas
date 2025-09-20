// app/login/page.tsx
"use client";

import { useState, FormEvent } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  // --- 1. Adicionamos o estado para o checkbox aqui ---
  const [rememberMe, setRememberMe] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);

    // Agora você tem acesso ao estado do checkbox aqui
    console.log('Tentando fazer login com:', { email, password, rememberMe });

    // ===================================================================
    // AQUI VOCÊ FARIA A CHAMADA PARA A SUA API FASTAPI
    // Você pode enviar o valor de "rememberMe" junto com os dados de login
    // ===================================================================
    try {
      // ... sua lógica de chamada de API
    } catch (err) {
      console.error('Erro no login:', err);
      setError('Falha ao fazer login. Verifique seu e-mail e senha.');
    }
    // ===================================================================
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <h2 className="mb-6 text-center text-2xl font-bold text-gray-900">
          Acesse sua conta
        </h2>
        <form onSubmit={handleSubmit}>
          {/* Campo de Email */}
          <div className="mb-4">
            {/* ... (código do input de email) ... */}
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email" id="email" name="email" value={email}
              onChange={(e) => setEmail(e.target.value)} required
              className="mt-1 block w-full rounded-md bg-gray-100 border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-solid focus:outline-green-400 focus:ring-gray-500 placeholder:text-gray-400 text-gray-700"
              placeholder="seuemail@exemplo.com"
            />
          </div>

          {/* Campo de Senha */}
          <div className="mb-6">
            {/* ... (código do input de senha) ... */}
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Senha
            </label>
            <input
              type="password" id="password" name="password" value={password}
              onChange={(e) => setPassword(e.target.value)} required
              className="mt-1 block w-full rounded-md bg-gray-100 border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-solid focus:outline-green-400 focus:ring-gray-500 placeholder:text-gray-400 text-gray-700"
              placeholder="********"
            />
          </div>

          {/* Seção Lembre-se de mim e Esqueceu a senha */}
          <div className="mb-6 flex items-center justify-between">
            {/* --- 2. Todo o JSX do checkbox foi colocado aqui --- */}
            <label className="flex cursor-pointer items-center gap-2">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={() => setRememberMe(!rememberMe)}
                className="peer sr-only"
              />
              <div
                className="
                  flex h-5 w-5 items-center justify-center rounded-md border-2 border-gray-200 
                  bg-white transition-all
                  peer-checked:border-green-400 peer-checked:bg-green-400"
              >
                {/* Ícone SVG diretamente inline */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={3}
                  stroke="currentColor"
                  className="h-3 w-3 text-white opacity-0 transition-opacity peer-checked:opacity-100"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              </div>
              <span className="select-none text-sm font-medium text-gray-700">
                Lembre-se de mim
              </span>
            </label>

            <a href="#" className="text-sm font-medium text-gray-600 hover:text-green-600 focus:ring-1 focus:ring-green-500 focus:ring-offset-2 rounded-md">
              Esqueceu a senha?
            </a>
          </div>

          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Botão de Login */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2"
            >
              Entrar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}