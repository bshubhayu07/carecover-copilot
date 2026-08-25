export interface Hospital {
  hospital_id: string;
  hospital_name: string;
  city: string;
  specialties: string[];
  in_network: boolean;
  room_types_available: string[];
  distance_km?: number;
  contact_number?: string;
}

export interface CityCoords {
  lat: number;
  lon: number;
}
