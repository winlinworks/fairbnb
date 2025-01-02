import PropertyRating from "@/components/card/PropertyRating";
import BookingCalendar from "@/components/Properties/BookingCalendar";
import BreadCrumbs from "@/components/Properties/BreadCrumbs";
import ImageContainer from "@/components/Properties/ImageContainer";
import ShareButton from "@/components/Properties/ShareButton";
import { fetchPropertyDetails } from "@/lib/api/fetchData";
import { log } from "console";
import { setDefaultAutoSelectFamily } from "net";
import { redirect } from "next/navigation";

async function PropertyDetailsPage({ params }: { params: { id: number } }) {
  const property = await fetchPropertyDetails(params.id);
  if (!property) redirect("/");
  const { baths, bedrooms, beds, guests } = property;
  const details = { baths, bedrooms, beds, guests };

  return (
    <section>
      <BreadCrumbs name={property.name} />
      <header className="flex justify-between items-center mt-4">
        <h1 className="text-4xl font-bold">{property.tagline}</h1>
        <div className="flex items-center gap-x-4">
          <ShareButton propertyId={property.id} name={property.name} />
          {/* favorite button */}
        </div>
      </header>
      <ImageContainer mainImage={property.image} name={property.name} />
      <section className="lg:grid lg:grid-cols-12 gap-x-12 mt-12">
        <div className="lg:col-span-8">
          <div className="flex gap-x-4 items-center">
            <h1 className="text-xl font-bold">{property.name}</h1>
            <PropertyRating inPage propertyId={property.id} />
          </div>
        </div>
        <div className="lg:col-span-4 flex flex-col items-center">
          <BookingCalendar />
        </div>
        <div className="lg:col-span-8"></div>
      </section>
    </section>
  );
}

export default PropertyDetailsPage;
