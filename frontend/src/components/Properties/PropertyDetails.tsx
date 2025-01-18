import { formatQuantity } from "@/utils/format";

type propertyDetailsProps = {
  details: {
    baths: number;
    bedrooms: number;
    beds: number;
    guests: number;
  };
};

export default function PropertyDetails({
  details: { bedrooms, baths, beds, guests },
}: propertyDetailsProps) {
  return (
    <div className="text-md font-light">
      <span>{formatQuantity(baths, "bath")}&middot;</span>
      <span>{formatQuantity(bedrooms, "bedroom")}&middot;</span>
      <span>{formatQuantity(beds, "bed")}&middot;</span>
      <span>{formatQuantity(guests, "guest")}&middot;</span>
    </div>
  );
}
