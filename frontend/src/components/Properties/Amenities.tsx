import { amenities } from "@/utils/amenities";
import Title from "./Title";
import Image from "next/image";

function Amenities({ amenityList }: { amenityList: string[] }) {
  return (
    <div>
      <Title text="What this place offers" />
      <div>
        {amenityList.map((name) => {
          const amenity = amenities.find((amenity) => amenity.name === name);
          const Icon = amenity?.icon;

          if (!amenity) return null;
          return (
            <div key={amenity.name} className="flex items-center gap-x-4 mb-2 ">
              {Icon && <Icon className="h-6 w-6 text-primary" />}
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
