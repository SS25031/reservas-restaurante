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

export interface RestaurantConfig {
	id: number;
	nombre: string;
	max_reservas_por_dia: number;
	capacidad_maxima_grupo: number;
	onboarding_completado: boolean;
}

export interface MesaConfig {
	numero: number;
	capacidad: number;
	pos_x: number | null;
	pos_y: number | null;
}

export interface TurnoConfig {
	turno: TurnoApi;
	activo: boolean;
	hora_inicio: string | null;
	hora_fin: string | null;
}

export interface CalendarDayConfig {
	fecha: string;
	cerrado: boolean;
	nota: string | null;
}

export interface CompletarOnboardingResponse {
	completado: boolean;
}

export interface ReabrirOnboardingResponse {
	completado: boolean;
}

export interface PublicRestaurant {
	nombre: string;
	capacidad_maxima_grupo: number;
	acepta_reservas: boolean;
}

export interface TurnoDisponibilidad {
	turno: TurnoApi;
	turno_label: string;
	disponible: boolean;
	mesas_libres: number;
}

export interface Disponibilidad {
	fecha: string;
	personas: number;
	cerrado: boolean;
	nota: string | null;
	acepta_reservas: boolean;
	turnos: TurnoDisponibilidad[];
}
