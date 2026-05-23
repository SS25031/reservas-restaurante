export interface AdminUser {
	id: number;
	email: string;
	restaurant_id: number;
}

export interface RegistroDisponible {
	disponible: boolean;
}

export type TurnoApi = 'MANANA' | 'TARDE' | 'NOCHE';

export interface Reserva {
	id: number;
	fecha: string;
	turno: TurnoApi;
	turno_label: string;
	numero_mesa: number;
	cliente: string;
	telefono: string;
	email: string;
	personas: number;
	estado: 'activa' | 'cancelada';
}

export interface ReservaCreate {
	cliente: string;
	telefono: string;
	email: string;
	personas: number;
	fecha: string;
	turno: TurnoApi;
}

export interface ReservaUpdate {
	fecha?: string;
	turno?: TurnoApi;
}

export interface OnboardingEstado {
	completado: boolean;
	mesas_count: number;
	turnos_activos: number;
}

export interface ReabrirOnboardingResponse {
	completado: boolean;
}
