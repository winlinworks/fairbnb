import { findCountryByName, formattedCountries } from "@/utils/countries";

function CountryFlagAndName({ countryName }: { countryName: string }) {
  const validCountry = findCountryByName(countryName);
  if (!validCountry) return null;

  // const countryName =
  //   validCountry.name.length > 20
  //     ? `${validCountry?.name.substring(0, 20)}...`
  //     : validCountry.name;
  return (
    <span className="flex justify-between items-center gap-2 text-sm">
      {validCountry.flag}
      {countryName}
    </span>
  );
}

export default CountryFlagAndName;
