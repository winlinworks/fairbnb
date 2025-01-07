import { faker } from "@faker-js/faker";
import { Profile } from "../types/types";

export const profiles: Profile[] = [];

for (let idx = 0; idx < faker.number.int({ min: 10, max: 20 }); idx++) {
  profiles.push({
    id: faker.string.uuid(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    username: faker.internet.username(),
    email: faker.internet.email(),
    profileImage: faker.image.avatar(),
    createdAt: faker.date.recent(),
    updatedAt: faker.date.recent(),
  });
}
