import countries from "world-countries";

export const formattedCountries = countries.map((country) => {
  return {
    code: country.cca2,
    name: country.name.common,
    flag: country.flag,
    region: country.region,
    location: country.latlng,
  };
});

export const findCountryByName = (name: string) => {
  return formattedCountries.find((country) => country.name === name);
};
