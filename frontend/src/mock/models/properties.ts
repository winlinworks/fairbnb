import { faker } from "@faker-js/faker";
import { profiles } from "./profiles";
import { Property } from "../types/types";

type CategoryLabel =
  | "cabin"
  | "tent"
  | "airstream"
  | "cottage"
  | "container"
  | "caravan"
  | "tiny"
  | "magic"
  | "warehouse"
  | "lodge";

export const properties: Property[] = [];

for (let idx = 0; idx < faker.number.int({ min: 10, max: 20 }); idx++) {
  const randomProfile = faker.helpers.arrayElement(profiles);
  properties.push({
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    tagline: faker.lorem.sentence(),
    category: faker.helpers.arrayElement<CategoryLabel>([
      "cabin",
      "tent",
      "airstream",
      "cottage",
      "container",
      "caravan",
      "tiny",
      "magic",
      "warehouse",
      "lodge",
    ]),
    image: faker.image.url(),
    country: faker.location.country(),
    description: faker.lorem.paragraph({ min: 5, max: 20 }),
    price: faker.number.int({ min: 100, max: 1000 }),
    guests: faker.number.int({ min: 1, max: 10 }),
    bedrooms: faker.number.int({ min: 1, max: 5 }),
    beds: faker.number.int({ min: 1, max: 5 }),
    baths: faker.number.int({ min: 1, max: 5 }),
    amenities: faker.commerce.productAdjective(),
    createdAt: faker.date.recent(),
    updatedAt: faker.date.recent(),
    profileId: randomProfile.id,
  });
}
