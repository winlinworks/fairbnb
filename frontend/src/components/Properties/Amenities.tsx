import { Amenity } from "@/utils/amenities";
import Title from "./Title";
import Image from "next/image";

function Amenities({ amenities }: { amenities: Amenity[] }) {
  const noAmenities = amenities.every((amenity) => !amenity.selected);

  if (noAmenities) return null;

  return (
    <div>
      <Title text="What this place offers" />
      <div>
        {amenities.map((amenity) => {
          if (!amenity.selected) return null;
          return (
            <div key={amenity.name} className="flex items-center gap-x-4 mb-2 ">
              <Image
                src={amenity.icon as unknown as string}
                alt={amenity.name}
                width={20}
                height={20}
                className="h-6 w-6 text-primary"
              />
              <span className="font-light text-sm capitalize">
                {amenity.name}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Amenities;
