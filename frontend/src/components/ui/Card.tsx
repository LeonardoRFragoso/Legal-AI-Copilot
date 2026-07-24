import { cn } from '../../lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export default function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn('bg-white rounded-lg shadow-sm border border-gray-200', className)}
      {...props}
    />
  )
}
