export interface Profile {
  id: string;
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  profileImage: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Property {
  id: string;
  name: string;
  tagline: string;
  category: string;
  image: string;
  country: string;
  description: string;
  price: number;
  guests: number;
  bedrooms: number;
  beds: number;
  baths: number;
  amenities: string[];
  createdAt: Date;
  updatedAt: Date;
  profileId: string;
}

export interface PropertyDetail {
  // property info
  id: string;
  name: string;
  tagline: string;
  image: string;
  country: string;
  description: string;
  price: number;
  guests: number;
  bedrooms: number;
  beds: number;
  baths: number;
  amenities: string[];

  // profile info
  profileId: string;
  firstName: string;
  profileImage: string;
  profileCreatedAt: Date;
}
