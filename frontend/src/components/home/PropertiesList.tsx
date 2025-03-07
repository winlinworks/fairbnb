import PropertyCard from "../card/PropertyCard";
import type { PropertyCardProps } from "@/utils/types";

function PropertiesList({ properties }: { properties: PropertyCardProps[] }) {
  return (
    <section className="mt-4 gap-8 grid sm:grid-cols-2  lg:grid-cols-3  xl:grid-cols-4">
      {Array.isArray(properties) && properties.length > 0 ? (
        properties.map((property) => {
          return <PropertyCard key={property.id} property={property} />;
        })
      ) : (
        <p>No properties available</p>
      )}
    </section>
  );
}

export default PropertiesList;
