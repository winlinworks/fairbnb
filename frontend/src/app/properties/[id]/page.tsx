import PropertyRating from "@/components/card/PropertyRating";
import Amenities from "@/components/Properties/Amenities";
import BookingCalendar from "@/components/Properties/BookingCalendar";
import BreadCrumbs from "@/components/Properties/BreadCrumbs";
import Description from "@/components/Properties/Description";
import ImageContainer from "@/components/Properties/ImageContainer";
import PropertyDetails from "@/components/Properties/PropertyDetails";
import ShareButton from "@/components/Properties/ShareButton";
import UserInfo from "@/components/Properties/UserInfo";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchPropertyDetails, fetchUserInfo } from "@/lib/api/fetchData";
import dynamic from "next/dynamic";
import { redirect } from "next/navigation";

const DynamicMap = dynamic(
  () => import("@/components/Properties/PropertyMap"),
  {
    ssr: false,
    loading: () => <Skeleton className="h-[400px] w-full" />,
  }
);

async function PropertyDetailsPage({ params }: { params: { id: number } }) {
  const property = await fetchPropertyDetails(params.id);

  if (!property) redirect("/");
  const { baths, bedrooms, beds, guests } = property;
  const details = { baths, bedrooms, beds, guests };

  const firstName = property.firstName;
  const profileImage = property.profileImage;

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
          <PropertyDetails details={details} />
          <UserInfo profile={{ profileImage, firstName }} />
          <Separator className="mt-4" />
          <Description description={property.description} />
          <Amenities amenityList={property.amenities} />
        </div>

        <div className="lg:col-span-4 flex flex-col items-center">
          <BookingCalendar />
        </div>
        <div className="lg:col-span-12">
          {" "}
          <Separator className="mt-4" />
          <DynamicMap countryName={property.country} />
        </div>
      </section>
    </section>
  );
}

export default PropertyDetailsPage;
