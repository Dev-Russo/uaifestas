'use client';

import { useState } from 'react';
// 1. A importação correta é 'Scanner' (e a tipagem para o resultado)
import { Scanner, IDetectedBarcode } from '@yudiel/react-qr-scanner';
import { useRouter } from 'next/navigation';
import { ArrowLeft, CheckCircle, XCircle } from 'lucide-react';

type ValidationResult = {
  status: 'success' | 'error' | 'info';
  message: string;
} | null;

export default function ValidarQrcodePage() {
  const router = useRouter();
  const [validationResult, setValidationResult] = useState<ValidationResult>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // A lógica de validação no backend continua a mesma
  const validateCodeOnBackend = async (uniqueCode: string) => {
    setIsLoading(true);
    setValidationResult({ status: 'info', message: `Código lido. Validando...` });
    try {
      const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
      const response = await fetch(`http://127.0.0.1:8000/sale/check/${uniqueCode}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Código inválido.');
      setValidationResult({ status: 'success', message: `Check-in de ${data.buyer_name} realizado!` });
    } catch (err: any) {
      setValidationResult({ status: 'error', message: err.message });
    } finally {
      setIsLoading(false);
      setTimeout(() => setValidationResult(null), 5000);
    }
  };

  // 2. A função agora recebe um array 'detectedCodes'
  const handleScan = (detectedCodes: IDetectedBarcode[]) => {
    // 3. Pegamos o primeiro código detectado e seu valor 'rawValue'
    if (detectedCodes.length > 0 && !isLoading) {
      const scannedCode = detectedCodes[0].rawValue;
      validateCodeOnBackend(scannedCode);
    }
  };

  return (
    <div className="relative w-screen h-screen bg-black">
      {/* 4. O componente no JSX é <Scanner> com a prop onScan */}
      <Scanner
        onScan={handleScan}
        onError={(error) => console.log(error?.message)}
        styles={{
            container: { width: '100%', height: '100%', paddingTop: '0' },
            video: { objectFit: 'cover' },
        }}
        // 'constraints' foi substituído por 'videoConstraints' em versões mais recentes
        constraints={{ facingMode: 'environment' }}
      />

      {/* O Overlay e o Banner de Resultado (sem alterações) */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <button 
          onClick={() => router.back()} 
          className="absolute top-4 left-4 p-2 rounded-full bg-black/50 pointer-events-auto z-10"
        >
          <ArrowLeft className="text-white" />
        </button>
        <div className="w-64 h-64 border-4 border-white/50 relative rounded-lg">
          {/* ... (código do retículo de scan) ... */}
        </div>
        <p className="mt-4 text-white text-lg font-semibold bg-black/50 px-4 py-2 rounded-md">
          Aponte a câmera para o QR Code
        </p>
      </div>

      {validationResult && (
        <div 
          className={`absolute bottom-0 left-0 w-full p-4 text-white text-center font-bold text-lg transition-transform duration-300 z-10 ${
            validationResult.status === 'success' ? 'bg-green-600' : ''
          } ${
            validationResult.status === 'error' ? 'bg-red-600' : ''
          } ${
            validationResult.status === 'info' ? 'bg-blue-600' : ''
          }`}
        >
          <div className="flex items-center justify-center gap-2">
            {validationResult.status === 'success' && <CheckCircle />}
            {validationResult.status === 'error' && <XCircle />}
            {validationResult.message}
          </div>
        </div>
      )}
    </div>
  );
}