'use client';

interface ProgressCircleProps {
  value: number;
  total: number;
  size?: number; // Tamanho do círculo em pixels
  strokeWidth?: number; // Largura da linha
}

export default function ProgressCircle({ value, total, size = 180, strokeWidth = 16 }: ProgressCircleProps) {
  if (total === 0) total = 1; // Evita divisão por zero
  
  const percentage = Math.round((value / total) * 100);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          {/* Círculo de fundo */}
          <circle
            stroke="currentColor"
            className="text-neutral-700"
            fill="transparent"
            strokeWidth={strokeWidth}
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
          {/* Círculo de progresso */}
          <circle
            stroke="currentColor"
            className="text-green-500"
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
        </svg>
        {/* Texto no meio */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-4xl font-bold text-white">{percentage}%</span>
        </div>
      </div>
      <div className="text-center mt-4">
        <p className="text-lg font-semibold text-white">Check-ins realizados</p>
        <p className="text-sm text-gray-400">{`${value} de ${total} validados`}</p>
      </div>
    </div>
  );
}