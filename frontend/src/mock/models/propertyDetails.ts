import { profiles } from "./profiles";
import { properties } from "./properties";
import { PropertyDetail, Profile } from "../types/types";
const profileHash: Record<string, Profile> = profiles.reduce(
  (acc, profile) => {
    acc[profile.id] = profile;
    return acc;
  },
  {} as Record<string, Profile>
);

export const propertyDetails: PropertyDetail[] = properties.map((property) => {
  const associatedProfile = profileHash[property.profileId];

  return {
    id: property.id,
    name: property.name,
    tagline: property.tagline,
    image: property.image,
    country: property.country,
    description: property.description,
    price: property.price,
    guests: property.guests,
    bedrooms: property.bedrooms,
    beds: property.beds,
    baths: property.baths,
    amenities: property.amenities,
    profileId: property.profileId,
    firstName: associatedProfile.firstName,
    profileImage: associatedProfile.profileImage,
    profileCreatedAt: associatedProfile.createdAt,
  };
});
